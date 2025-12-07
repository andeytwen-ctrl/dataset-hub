from typing import Optional

import pandas as pd

from dataset_hub._core.data_bundle import DataBundle
from dataset_hub._core.get_data import get_data as _get_data

task_type = "timeseries"


def get_household_power(verbose: Optional[bool] = None) -> pd.DataFrame:
    """
    Load and return the Individual Household Electric Power Consumption dataset.

    Measurements of **electric power consumption in a single household** with a one-minute \
        sampling rate over a period of almost 4 years (December 2006 – November 2010). \
        Each record contains several electrical and sub-metering measurements.
     
    
    This dataset is designed for minute-level analysis of total household energy \
        consumption, capturing overall usage patterns of a single home.


    Original dataset: This dataset is available on the UCI Machine Learning \
        Repository:  
    `Individual Household Electric Power Consumption <https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption>`_

    Columns:

    - ``Date`` (str): Date of measurement in format dd/mm/yyyy
    - ``Time`` (str): Time of measurement in format hh:mm:ss
    - ``Global_active_power`` (float): Household global minute-averaged active \
        power (kilowatt)
    - ``Global_reactive_power`` (float): Household global minute-averaged reactive \
        power (kilowatt)
    - ``Voltage`` (float): Minute-averaged voltage (volt)
    - ``Sub_metering_1`` (float): Energy sub-metering No. 1 \
        (kitchen: dishwasher, oven, microwave; watt-hour of active energy)
    - ``Sub_metering_2`` (float): Energy sub-metering No. 2 \
        (laundry room: washing machine, tumble-drier, refrigerator, light; watt-hour)
    - ``Sub_metering_3`` (float): Energy sub-metering No. 3 \
        (electric water-heater, air-conditioner; watt-hour)
    - ``Global_intensity`` 🚩 (float): Household global minute-averaged current \
        intensity (ampere)

    Notes:
    - Missing values are present in approximately 1.25% of the rows. 
    - Active energy not covered by sub-meterings 1–3 can be calculated as:  
    `(Global_active_power*1000/60 - Sub_metering_1 - Sub_metering_2 - Sub_metering_3)` \
        in watt-hour.

    Args:
        verbose (bool, optional):
            If True, the function prints a link to the dataset documentation \
                in the log output after loading. (e.g., on this page)
            Default is None, which uses the global :ref:`settings`.

    Returns:
        pandas.DataFrame: The household power consumption dataset with all features.

    Quick Start:

    .. code-block:: python

        import dataset_hub

        household_power = dataset_hub.timeseries.get_household_power()

    Baseline:

    .. note::

        You need to install the following packages before running this baseline:

        .. code-block:: bash
        
            pip install prophet 
            pip install matplotlib

    .. code-block:: python

        import pandas as pd
        from prophet import Prophet
        from dataset_hub.timeseries import get_household_power
        import numpy as np
        import matplotlib.pyplot as plt

        # Load dataset
        household_power = get_household_power()

        # Combine Date and Time into datetime
        household_power["datetime"] = pd.to_datetime(household_power["Date"] + " " + household_power["Time"], dayfirst=True)
        household_power = household_power.drop(["Date", "Time"], axis=1)

        # Aggregate to monthly mean
        monthly_power = household_power.resample("ME", on="datetime").mean().reset_index()

        # Prepare data for Prophet
        df_prophet = monthly_power[["datetime", "Global_active_power"]].rename(columns={"datetime": "ds", "Global_active_power": "y"})
        df_prophet["y"] = df_prophet["y"].ffill()

        # Drop incomplete last month
        df_prophet = df_prophet.iloc[:-1]

        # Split: train on all except last full month
        train_df = df_prophet.iloc[:-1]
        test_df = df_prophet.iloc[-1:]

        # ========================
        # Part 1: Monthly forecast
        # ========================
        model = Prophet(daily_seasonality=False, yearly_seasonality=True)
        model.fit(train_df)

        # Create future dataframe for next month
        future = model.make_future_dataframe(periods=1, freq='ME')
        forecast = model.predict(future)

        # Plot monthly forecast
        fig1 = model.plot(forecast)
        plt.title("Prophet monthly forecast of Global Active Power for next month")
        plt.show()

        # Plot components (trend, yearly seasonality)
        fig2 = model.plot_components(forecast)
        plt.show()

        # =================================
        # Part 2: Next month forecast error
        # =================================
        # Predicted and actual for the last month
        pred_total = forecast.iloc[-1]["yhat"]
        actual_total = test_df["y"].values[0]

        # Compute percentage error
        mape = np.abs((actual_total - pred_total) / actual_total) * 100

        # Note: This is NOT a classical MAPE or robust model evaluation.
        # We are showing the percentage error on a single month forecast as an illustrative example only.
        print(f"Percentage error for next month forecast: {mape:.2f}%") # 7.58%
    """  # noqa: E501

    dataset: DataBundle[pd.DataFrame] = _get_data(
        dataset_name="household_power", task_type=task_type, verbose=verbose
    )
    return dataset["data"]
