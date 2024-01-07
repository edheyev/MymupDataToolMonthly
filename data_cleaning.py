#from data_config import yim_providers
import pandas as pd

def clean_column_names(dataframes):
    print("Standardizing column names...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        new_columns = []
        for col in df.columns:
            col = col.replace(" ", "_").lower()
            if col == "service_type":
                col = "contact_service_type"
            # elif col == "file_closure_service_type":
            #      col = "contact_service_type"
            new_columns.append(col)
        df.columns = new_columns
        cleaned_dataframes[df_name] = df
    return cleaned_dataframes


def remove_duplicates(dataframes):
    print("Removing duplicates...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        # This will drop rows only if every column in the row is identical to another row
        cleaned_dataframes[df_name] = df.drop_duplicates()

    return cleaned_dataframes



def isolate_reporting_period(dataframes, start_date, end_date, date_column):
    print("Isolating data within the reporting period...")
    isolated_dataframes = {}
    for df_name, df in dataframes.items():
        if date_column in df.columns:
            isolated_dataframes[df_name] = df[
                df[date_column].between(start_date, end_date)
            ]
        else:
            print(
                f"Warning: '{date_column}' column not found in '{df_name}' dataframe."
            )
            isolated_dataframes[df_name] = df
    return isolated_dataframes


def remove_trailing_spaces_from_values(dataframes_dict):
    """
    Removes trailing spaces from the values of all columns in each dataframe stored in a dictionary.

    :param dataframes_dict: A dictionary of pandas DataFrames.
    :return: A dictionary of pandas DataFrames with trailing spaces removed from the values of each column.
    """
    cleaned_dfs_dict = {}
    for key, df in dataframes_dict.items():
        for col in df.columns:
            if (
                df[col].dtype == "object"
            ):  # Check if the column is of object type (usually strings)
                # Use .loc to specify the rows and columns you're modifying
                df.loc[:, col] = df[col].apply(
                    lambda x: x.rstrip() if isinstance(x, str) else x
                )
        cleaned_dfs_dict[key] = df
    return cleaned_dfs_dict


def validate_data_files(dataframes, file_info):
    print("Validating data files...")
    for df_name, df in dataframes.items():
        if df_name in file_info:
            correct_columns = file_info[df_name]["columns"]
            print(f'> Checking {df_name} for {", ".join(correct_columns)}')
            if not set(correct_columns).issubset(df.columns):
                raise ValueError(
                    f"DataFrame {df_name} is missing one or more of the correct columns."
                )
    return dataframes



def filter_mib_services(dataframes):
    """
    Filters dataframes based on the following criteria:
    - If a dataframe's name starts with 'mib', it filters rows where 'service_type' matches the YIM providers.
    - If a dataframe's name does not start with 'mib', it includes:
        - All rows that are not franchise 'Inspiring neighborhoods'.
        - Rows of franchise 'Inspiring neighborhoods' with 'service_type' 'CYP'.

    :param dataframes: A dictionary of pandas DataFrames to filter.
    :param yim_providers: A list of YIM provider service types.
    :return: A dictionary of filtered pandas DataFrames.
    """
    print("Filtering MIB services...")
    filtered_dataframes = {}

    for df_name, df in dataframes.items():
        if df_name.lower().startswith('mib'):
            filtered_df = df
            filtered_dataframes[df_name] = filtered_df
            # Process dataframes whose names start with 'mib'
            # if 'contact_service_type' in df.columns and df_name in yim_providers:
            #     filtered_dataframes[df_name] = df[df["contact_service_type"].isin(yim_providers)]
            # else:
            #     filtered_dataframes[df_name] = df
        else:
        #     # If the required columns are not present, keep the dataframe as is
            filtered_df = df
            filtered_dataframes[df_name] = filtered_df

    return filtered_dataframes


def add_reason_to_file_closures(dataframes):

    """
    Merges the 'reason' column from a specified file closures DataFrame into a specified file closures goals DataFrame,
    and handles multiple client IDs with appropriate NaN filling.

    :param dataframes: A dictionary of pandas DataFrames.
    :param df_file_closures_name: The name of the DataFrame containing file closures.
    :param df_file_closures_goals_name: The name of the DataFrame containing file closures and goals.
    :return: A dictionary of pandas DataFrames with the merged 'reason' column.
    """
    df_file_closures_name = 'File_Closures_Within_Reporting_Period'
    df_file_closures_goals_name = 'File_Closures_And_Goals_Within_Reporting_Period'
    MIB_df_file_closures_goals_name = 'MIB_File_Closures_And_Goals_Within_Reporting_Period'
    
    filtered_dataframes = {}

    for df_name, df in dataframes.items():
        if df_name == df_file_closures_goals_name or df_name == MIB_df_file_closures_goals_name:
            # Check if the required DataFrame exists
            if df_file_closures_name not in dataframes:
                print(f"DataFrame '{df_file_closures_name}' not found.")
                continue

            df_file_closures = dataframes[df_file_closures_name]

            # Ensure 'client_id' is present in both DataFrames
            if 'client_id' not in df.columns or 'client_id' not in df_file_closures.columns:
                print("Both DataFrames must contain a 'client_id' column.")
                continue

            # Merge the two DataFrames on 'client_id'
            merged_df = pd.merge(df, df_file_closures[['client_id', 'reason']], 
                                 on='client_id', how='left')
            filtered_dataframes[df_name] = merged_df
        else:
            # Keep the dataframe as is if it's not the target dataframe
            filtered_dataframes[df_name] = df

    return filtered_dataframes
    # filtered_dataframes = {}

    # for df_name, df in dataframes.items():
    #     if df_name == df_file_closures_goals_name:
    #         # Check if the required DataFrame exists
    #         if df_file_closures_name not in dataframes:
    #             print(f"DataFrame '{df_file_closures_name}' not found.")
    #             continue

    #         df_file_closures = dataframes[df_file_closures_name]

    #         # Ensure 'client_id' is present in both DataFrames
    #         if 'client_id' not in df.columns or 'client_id' not in df_file_closures.columns:
    #             print("Both DataFrames must contain a 'client_id' column.")
    #             continue

    #         # Merge the two DataFrames on 'client_id'
    #         merged_df = pd.merge(df, df_file_closures[['client_id', 'reason']], 
    #                              on='client_id', how='left')
    #         filtered_dataframes[df_name] = merged_df
    #     else:
    #         # Keep the dataframe as is if it's not the target dataframe
    #         filtered_dataframes[df_name] = df

    # return filtered_dataframes