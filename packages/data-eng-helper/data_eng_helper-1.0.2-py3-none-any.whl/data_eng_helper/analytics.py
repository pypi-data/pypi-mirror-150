import pandas as pd


class Ops:
    """class houses methods that apply common transformations to pandas data frames."""

    @classmethod
    def remove_null_values(cls, pandas_df: pd.DataFrame) -> pd.DataFrame:
        """Removes all null rows."""
        pandas_df = pandas_df.dropna()
        return pandas_df

    @classmethod
    def rotate(cls, data: pd.DataFrame, x: str, y: str, scalar: str) -> pd.DataFrame:
        """Rotates dataframe layout."""
        data = data.T.reset_index().reindex(columns=[x, y, scalar])
        return data
