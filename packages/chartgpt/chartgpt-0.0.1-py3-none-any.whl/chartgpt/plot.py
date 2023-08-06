from pydantic import BaseModel
import pandas as pd
from typing import List, Dict, Union, Optional, Tuple, Any
from plotly.graph_objects import Figure

class ChartGPT:
    """ChartGPT object. This is the main object of the ChartGPT package.

    Args:
        df (pd.DataFrame): A DataFrame.
        description (Optional[str], optional): A description of the chart. Defaults to "A chart.".
    """

    def __init__(self, df:pd.DataFrame, *args, **kwargs):
        print("ChartGPT model initialized")
        self.figure = Figure()
        self.plot(df, *args, **kwargs)
        self.memory = None

    def create_chart(self, df:pd.DataFrame):
        """Plot a chart from a DataFrame.

        Args:
            df (pd.DataFrame): A DataFrame.
            description (Optional[str], optional): A description of the chart. Defaults to "A chart.".

        Returns:
            Figure: A Plotly figure.
        """
        print(f"Plotting chart")

    def update_chart(self, figure:Figure, prompt:str):
        """Update the chart with new data.

        Args:
            df (pd.DataFrame): A DataFrame.

        Returns:
            Figure: A Plotly figure.
        """
        print(f"Updating chart")

    def __repr__(self):
        return f"ChartGPT()"


class ChartGPT:
    def __init__(self) -> None:
        pass

    def load(self, df:pd.DataFrame) -> None:
        """Load a DataFrame into ChartGPT.

        Args:
            df (pd.DataFrame): A DataFrame.
        """
        self.memory = df

    def plot(self, prompt:str):
        pass
