# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:11:17 2024

@author: Edloc
"""

import pandas as pd
import numpy as np
import os
import sys



def load_data_files(directory, file_info, log_message=None):
    print("Loading data files...")
    dataframes = {}

    if not os.listdir(directory):
        raise ValueError(f"The directory {directory} is empty")

    for key, info in file_info.items():
        base_filename = info["filename"].split(".")[0]
        # Adjust the pattern to include files with and without '_mib_' after the base filename
        matching_files = [
            f
            for f in os.listdir(directory)
            if base_filename in f and (f.endswith(".csv") or "_mib_" in f)
        ]

        if not matching_files:
            error_message = f"Error: Required file starting with '{base_filename}' not found in directory."
            print(error_message)
            if log_message:
                log_message(error_message)
            sys.exit(1)  # Exit with an error code if files are missing

        combined_df_list = []
        for file_name in matching_files:
            full_path = os.path.join(directory, file_name)
            try:
                df = pd.read_csv(full_path)
                combined_df_list.append(df)
                print(f"> Loaded {key} from {file_name}")
            except Exception as e:
                print(f"Error loading {full_path}: {e}")
                if log_message:
                    log_message(f"Error loading {full_path}: {e}")
                continue  # Optionally continue to try loading other files even if one fails

        # Combine all matching DataFrames into one DataFrame for this key
        if combined_df_list:
            dataframes[key] = pd.concat(combined_df_list, ignore_index=True)
        else:
            print(f"No dataframes were loaded for {key}, likely due to errors.")
            if log_message:
                log_message(
                    f"No dataframes were loaded for {key}, likely due to errors."
                )

    return dataframes


def isolate_date_range(df, date_column, date_range=None):
    """
    Filters the DataFrame to include rows where the date in the specified column falls within the given date range.

    Parameters:
    - df: DataFrame to filter.
    - date_column: The name of the column containing date values in "DD/MM/YYYY" format.
    - date_range: A tuple containing the start and end date of the range as strings in "YYYY-MM-DD" format. Defaults to None.

    Returns:
    - A DataFrame filtered to include only rows within the specified date range if provided, otherwise returns the original DataFrame.
    """

    # Convert the date column from "DD/MM/YYYY" to datetime format
    df = df.copy()
    df.loc[:, date_column] = pd.to_datetime(
        df[date_column], format="%d/%m/%Y", errors="coerce"
    )

    # If a date range is provided, convert start_date and end_date from "YYYY-MM-DD" to datetime for comparison
    if date_range:
        start_date, end_date = date_range
        # Convert start_date and end_date strings to datetime
        # start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
        # end_date = pd.to_datetime(end_date, format="%Y-%m-%d")

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filter the DataFrame based on the date range
        mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
        filtered_df = df.loc[mask]
    else:
        # If no date range is provided, return the original DataFrame or handle differently
        filtered_df = df

    return filtered_df


def get_previous_month_date_range(date_range):
    """
    Takes a date range tuple and returns a tuple for the previous month's corresponding date range.

    Parameters:
    - date_range: A tuple containing the start and end date of the range as strings in "YYYY-MM-DD" format.

    Returns:
    - A tuple containing the start and end date of the previous month's range as strings in "YYYY-MM-DD" format.
    """

    # Convert start_date and end_date strings to datetime
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Calculate the first day of the current month's start_date
    first_day_current_month = start_date.replace(day=1)

    # Calculate the last day of the previous month, which is one day before the first day of the current month
    last_day_previous_month = first_day_current_month - pd.Timedelta(days=1)

    # Calculate the first day of the previous month
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Convert dates back to "YYYY-MM-DD" string format for output
    prev_month_start_date = first_day_previous_month.strftime("%Y-%m-%d")
    prev_month_end_date = last_day_previous_month.strftime("%Y-%m-%d")

    return (prev_month_start_date, prev_month_end_date)


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
    # Ensure the input is actually a DataFrame and column tuple
    if not isinstance(dataframe_and_column, tuple) or not hasattr(
        dataframe_and_column[0], "columns"
    ):
        raise TypeError("Expected a tuple with a DataFrame and column name")

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
