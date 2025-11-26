from typing import Any

RUNTIME_SETTINGS = {}


def set_option(
    key: str, value: Any
) -> None:  # TODO add validating keys and values and rise Errors
    """"""  # TODO add docstring lice pandas set_option
    RUNTIME_SETTINGS[key] = value
