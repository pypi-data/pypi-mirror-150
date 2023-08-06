import logging
import time
import math
from pathlib import Path
from typing import Union

import torch
from torchinfo import summary


class MetricMonitor:
    """Calculates and stroes the average value of the metrics/loss."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all the parameters to zero."""
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val: float, n: int = 1):
        """Update the value of the metrics and calculate their average value
        over the entire dataset

        Args:
        -----
            val (float): Computed metric (per batch).
            n (int, optional): Batch size. Defaults to 1.
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def get_logger(
    script_name: Union[str, None] = None,
    log_file: Union[
        str, Path, None
    ] = f"logs/pthelper_{time.strftime('%Y%m%dT%H%M%S', time.localtime())}.log",
    stream_handler: bool = True,
) -> logging.getLogger:
    """Initiate the logger to log the progress into a file.
    Args:
    -----
        script_name (str): Name of the scripts outputting the logs.
        log_file (str): Name of the log file. Defaults to `logs/pthelper_{time.strftime('%Y%m%dT%H%M%S', time.localtime())}.log`.
        stream_handler (bool, optional): If true, show logs in the console. Defaults to True.

    Returns:
    --------
        logging.getLogger: Logger object.
    """
    logger = logging.getLogger(name=script_name)
    logger.setLevel(logging.INFO)

    if log_file is not None:
        log_file = Path(log_file)
        log_file.parent.mkdir(
            parents=True, exist_ok=True
        )  # make dir. for log file
        # create handlers
        f_handler = logging.FileHandler(log_file.as_posix(), mode="w")
        # create formatters and add it to the handlers
        f_format = logging.Formatter(
            "%(asctime)s:%(name)s: %(levelname)s:%(message)s"
        )
        f_handler.setFormatter(f_format)
        # add handlers to the logger
        logger.addHandler(f_handler)

    # display the logs in console
    if stream_handler:
        s_handler = logging.StreamHandler()
        s_format = logging.Formatter("%(name)s: %(levelname)s:%(message)s")
        s_handler.setFormatter(s_format)
        logger.addHandler(s_handler)

    return logger


def time_since(since: int, percent: float) -> str:
    """Helper function to time the training and evaluation process.

    Args:
    -----
        since (int): Start time.
        percent (float): Percent to the task done.

    Returns:
    --------
        str: Print elapsed/remaining time to console.
    """

    def as_minutes_seconds(s: float) -> str:
        m = math.floor(s / 60)
        s -= m * 60
        m, s = int(m), int(s)
        return f"{m:2d}m {s:2d}s"

    now = time.time()
    elapsed = now - since
    total_estimated = elapsed / percent
    remaining = total_estimated - elapsed
    return f"{as_minutes_seconds(elapsed)} (remain {as_minutes_seconds(remaining)})"


def get_model_params(model: torch.nn.Module) -> int:
    """Helper function to determine the total number of the trainable parameters
    in the PyTorch model.

    Args:
    -----
        model (torch.nn.Module): Instance of the PyTorch model being used.

    Returns:
    --------
        int: Number of the trainable parameters.
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def model_details(
    model: torch.nn.Module,
    input_size: tuple,
    device: torch.device = torch.device("cpu"),
):
    """Print Keras like model details on the console.

    Args:
    -----
        model (torch.nn.Module): Instance of the PyTorch model being used.
        input_size (tuple): Size of the input.
        device (torch.device): cuda or CPU. Defaults to CPU.
    """
    print("\t\t\t\tMODEL SUMMARY")
    model = model.to(device)
    summary(model, input_size=input_size, device=device)
    x = torch.rand(*input_size)
    x = x.to(device)
    print(f"Batched input size: {x.shape}")
    print(f"Batched output size: {model(x).shape}")
    print(f"Model contains {get_model_params(model)} trainable parameters.")
