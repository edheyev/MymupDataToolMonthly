import tkinter as tk
import pandas as pd
import data_utils as dp
from data_config import file_info  

def main():
    
    print("Begin Processing files")
    
    # Directory containing the files
    directory = "./quarterly_data_dump"

    raw_data = load_data_files(directory, file_info)
    
    # Clean the data
    cleaned_data = clean_column_names(raw_data)

    
    # Validate data files
    validated_data = validate_data_files(cleaned_data, file_info)
    
    # Produce tables
    
    # Concatenate tables
    
    # Write to file
    
    
def load_data_files(directory, file_info):
    """
    Loads multiple CSV files from a specified directory into a dictionary of pandas DataFrames.

    :param directory: Path to the directory containing the CSV files.
    :param file_info: A dictionary where keys are descriptive names related to the table keys,
                      and values are dictionaries with filenames and columns.
    :return: A dictionary of pandas DataFrames.
    """
    print("Loading data files...")

    dataframes = {}
    for key, info in file_info.items():
        full_path = f"{directory}/{info['filename']}"
        try:
            dataframes[key] = pd.read_csv(full_path)
            print('>' + key)
        except Exception as e:
            print(f"Error loading {full_path}: {e}")
    return dataframes

def clean_column_names(dataframes):
    """
    Cleans column names in all dataframes: replaces spaces with underscores and converts to lowercase.

    :param dataframes: A dictionary of pandas DataFrames.
    :return: A dictionary of pandas DataFrames with cleaned column names.
    """
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        df.columns = [col.replace(' ', '_').lower() for col in df.columns]
        cleaned_dataframes[df_name] = df
    return cleaned_dataframes


def validate_data_files(dataframes, file_info):
    """
    Validates the data in the dataframes.

    :param dataframes: A dictionary of pandas DataFrames.
    :param file_info: A dictionary that maps each DataFrame name to its filename and correct columns.
    :return: A dictionary of pandas DataFrames.
    """
    print("Validating data files...")
    
    for df_name, df in dataframes.items():
        if df_name in file_info:
            correct_columns = file_info[df_name]["columns"]
            print('> checking ' + df_name + ' for ' + ', '.join(correct_columns)) 
            if not set(correct_columns).issubset(df.columns):
                raise ValueError(f"DataFrame {df_name} is missing one or more of the correct columns.")
            print("...ok")
    
    return dataframes



if __name__ == "__main__":
    main()
