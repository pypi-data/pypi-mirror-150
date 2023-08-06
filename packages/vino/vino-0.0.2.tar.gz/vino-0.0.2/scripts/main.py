from ast import arg
from collections import OrderedDict
import pickle
import os
import sys
import time
import git
import comet_ml
import pytorch_lightning as pl
from pytorch_lightning import _logger as log

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from vino.parsing import parse_args
from vino.utils.registry import get_object
from vino.datasets.utils import get_censoring_dist
import vino.utils.loading as loaders
from vino.utils.callbacks import set_callbacks


def cli_main(args):

    args.checkpoint_callback = False

    trainer = pl.Trainer.from_argparse_args(args)
    # Remove callbacks from args for safe pickling later
    args.callbacks = None
    args.num_nodes = trainer.num_nodes
    args.num_processes = trainer.num_processes
    args.world_size = args.num_nodes * args.num_processes
    args.global_rank = trainer.global_rank
    args.local_rank = trainer.local_rank

    if args.logger_name == "comet":
        tb_logger = pl.loggers.CometLogger(
            api_key=os.environ.get("COMET_API_KEY"),
            project_name=args.project_name,
            experiment_name=args.experiment_name,
            workspace=args.workspace,
            log_env_details=True,
            log_env_cpu=True,
        )
        trainer.logger = tb_logger

    repo = git.Repo(search_parent_directories=True)
    commit = repo.head.object
    log.info(
        "\nProject main running by author: {} \ndate:{}, \nfrom commit: {} -- {}".format(
            commit.author,
            time.strftime("%m-%d-%Y %H:%M:%S", time.localtime(commit.committed_date)),
            commit.hexsha,
            commit.message,
        )
    )

    train_dataset = loaders.get_train_dataset_loader(
        args, get_object(args.dataset, "dataset")(args, "train")
    )
    dev_dataset = loaders.get_eval_dataset_loader(
        args, get_object(args.dataset, "dataset")(args, "dev"), False
    )

    # print args
    for key, value in sorted(vars(args).items()):
        print("{} -- {}".format(key.upper(), value))

    # create or load lightning model from checkpoint
    model = loaders.get_lightning_model(args)

    if args.logger_name == "comet":
        # log to comet
        trainer.logger.experiment.set_model_graph(model)
        trainer.logger.experiment.add_tags(args.comet_tags)
        trainer.logger.experiment.log_parameters(args)

    # add callbacks
    trainer.callbacks = set_callbacks(trainer, args)

    if args.train:
        if "survival" in args.metrics:
            # compute censoring distribution
            args.censoring_distribution = get_censoring_dist(train_dataset.dataset)
        log.info("\nTraining Phase...")
        trainer.fit(model, train_dataset, dev_dataset)
        args.model_path = trainer.checkpoint_callback.best_model_path

    if args.dev:
        log.info("\nValidation Phase...")
        trainer.test(
            model, dev_dataset, ckpt_path=args.model_path
        ) if args.train else trainer.test(model, dev_dataset)

    # testing
    if args.test:
        log.info("\nInference Phase on test set...")
        test_dataset = loaders.get_eval_dataset_loader(
            args, get_object(args.dataset, "dataset")(args, "test"), False
        )
        trainer.test(
            model, test_dataset, ckpt_path=args.model_path
        ) if args.train else trainer.test(model, test_dataset)

    if args.eval_on_train:
        log.info("\nInference Phase on train set...")
        train_dataset = loaders.get_eval_dataset_loader(
            args, get_object(args.dataset, "dataset")(args, "train"), False
        )
        trainer.test(model, train_dataset)

    print("Saving args to {}.args".format(args.results_path))
    pickle.dump(vars(args), open("{}.args".format(args.results_path), "wb"))


if __name__ == "__main__":
    args = parse_args()
    cli_main(args)
