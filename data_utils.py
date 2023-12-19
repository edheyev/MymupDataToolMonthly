# data_utils.py

import pandas as pd

def filter_by_indices(df, indices):
    """
    Filter the DataFrame based on row indices.
    
    :param df: pandas DataFrame to filter.
    :param indices: A list of integers representing row indices.
    :return: Filtered DataFrame.
    """
    if not indices:
        return pd.DataFrame()  # Return an empty DataFrame if indices list is empty
    return df.iloc[indices]

def filter_by_isin(df, column_name, values):
    """
    Filter the DataFrame based on values in a specific column using the .isin() method.
    
    :param df: pandas DataFrame to filter.
    :param column_name: Name of the column to filter by.
    :param values: List of values to filter for in the specified column.
    :return: Filtered DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    return df[df[column_name].isin(values)]
