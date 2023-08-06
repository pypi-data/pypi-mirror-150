import torch
from torch import optim
from vino.utils.registry import register_object


@register_object("reduce_on_plateau", "scheduler")
class ReduceLROnPlateau(optim.lr_scheduler.ReduceLROnPlateau):
    """
    https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html#torch.optim.lr_scheduler.ReduceLROnPlateau
    """

    def __init__(self, optimizer, args):
        super().__init__(
            optimizer,
            patience=args.patience,
            factor=args.lr_decay,
            mode="min" if "loss" in args.monitor else "max",
        )


@register_object("exponential_decay", "scheduler")
class ExponentialLR(optim.lr_scheduler.ExponentialLR):
    """
    https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ExponentialLR.html#torch.optim.lr_scheduler.ExponentialLR
    """

    def __init__(self, optimizer, args):
        super().__init__(optimizer, gamma=args.lr_decay)


@register_object("cosine_annealing", "scheduler")
class CosineAnnealingLR(optim.lr_scheduler.CosineAnnealingLR):
    """
    https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html
    """

    def __init__(self, optimizer, args):
        super().__init__(optimizer, args.cosine_annealing_period)


@register_object("cosine_annealing_restarts", "scheduler")
class CosineAnnealingWarmRestarts(optim.lr_scheduler.CosineAnnealingWarmRestarts):
    """
    https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingWarmRestarts.html#torch.optim.lr_scheduler.CosineAnnealingWarmRestarts
    """

    def __init__(self, optimizer, args):
        super().__init__(
            optimizer,
            T_0=args.cosine_annealing_period,
            T_mult=args.cosine_annealing_period_scaling,
        )
