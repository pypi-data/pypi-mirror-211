import random
import random
import pandas as pd
from ngdataforecast.forecast_model import ForecastModel
import math


class LocalLevel(ForecastModel):
    """
    A forecasting model that uses the data of the previous week as the prediction for the next week.
    The variance is calculated based on the last month's data.
    Scenarios are generated based on a normal distribution centered on the point forecast.
    """

    def __init__(self, input_dict):
        super().__init__(input_dict)

    def _create_point_forecast(self, df, forecast_timestamps):
        """Create the point forecast DataFrame."""
        point_forecast = pd.DataFrame(index=forecast_timestamps, columns=["value"])
        point_forecast["value"] = [
            df[df.index.hour == hour]["value"].iloc[-7]
            for hour in forecast_timestamps.hour
        ]
        return point_forecast

    def _calculate_variance(self, df, forecast_timestamps):
        """Calculate the variance DataFrame."""
        # Initialize an empty DataFrame for variance
        variance = pd.DataFrame(index=forecast_timestamps, columns=["variance"])

        # Extract the hour from the timestamp
        df["hour"] = df.index.hour

        # Group the DataFrame by hour and calculate the mean
        df_mean_by_hour = df.groupby("hour").mean()

        # Calculate the variance for each hour of the day
        for hour in range(24):
            hour_data = df[df["hour"] == hour]["value"]
            hour_mean = df_mean_by_hour.loc[hour, "value"]
            hour_var = ((hour_data - hour_mean) ** 2).mean()

            # Create a mask for the respective hour
            mask = variance.index.hour == hour
            variance.loc[mask, "variance"] = hour_var

        return variance

    def _generate_scenarios(self, point_forecast, variance, forecast_timestamps):
        """Generate the scenarios DataFrame."""
        scenarios = pd.DataFrame(index=forecast_timestamps)
        for i in range(
            self.inputs["metadata"]["number_of_scenarios"]
        ):  # create 3 scenarios
            scenarios[f"scenario_{i+1}"] = point_forecast["value"] + [
                random.gauss(0, math.sqrt(variance["variance"].iloc[0]))
                for _ in range(len(forecast_timestamps))
            ]
        return scenarios

    def forecast(self):
        """
        Perform the forecast.
        """

        # Retrieve the dependent variable data
        df = self.inputs["dependent_variable"]

        # Create DataFrames to store forecast
        last_timestamp = df.index.max()
        forecast_timestamps = pd.date_range(
            start=last_timestamp, periods=24 * 7 + 1, freq="H"
        )[
            1:
        ]  # Assuming hourly frequency

        self.forecast = {}

        # Point forecast
        self.forecast["point_forecast"] = self._create_point_forecast(
            df, forecast_timestamps
        )

        # Variance
        self.forecast["variance"] = self._calculate_variance(df, forecast_timestamps)

        # Scenarios
        self.forecast["scenarios"] = self._generate_scenarios(
            self.forecast["point_forecast"],
            self.forecast["variance"],
            forecast_timestamps,
        )

        # Initialize empty model statistics
        self.model_statistics = {"residuals": pd.DataFrame(), "statistical_tests": {}}

        return self.forecast
