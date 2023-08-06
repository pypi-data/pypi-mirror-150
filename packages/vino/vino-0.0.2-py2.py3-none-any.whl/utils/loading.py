from argparse import Namespace, FileType
import pickle
import collections.abc as container_abcs
import re
from tabnanny import check
from typing import Literal
from vino.utils.registry import get_object
import torch
from torch.utils import data
from vino.utils.sampler import DistributedWeightedSampler
from vino.utils.augmentations import get_augmentations
from pytorch_lightning.utilities.cloud_io import load as pl_load
from vino.loaders.image_loaders import OpenCVLoader, DicomLoader
from pytorch_lightning.utilities.cloud_io import load as pl_load

string_classes = (str, bytes)
int_classes = int
np_str_obj_array_pattern = re.compile(r"[SaUO]")

default_collate_err_msg_format = (
    "default_collate: batch must contain tensors, numpy arrays, numbers, "
    "dicts, MoleculeDatapoint or lists; found {}"
)


def default_collate(batch):
    r"""Puts each data field into a tensor with outer dimension batch size"""

    elem = batch[0]
    elem_type = type(elem)
    if isinstance(elem, torch.Tensor):
        out = None
        if torch.utils.data.get_worker_info() is not None:
            # If we're in a background process, concatenate directly into a
            # shared memory tensor to avoid an extra copy
            numel = sum([x.numel() for x in batch])
            storage = elem.storage()._new_shared(numel)
            out = elem.new(storage)
        return torch.stack(batch, 0, out=out)
    elif (
        elem_type.__module__ == "numpy"
        and elem_type.__name__ != "str_"
        and elem_type.__name__ != "string_"
    ):
        if elem_type.__name__ == "ndarray" or elem_type.__name__ == "memmap":
            # array of string classes and object
            if np_str_obj_array_pattern.search(elem.dtype.str) is not None:
                raise TypeError(default_collate_err_msg_format.format(elem.dtype))

            return default_collate([torch.as_tensor(b) for b in batch])
        elif elem.shape == ():  # scalars
            return torch.as_tensor(batch)
    elif isinstance(elem, float):
        return torch.tensor(batch, dtype=torch.float64)
    elif isinstance(elem, int_classes):
        return torch.tensor(batch)
    elif isinstance(elem, string_classes):
        return batch
    elif isinstance(elem, container_abcs.Mapping):
        return {key: default_collate([d[key] for d in batch]) for key in elem}
    elif isinstance(elem, tuple) and hasattr(elem, "_fields"):  # namedtuple
        return elem_type(*(default_collate(samples) for samples in zip(*batch)))
    elif isinstance(elem, container_abcs.Sequence):
        # check to make sure that the elements in batch have consistent size
        it = iter(batch)
        elem_size = len(next(it))
        if not all(len(elem) == elem_size for elem in it):
            raise RuntimeError("each element in list of batch should be of equal size")
        transposed = zip(*batch)
        return [default_collate(samples) for samples in transposed]

    raise TypeError(default_collate_err_msg_format.format(elem_type))


def ignore_None_collate(batch):
    """
    default_collate wrapper that creates batches only of not None values.
    Useful for cases when the dataset.__getitem__ can return None because of some
    exception and then we will want to exclude that sample from the batch.
    """
    batch = [x for x in batch if x is not None]
    if len(batch) == 0:
        return None
    return default_collate(batch)


def get_train_dataset_loader(args, train_data):
    """
    Given arg configuration, return appropriate torch.DataLoader
    for train_data and dev_data

    returns:
    train_data_loader: iterator that returns batches
    dev_data_loader: iterator that returns batches
    """
    if args.class_bal:
        if args.accelerator == "ddp":
            sampler = DistributedWeightedSampler(
                train_data,
                weights=train_data.weights,
                replacement=True,
                rank=args.global_rank,
                num_replicas=args.world_size,
            )
        else:
            sampler = data.sampler.WeightedRandomSampler(
                weights=train_data.weights,
                num_samples=len(train_data),
                replacement=True,
            )
    else:
        if args.accelerator == "ddp":
            sampler = torch.utils.data.distributed.DistributedSampler(
                train_data,
                shuffle=True,
                rank=args.global_rank,
                num_replicas=args.world_size,
            )
        else:
            sampler = data.sampler.RandomSampler(train_data)

    train_data_loader = data.DataLoader(
        train_data,
        num_workers=args.num_workers,
        sampler=sampler,
        pin_memory=True,
        batch_size=args.batch_size,
        collate_fn=ignore_None_collate,
    )

    return train_data_loader


