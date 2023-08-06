import os
from vino.utils.registry import register_object
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor

# TODO: add args for various callbacks -- currently hardcoded


@register_object("checkpointer", "callback")
class Checkpoint(ModelCheckpoint):
    def __init__(self, args) -> None:
        super().__init__(
            monitor=args.monitor,
            dirpath=os.path.join(args.save_dir, args.experiment_name),
            mode="min" if "loss" in args.monitor else "max",
            filename="{}".format(args.experiment_name) + "{epoch}",
            every_n_epochs=1,
            save_top_k=args.checkpoint_save_top_k,
            save_last=args.checkpoint_save_last,
        )


@register_object("lr_monitor", "callback")
class LRMonitor(LearningRateMonitor):
    def __init__(self, args) -> None:
        super().__init__(logging_interval="step")
