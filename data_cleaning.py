#from data_config import yim_providers
import pandas as pd

def clean_column_names(dataframes, log_message=None):
    print("Standardizing column names...")
    log_message("Standardizing column names...")
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


def remove_duplicates(dataframes, log_message=None):
    if log_message:
        log_message("Removing duplicates...")
    else:
        print("Removing duplicates...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        original_row_count = df.shape[0]
        cleaned_df = df.drop_duplicates()
        cleaned_dataframes[df_name] = cleaned_df
        duplicates_removed = original_row_count - cleaned_df.shape[0]
        if log_message:
            log_message(f"Removed {duplicates_removed} duplicates from {df_name}.")
        else:
            print(f"Removed {duplicates_removed} duplicates from {df_name}.")
    return cleaned_dataframes




def isolate_reporting_period(dataframes, start_date, end_date, log_message=None):
    print("Isolating data within the reporting period...")
    log_message("Isolating data within the reporting period...")

    # Convert start and end dates to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    for df_name, df in dataframes.items():
        # Check specific DataFrame and 'contact_date' column presence
        if df_name in ["Contacts_Or_Indirects_Within_Reporting_Period", "MIB_Contacts_Or_Indirects_Within_Reporting_Period"]:
            if 'contact_date' in df.columns:
                initial_row_count = len(df)
                print(f"Initial row count for '{df_name}': {initial_row_count}")
                log_message(f"Initial row count for '{df_name}': {initial_row_count}")
                # Convert 'contact_date' to datetime, coerce errors to NaT
                df['contact_date'] = pd.to_datetime(df['contact_date'], errors='coerce')
                
                # Drop rows with NaT in 'contact_date' and count them
                na_removed_count = df['contact_date'].isna().sum()
                df.dropna(subset=['contact_date'], inplace=True)
                print(f"Rows dropped due to NaT in 'contact_date' for '{df_name}': {na_removed_count}")
                log_message(f"Rows dropped due to NaT in 'contact_date' for '{df_name}': {na_removed_count}")
                # Filter data to include only rows within the reporting period
                filtered_df = df[(df['contact_date'] >= start_date) & (df['contact_date'] <= end_date)]
                period_filtered_count = initial_row_count - len(filtered_df)
                print(f"Rows filtered out of the reporting period for '{df_name}': {period_filtered_count}")
                log_message(f"Rows filtered out of the reporting period for '{df_name}': {period_filtered_count}")
                dataframes[df_name] = filtered_df

    return dataframes



def isolate_client_ages(dataframes, low_age, high_age, log_message=None):
    removed_client_ids = set()
    removed_count_first_pass = 0
    removed_count_second_pass = 0

    # First pass: Isolate ages and collect client_ids
    for df_name, df in dataframes.items():
        if 'client_age' in df.columns:
            # Find rows outside the age range
            outside_age_range = df[(df['client_age'] < low_age) | (df['client_age'] > high_age)]
            removed_count_first_pass += len(outside_age_range)
            
            # Collect client_ids
            removed_client_ids.update(outside_age_range['client_id'].unique())
            
            # Remove rows outside the age range
            dataframes[df_name] = df.drop(outside_age_range.index)

    # Second pass: Remove rows with matching client_ids in all dataframes
    for df_name, df in dataframes.items():
        if 'client_id' in df.columns:
            # Find rows with matching client_ids
            rows_to_remove = df[df['client_id'].isin(removed_client_ids)]
            removed_count_second_pass += len(rows_to_remove)
            
            # Remove these rows
            dataframes[df_name] = df.drop(rows_to_remove.index)

    print(f"Removed {removed_count_first_pass} rows based on age criteria.")
    log_message(f"Removed {removed_count_first_pass} rows based on age criteria.")
    print(f"Removed an additional {removed_count_second_pass} rows based on matching client_ids.")
    log_message(f"Removed an additional {removed_count_second_pass} rows based on matching client_ids.")
    return dataframes

    
    
    return dataframes

def remove_trailing_spaces_from_values(dataframes_dict, log_message=None):
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


def validate_data_files(dataframes, file_info, log_message=None):
    print("Validating data files...")
    log_message("Validating data files...")
    for df_name, df in dataframes.items():
        if df_name in file_info:
            required_columns = file_info[df_name]["columns"]
            print(f'> Validating {df_name} for required columns: {", ".join(required_columns)}')
            log_message(f'> Validating {df_name} for required columns: {", ".join(required_columns)}')
            # Identify missing columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                error_message = f"DataFrame '{df_name}' is missing the following required columns: {missing_columns_str}"
                log_message(error_message)
                raise ValueError(error_message)
    return dataframes




def filter_mib_services(dataframes, log_message=None):
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


# def add_reason_to_file_closures(dataframes, log_message=None):

#     """
#     Merges the 'reason' column from a specified file closures DataFrame into a specified file closures goals DataFrame,
#     and handles multiple client IDs with appropriate NaN filling.

#     :param dataframes: A dictionary of pandas DataFrames.
#     :param df_file_closures_name: The name of the DataFrame containing file closures.
#     :param df_file_closures_goals_name: The name of the DataFrame containing file closures and goals.
#     :return: A dictionary of pandas DataFrames with the merged 'reason' column.
#     """
#     df_file_closures_name = 'File_Closures_Within_Reporting_Period'
#     df_file_closures_goals_name = 'File_Closures_And_Goals_Within_Reporting_Period'
#     MIB_df_file_closures_goals_name = 'MIB_File_Closures_And_Goals_Within_Reporting_Period'
    
#     filtered_dataframes = {}

#     for df_name, df in dataframes.items():
#         if df_name == df_file_closures_goals_name or df_name == MIB_df_file_closures_goals_name:
#             # Check if the required DataFrame exists
#             if df_file_closures_name not in dataframes:
#                 print(f"DataFrame '{df_file_closures_name}' not found.")
#                 log_message(f"DataFrame '{df_file_closures_name}' not found.")
#                 continue

#             df_file_closures = dataframes[df_file_closures_name]

#             # Ensure 'client_id' is present in both DataFrames
#             if 'client_id' not in df.columns or 'client_id' not in df_file_closures.columns:
#                 print("Both DataFrames must contain a 'client_id' column.")
#                 log_message("Both file_closures  and file_closures and goals must contain a 'client_id' column.")
#                 continue

#             # Merge the two DataFrames on 'client_id'
#             merged_df = pd.merge(df, df_file_closures[['client_id', 'reason']], 
#                                  on='client_id', how='left')
#             filtered_dataframes[df_name] = merged_df
#         else:
#             # Keep the dataframe as is if it's not the target dataframe
#             filtered_dataframes[df_name] = df

#     return filtered_dataframes

def add_reason_to_file_closures(dataframes, log_message=None):
    print("Adding 'reason' column to file_closures and file_closures_and_goals...")
    try:
        df_file_closures_name = 'File_Closures_Within_Reporting_Period'
        df_file_closures_goals_name = 'File_Closures_And_Goals_Within_Reporting_Period'
        MIB_df_file_closures_goals_name = 'MIB_File_Closures_And_Goals_Within_Reporting_Period'
        
        filtered_dataframes = {}

        for df_name, df in dataframes.items():
            print(f"Processing DataFrame: {df_name}")  # Logging current DataFrame
            if df_name in [df_file_closures_goals_name, MIB_df_file_closures_goals_name]:
                # Check if the required DataFrame exists
                if df_file_closures_name not in dataframes:
                    print(f"DataFrame '{df_file_closures_name}' not found.")
                    if log_message:
                        log_message(f"DataFrame '{df_file_closures_name}' not found.")
                    continue

                df = df.copy()
                df_file_closures = dataframes[df_file_closures_name].copy()

                if 'client_id' not in df.columns or 'client_id' not in df_file_closures.columns or 'file_closure_date' not in df.columns or 'file_closure_date' not in df_file_closures.columns:
                    print("Both DataFrames must contain 'client_id' and 'file_closure_date' columns.")
                    if log_message:
                        log_message("Both file_closures and file_closures and goals must contain 'client_id' and 'file_closure_date' columns.")
                    continue

                df.loc[:, 'file_closure_date'] = pd.to_datetime(df['file_closure_date'])
                df_file_closures.loc[:, 'file_closure_date'] = pd.to_datetime(df_file_closures['file_closure_date'])

                merged_df = pd.merge(df, df_file_closures[['client_id', 'file_closure_date', 'reason']], 
                                     on=['client_id', 'file_closure_date'], how='left')
                filtered_dataframes[df_name] = merged_df
            else:
                filtered_dataframes[df_name] = df.copy()

        return filtered_dataframes

    except Exception as e:
        print(f"An error occurred: {e}")
        if log_message:
            log_message(f"An error occurred: {e}")
        return None


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