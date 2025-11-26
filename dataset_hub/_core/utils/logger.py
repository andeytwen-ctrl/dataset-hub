import logging
from functools import wraps
from logging import Logger
from typing import Optional

from dataset_hub._core.settings.loader import load_settings


def get_logger(name: Optional[str] = None) -> Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name (Optional[str]): The name of the logger. If None,
            the root logger is returned.

    Returns:
        Logger: A logging.Logger instance corresponding to the given name.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logging.getLogger(name)


def log_dataset_doc_from_args(
    dataset_name_arg="dataset_name", task_type_arg="task_type", verbose_arg="verbose"
):  # TODO Add to documentation
    """"""  # TODO add detail doctring

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get arg values
            from inspect import signature

            sig = signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            dataset_name = bound.arguments[dataset_name_arg]
            task_type = bound.arguments[task_type_arg]
            verbose = bound.arguments[verbose_arg]

            result = func(*args, **kwargs)

            if verbose is None:
                settings = load_settings()
                verbose = settings["verbose"]
            if verbose:
                logger = get_logger(func.__module__)
                logger.info(
                    f"Documentation: https://getdataset.github.io/dataset-hub/datasets/{task_type}/{dataset_name}.html"
                )

            return result

        return wrapper

    return decorator
