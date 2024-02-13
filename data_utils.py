# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:11:17 2024

@author: Edloc
"""

import pandas as pd
import numpy as np


import pandas as pd
import os

def load_data_files(directory, file_info, log_message=None):
    print("Loading data files...")
    # log_message("Loading data files...")
    dataframes = {}
    
    if not os.listdir(directory):
        raise ValueError(f"The directory {directory} is empty")

    for key, info in file_info.items():
        matching_files = [f for f in os.listdir(directory) if f.startswith(info["filename"].split(".")[0])]
        
        if not matching_files:
            error_message = f"Error: Required file starting with '{info['filename'].split('.')[0]}' not found in directory."
            print(error_message)
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
                # log_message(f"Error loading {full_path}: {e}")
                continue  # Optionally continue to try loading other files even if one fails
        
        # Combine all matching DataFrames into one DataFrame for this key
        if combined_df_list:
            dataframes[key] = pd.concat(combined_df_list, ignore_index=True)
        else:
            print(f"No dataframes were loaded for {key}, likely due to errors.")
            log_message(f"No dataframes were loaded for {key}, likely due to errors.")
    
    return dataframes


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
    if not isinstance(dataframe_and_column, tuple) or not hasattr(dataframe_and_column[0], 'columns'):
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
