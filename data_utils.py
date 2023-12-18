# data_utils.py

import pandas as pd

def filter_dataframe(df, toggle_states, toggle_index):
    """
    Filters the DataFrame based on toggle states and a custom filter for specific names.
    
    :param df: pandas DataFrame to filter.
    :param toggle_states: List of boolean values representing toggle states.
    :param toggle_index: Index of the activated toggle.
    :return: Filtered DataFrame.
    """
    # Custom filter for specific names
    if toggle_index == 3:
        return df[df['first_name'].isin(['Burty', 'Claire'])]

    # Determine which rows to show based on toggle states
    selected_rows = []
    if toggle_states[0]:  # First three rows for the first toggle
        selected_rows.extend([0, 1, 2])
    if toggle_states[1]:
        selected_rows.append(1)
    if toggle_states[2]:
        selected_rows.append(2)

    # Make sure to return a DataFrame
    return df.iloc[selected_rows] if selected_rows else pd.DataFrame()

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
