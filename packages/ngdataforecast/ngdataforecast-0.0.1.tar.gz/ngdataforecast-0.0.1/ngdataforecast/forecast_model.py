import pandas as pd
from typing import Dict, Any


class ForecastModel:
    def __init__(self, input_dict: Dict[str, Any]):
        """
        Initialize ForecastModel with input_dict.

        Args:
            input_dict (dict): A dictionary containing metadata, dependent variable,
                and explanatory variables for a SARIMA forecast model.
        """
        self.input_dict = input_dict
        self.inputs = {}

    def process_inputs(self):
        """
        Process input dictionary and validate it.

        This method transforms the data into Pandas DataFrames
        and store them into self.inputs.
        """
        self._process_metadata()
        self._process_dependent_variable()
        self._process_explanatory_variables()

        self._validate_inputs()

        # Add utils
        self.inputs["utils"] = {}
        self.inputs["utils"]["date_dim"] = self.generate_date_dim()

    def _process_metadata(self):
        """
        Process and validate metadata.
        """
        self.inputs["metadata"] = self.input_dict["metadata"]
        if not isinstance(self.inputs["metadata"], dict):
            raise ValueError("Metadata should be a dictionary.")

    def _process_dependent_variable(self):
        """
        Process and validate dependent variable.
        """
        dv = self.input_dict["dependent_variable"]
        if not isinstance(dv, dict):
            raise ValueError("Dependent variable should be a dictionary.")
        dv_df = pd.DataFrame(dv["data"])
        dv_df["timestamp"] = pd.to_datetime(dv_df["timestamp"])
        self.inputs["dependent_variable"] = dv_df.set_index("timestamp")

    def _process_explanatory_variables(self):
        """
        Process and validate explanatory variables.
        """
        evs = self.input_dict["explanatory_variables"]
        self.inputs["explanatory_variables"] = {}
        if not isinstance(evs, list):
            raise ValueError("Explanatory variables should be a list.")
        for ev in evs:
            ev_df = pd.DataFrame(ev["data"])
            ev_df["timestamp"] = pd.to_datetime(ev_df["timestamp"])
            self.inputs["explanatory_variables"][ev["name"]] = ev_df.set_index(
                "timestamp"
            )

    def compute_quantiles(self, scenarios):
        """
        Given a DataFrame of scenarios, computes the quantiles for each timestamp.
        """

        quantiles_dict = {}

        # Calculate quantiles for each timestamp
        for timestamp in scenarios.index:
            scenario_values = scenarios.loc[timestamp]
            quantiles_dict[str(timestamp)] = scenario_values.quantile(
                [0.5, 0.75, 0.9, 0.99]
            ).to_dict()

        return quantiles_dict

    def convert_to_output_format(self):
        """Converts the class instance to the desired output format."""

        output = {
            "metadata": self.inputs["metadata"],
            "forecast": [],
            "model_statistics": {
                "residuals": self.model_statistics["residuals"]
                .reset_index()
                .to_dict("records"),
                "statistical_tests": self.model_statistics["statistical_tests"],
            },
        }

        # Calculate quantiles
        quantiles = self.compute_quantiles(self.forecast["scenarios"])

        for i in range(len(self.forecast["point_forecast"])):
            timestamp = str(self.forecast["point_forecast"].index[i])

            forecast_item = {
                "timestamp": timestamp,
                "point_forecast": self.forecast["point_forecast"]["value"].iloc[i],
                "variance": self.forecast["variance"]["variance"].iloc[i],
                "scenarios": [],
                "quantiles": quantiles[timestamp],
            }

            for scenario_column in self.forecast["scenarios"].columns:
                scenario_value = self.forecast["scenarios"][scenario_column].iloc[i]
                forecast_item["scenarios"].append({scenario_column: scenario_value})

            output["forecast"].append(forecast_item)

        return output

    def generate_date_dim(self):
        """
        Generate a DataFrame with additional information about the timestamps.

        The DataFrame includes day of week, day of month, and whether the day is a weekday.
        This information can be useful for analyzing time series data.
        """
        # Extract timestamps from dependent variable
        timestamps = self.inputs["dependent_variable"].index
        df_date_dim = pd.DataFrame(index=timestamps)

        # Add additional date information
        df_date_dim["day_of_week"] = df_date_dim.index.dayofweek
        df_date_dim["day_of_month"] = df_date_dim.index.day
        df_date_dim["is_weekday"] = df_date_dim["day_of_week"].apply(
            lambda x: 1 if x < 5 else 0
        )

        return df_date_dim

    def _validate_inputs(self):
        """
        Validate inputs. The purpose of this function is to ensure that
        the data fed into the model is appropriate and as expected.

        This could involve checking the type of the data, ensuring
        that required keys are in the dictionary, etc.

        If any validation fails, an error should be raised.
        """
        # Extract dependent variable timestamps
        dv_timestamps = set(self.inputs["dependent_variable"].index)

        # Iterate over each exogenous variable and compare timestamps
        for name, df in self.inputs["explanatory_variables"].items():
            # Check if timestamps match
            if set(df.index) != dv_timestamps:
                raise ValueError(
                    f"Timestamps of {name} do not match with dependent variable timestamps."
                )

            # Check for null values
            if df.isnull().values.any():
                raise ValueError(f"{name} contains null values.")

        # Check for null values in dependent variable
        if self.inputs["dependent_variable"].isnull().values.any():
            raise ValueError("Dependent variable contains null values.")

        # verify that number of scenarios is present and greater than 0
