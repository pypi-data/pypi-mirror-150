import traceback, warnings
import argparse
from typing import List, Literal
from abc import ABCMeta, abstractmethod
import json
from collections import Counter
import numpy as np
from torch.utils import data
from vino.utils.loading import get_sample_loader
from vino.datasets.utils import METAFILE_NOTFOUND_ERR, LOAD_FAIL_MSG


class Abstract_Dataset(data.Dataset):
    def __init__(self, args: argparse.ArgumentParser, split_group: str) -> None:
        """
        NLST Dataset
        params: args - config.
        params: transformer - A transformer object, takes in a PIL image, performs some transforms and returns a Tensor
        params: split_group - ['train'|'dev'|'test'].

        constructs: standard pytorch Dataset obj, which can be fed in a DataLoader for batching
        """
        __metaclass__ = ABCMeta

        super(Abstract_Dataset, self).__init__()

        self.split_group = split_group
        self.args = args

        try:
            self.metadata_json = json.load(open(args.dataset_file_path, "r"))
        except Exception as e:
            raise Exception(METAFILE_NOTFOUND_ERR.format(args.dataset_file_path, e))

        self.input_loader = get_sample_loader(split_group, args)

        self.dataset = self.create_dataset(split_group)
        if len(self.dataset) == 0:
            return

        self.set_sample_weights(args)

        self.print_summary_statement(self.dataset, split_group)

    @abstractmethod
    def create_dataset(
        self, split_group: Literal["train", "dev", "test"]
    ) -> List[dict]:
        """
        Creates the dataset of samples from json metadata file.
        """
        pass

    @abstractmethod
    def skip_sample(self, sample) -> bool:
        """
        Return True if sample should be skipped and not included in data
        """
        return False

    @abstractmethod
    def check_label(self, sample) -> bool:
        """
        Return True if the row contains a valid label for the task
        """
        pass

    @abstractmethod
    def get_label(self, sample):
        """
        Get task specific label for a given sample
        """
        pass

    @property
    @abstractmethod
    def SUMMARY_STATEMENT(self) -> None:
        """
        Prints summary statement with dataset stats
        """
        pass

    def print_summary_statement(self, dataset, split_group):
        statement = "{} DATASET CREATED FOR {}\n.{}".format(
            split_group.upper(), self.args.dataset.upper(), self.SUMMARY_STATEMENT
        )
        print(statement)

    def __len__(self) -> int:
        return len(self.dataset)

    @abstractmethod
    def __getitem__(self, index):
        """
        Fetch single sample from dataset

        Args:
            index (int): random index of sample from dataset

        Returns:
            sample (dict): a sample
        """
        sample = self.dataset[index]
        try:
            return sample
        except Exception:
            warnings.warn(
                LOAD_FAIL_MSG.format(sample["sample_id"], traceback.print_exc())
            )

    def assign_splits(self, metadata_json) -> None:
        """
        Assign samples to data splits

        Args:
            metadata_json (dict): raw json dataset loaded
        """
        for idx in range(len(metadata_json)):
            metadata_json[idx]["split"] = np.random.choice(
                ["train", "dev", "test"], p=self.args.split_probs
            )

    def set_sample_weights(self, args: argparse.ArgumentParser) -> None:
        """
        Set weights for each sample

        Args:
            args (argparse.ArgumentParser)
        """
        if args.class_bal:
            label_dist = [d[args.class_bal_key] for d in self.dataset]
            label_counts = Counter(label_dist)
            weight_per_label = 1.0 / len(label_counts)
            label_weights = {
                label: weight_per_label / count for label, count in label_counts.items()
            }

            print("Class counts are: {}".format(label_counts))
            print("Label weights are {}".format(label_weights))
            self.weights = [label_weights[d[args.class_bal_key]] for d in self.dataset]
        else:
            pass

    @property
    def DATASET_ITEM_KEYS(self) -> list:
        """
        List of keys to be included in sample when being batched

        Returns:
            list
        """
        standard = ["sample_id"]
        return standard
