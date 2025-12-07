from typing import Optional

import pandas as pd

from dataset_hub._core.data_bundle import DataBundle
from dataset_hub._core.get_data import get_data as _get_data

task_type = "timeseries"


def get_household_power(verbose: Optional[bool] = None) -> pd.DataFrame:
    """ """

    dataset: DataBundle[pd.DataFrame] = _get_data(
        dataset_name="household_power", task_type=task_type, verbose=verbose
    )
    return dataset["data"]