def get_eval_dataset_loader(args, eval_data, shuffle):

    if args.accelerator == "ddp":
        sampler = torch.utils.data.distributed.DistributedSampler(
            eval_data,
            shuffle=shuffle,
            rank=args.global_rank,
            num_replicas=args.world_size,
        )
    else:
        sampler = (
            torch.utils.data.sampler.RandomSampler(eval_data)
            if shuffle
            else torch.utils.data.sampler.SequentialSampler(eval_data)
        )
    data_loader = torch.utils.data.DataLoader(
        eval_data,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        collate_fn=ignore_None_collate,
        pin_memory=True,
        drop_last=False,
        sampler=sampler,
    )

    return data_loader


@torch.no_grad()
def concat_all_gather(tensor):
    """
    Performs all_gather operation on the provided tensors.
    *** Warning ***: torch.distributed.all_gather has no gradient.
    """

    tensors_gather = [
        torch.ones_like(tensor) for _ in range(torch.distributed.get_world_size())
    ]
    torch.distributed.all_gather(tensors_gather, tensor, async_op=False)
    output = torch.cat(tensors_gather, dim=0)
    return output


def get_sample_loader(split_group: Literal["train", "dev", "test"], args: Namespace):
    """[summary]

    Parameters
    ----------
    ``split_group`` : str
        dataset split according to which the augmentation is selected (choices are ['train', 'dev', 'test'])
    ``args`` : Namespace
        global args

    Returns
    -------
    abstract_loader
        sample loader (DicomLoader for dicoms or OpenCVLoader pngs). see sybil.loaders.image_loaders
    """
    if split_group in ["test", "dev"]:
        augmentations = get_augmentations(
            args.test_rawinput_augmentations, args.test_tnsr_augmentations, args
        )
    else:
        augmentations = get_augmentations(
            args.train_rawinput_augmentations, args.train_tnsr_augmentations, args
        )
    return get_object(args.input_loader_name, "input_loader")(
        args.cache_path, augmentations, args
    )


def get_lightning_model(args: Namespace):
    """Create new model or load from checkpoint

    Args:
        args (Namespace): global args

    Raises:
        FileType: snapshot must be ".args" or ".ckpt" file

    Returns:
        model: pl.LightningModule instance
    """
    if args.from_checkpoint:
        if args.snapshot.endswith(".args"):
            snargs = Namespace(**pickle.load(open(args.snapshot, "rb")))
            # update saved args with new arguments
            for k, v in vars(args).items():
                if k not in snargs:
                    snargs.__setattr__(k, v)
            model = get_object(snargs.lightning_name, "lightning")(snargs)
            modelpath = snargs.model_path
        elif args.snapshot.endswith(".ckpt"):
            model = get_object(args.lightning_name, "lightning")(args)
            modelpath = args.snapshot
            checkpoint = pl_load(
                args.snapshot, map_location=lambda storage, loc: storage
            )
            snargs = checkpoint["hyper_parameters"]["args"]
        else:
            raise FileType("Snapshot should be an args or ckpt file.")
        # update args with old args if not found
        for k, v in vars(snargs).items():
            if k not in args:
                args.__setattr__(k, v)
        model = model.load_from_checkpoint(
            checkpoint_path=modelpath,
            strict=not args.relax_checkpoint_matching,
            **{"args": args}
        )
    else:
        model = get_object(args.lightning_name, "lightning")(args)
    return model
