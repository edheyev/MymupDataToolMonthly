# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:11:17 2024

@author: Edloc
"""

import pandas as pd
import numpy as np


def find_dict_by_table_name(table_name, dict_array):
    for dictionary in dict_array:
        if dictionary.get("table_name") == table_name:
            return dictionary
    raise ValueError(
        f"Dictionary with table_name '{table_name}' not found in the array."
    )


def calculate_percentage(numerator_df, denominator_df):
    # Example: calculate a simple percentage
    numerator = len(numerator_df)
    denominator = len(denominator_df)

    if denominator == 0:
        return "0%"  # Avoid division by zero
    else:
        percentage = (numerator / denominator) * 100
        return f"{percentage:.2f}%"  # Format to two decimal places


def calculate_average(dataframe_and_column):
    # Unpack the tuple into DataFrame and column name
    dataframe, column_name = dataframe_and_column

    # Check if the column exists in the DataFrame
    if column_name in dataframe.columns:
        # Calculate the average of the specified column
        average_value = dataframe[column_name].mean()
        return f"{average_value:.2f}"  # Format to two decimal places
    else:
        return "n/a"


def calculate_count(filtered_df):
    count = len(filtered_df)
    return count


def calculate_row_total(row_dataframes):
    # Sum up counts, skipping placeholders
    total = sum(len(df) for df in row_dataframes if isinstance(df, pd.DataFrame))
    return total


def calculate_percentage_row_total(row_dataframes):
    total_numerator = 0
    total_denominator = 0

    for cell in row_dataframes:
        if cell is None or not isinstance(cell, tuple):
            continue  # Skip None values and non-tuple values

        numerator_df, denominator_df = cell
        total_numerator += len(numerator_df)
        total_denominator += len(denominator_df)

    if total_denominator == 0:
        return "0%"  # Avoid division by zero

    total_percentage = (total_numerator / total_denominator) * 100
    return f"{total_percentage:.2f}%"


def calculate_row_average(row_dataframes):
    averages = []

    for dataframe_and_column in row_dataframes:
        # Use calculate_average function to get the average for each column
        average_value = calculate_average(dataframe_and_column)

        # Check if the returned value is numeric and add it to the list of averages
        if average_value.replace(".", "", 1).isdigit():
            averages.append(float(average_value))

    # Calculate the overall average if there are valid averages in the list
    if averages:
        return round(sum(averages) / len(averages), 2)
    else:
        return "n/a"


def calculate_percentage_as_number(numerator_df, denominator_df):
    # Calculate percentage as a numeric value for summing
    numerator = len(numerator_df)
    denominator = len(denominator_df)

    if denominator == 0:
        return 0  # Avoid division by zero
    else:
        return (numerator / denominator) * 100


def is_percentage_row(row_name):
    return row_name.startswith("%") or row_name.startswith("Percentage")


def is_average_row(row_name):
    return row_name.startswith("average") or row_name.startswith("Average")
