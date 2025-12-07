from dataset_hub.classification.datasets import get_iris, get_titanic
from dataset_hub.regression.datasets import get_housing
from dataset_hub.timeseries.datasets import get_household_power

SMOKE_DATAFRAME_DATASETS = [get_titanic]
AVAILABILITY_DATAFRAME_DATASETS = [
    get_titanic,
    get_iris,
    get_housing,
    get_household_power,
]
