# from data_config import yim_providers
import pandas as pd
import numpy as np


def clean_column_names(dataframes, log_message=None):
    print("Standardizing column names...")
    log_message("Standardizing column names...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        new_columns = []
        for col in df.columns:
            col = col.replace(" ", "_").lower().strip("_")  # Added strip("_") here
            if col == "service_type":
                col = "contact_service_type"
            elif col == "userid":
                col = "client_id"
            elif col == "sen":
                col = "special_education_needs"
            elif col == "postcode":
                col = "post_code"
            new_columns.append(col)

        df.columns = new_columns
        cleaned_dataframes[df_name] = df
    return cleaned_dataframes


def remove_duplicates(dataframes, log_message=None):
    print("removing duplicates")
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
            print(f"Removed {duplicates_removed} duplicates from {df_name}.")
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
        if df_name in [
            "Contacts_Or_Indirects_Within_Reporting_Period",
            "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        ]:
            if "contact_date" in df.columns:
                initial_row_count = len(df)
                print(f"Initial row count for '{df_name}': {initial_row_count}")
                log_message(f"Initial row count for '{df_name}': {initial_row_count}")
                # Convert 'contact_date' to datetime, coerce errors to NaT
                df["contact_date"] = pd.to_datetime(df["contact_date"], errors="coerce")

                # Drop rows with NaT in 'contact_date' and count them
                na_removed_count = df["contact_date"].isna().sum()
                df.dropna(subset=["contact_date"], inplace=True)
                print(
                    f"Rows dropped due to NaT in 'contact_date' for '{df_name}': {na_removed_count}"
                )
                log_message(
                    f"Rows dropped due to NaT in 'contact_date' for '{df_name}': {na_removed_count}"
                )
                # Filter data to include only rows within the reporting period
                filtered_df = df[
                    (df["contact_date"] >= start_date)
                    & (df["contact_date"] <= end_date)
                ]
                period_filtered_count = initial_row_count - len(filtered_df)
                print(
                    f"Rows filtered out of the reporting period for '{df_name}': {period_filtered_count}"
                )
                log_message(
                    f"Rows filtered out of the reporting period for '{df_name}': {period_filtered_count}"
                )
                dataframes[df_name] = filtered_df

    return dataframes


def remove_invalid_rows(dataframes, log_message=None):
    # TODO
    return dataframes
    
def remove_duplicates(dataframes, log_message=None):
    columns_to_ignore = ['file_closure', 'referral_closure']
    print("Removing duplicates...")
    if log_message:
        log_message("Removing duplicates...")
    
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        original_row_count = df.shape[0]
        
        # Create a list of columns to consider for duplicate removal
        columns_to_consider = [col for col in df.columns if col not in columns_to_ignore]
        
        # Use the `subset` parameter to ignore specified columns
        cleaned_df = df.drop_duplicates(subset=columns_to_consider)
        
        cleaned_dataframes[df_name] = cleaned_df
        duplicates_removed = original_row_count - cleaned_df.shape[0]
        if log_message:
            log_message(f"Removed {duplicates_removed} duplicates from {df_name}.")
        else:
            print(f"Removed {duplicates_removed} duplicates from {df_name}.")
    
    return cleaned_dataframes

def isolate_client_ages(dataframes, yim_providers, log_message=None):
    """
    Removes clients from the dataframe that are not in the correct age categories.
    
    For entries from the yim_providers list in the 'franchise' column, removes ages 26 and up.
    For those that are not yim_providers, also removes ages 19-25.
    """
    removal_ids = set()

    print(f"isolating client ages...")
    for df_name, df in dataframes.items():
        if "age" in df.columns and "franchise" in df.columns:
            is_yim_provider = df["franchise"].isin(yim_providers)
            keep_rows = ((is_yim_provider & (df["age"] < 26)) | (~is_yim_provider & (df["age"] < 19)))

            removal_ids.update(df[~keep_rows]["client_id"].unique())

            df_filtered = df[keep_rows].reset_index(drop=True)
            dataframes[df_name] = df_filtered


    for df_name, df in dataframes.items():
        if "client_id" in df.columns:
            df_final = df[~df['client_id'].isin(removal_ids)].reset_index(drop=True)
            dataframes[df_name] = df_final

    return dataframes



# def isolate_client_ages(dataframes, yim_providers, log_message=None):
#     print("Isolating client ages...")
#     if log_message:
#         log_message("Isolating client ages...")
#     if log_message and not callable(log_message):
#         raise ValueError("log_message should be a callable function")

#     removed_client_ids = set()
#     removed_count_first_pass = 0

#     for df_name, df in dataframes.items():
#         if not isinstance(df, pd.DataFrame):
#             raise ValueError(f"The item {df_name} is not a pandas DataFrame.")

#         if "age" in df.columns and "client_id" in df.columns:
#             # Apply different removal criteria based on the 'franchise' column
#             try:
#                 # Conditions for YiM and non-YiM providers
#                 yim_condition = (df["age"] >= 26) & df["franchise"].isin(yim_providers)
#                 non_yim_condition = ((df["age"] >= 26) | ((df["age"] >= 19) & (df["age"] <= 25))) & ~df["franchise"].isin(yim_providers)
                
#                 # Identify rows to remove
#                 rows_to_remove = df[yim_condition | non_yim_condition]
#                 removed_count_first_pass += len(rows_to_remove)
                
#                 # Update set of client IDs to remove
#                 removed_client_ids.update(rows_to_remove["client_id"].unique())
                
#                 # Drop the identified rows
#                 dataframes[df_name] = df.drop(index=rows_to_remove.index).reset_index(drop=True)

#             except KeyError as e:
#                 if log_message:
#                     log_message(f"Column not found in {df_name}: {e}")
#                 continue  # Continue to next DataFrame if there's an error

#     # Second pass: remove all rows with client_ids marked for removal in any dataframe
#     removed_count_second_pass = 0
#     for df_name, df in dataframes.items():
#         if "client_id" in df.columns:
#             initial_len = len(df)
#             # Keep rows where 'client_id' is not in 'removed_client_ids'
#             dataframes[df_name] = df[~df["client_id"].isin(removed_client_ids)]
#             removed_count_second_pass += initial_len - len(dataframes[df_name])

#     if log_message:
#         log_message(f"Removed {removed_count_first_pass} rows based on age criteria.")
#         log_message(f"Removed an additional {removed_count_second_pass} rows based on matching client_ids.")
#         print(f"Removed {removed_count_first_pass} rows based on age criteria.")
#         print(f"Removed an additional {removed_count_second_pass} rows based on matching client_ids.")

#     return dataframes

def filter_post_codes_add_craven(dataframes, log_message=None):
    print("Filtering postcodes and adding Craven column...")
    if log_message:
        log_message("Filtering postcodes and adding Craven column...")
    
    # Initialization
    removed_client_ids_due_to_no_postcode = set()
    total_rows_before = 0
    total_rows_after = 0
    total_craven_marked = 0

    # Sets for postcode prefixes
    bradford_prefixes = {"BD1", "BD10", "BD11", "BD12", "BD13", "BD14", "BD15", "BD16", "BD17", "BD18", "BD2", "BD20", "BD21", "BD22", "BD23", "BD3", "BD4", "BD5", "BD6", "BD7", "BD8", "BD9", "BD98", "BD99", "HD6", "HX2", "HX3", "HX7", "LS12", "LS19", "LS20", "LS21", "LS28", "LS29"}
    craven_prefixes = {"BD20", "LS29"}

    def extract_postcode_prefix(postcode):
        # Convert any input to string and remove spaces
        cleaned_postcode = ''.join(filter(str.isalnum, str(postcode).upper()))
        
        # Determine the prefix based on the length after removing spaces
        # For postcodes with 6 characters (without spaces), the prefix is the first 3 characters
        # For postcodes with 7 characters (without spaces), the prefix is the first 4 characters
        if len(cleaned_postcode) == 6:
            return cleaned_postcode[:3]
        elif len(cleaned_postcode) == 7:
            return cleaned_postcode[:4]
        else:
            # Handle other lengths conservatively, defaulting to the first 3 characters
            return cleaned_postcode[:3]



    # Loop through each dataframe
    for df_name, df in dataframes.items():
        if 'post_code' in df.columns:
            # Initial count
            total_rows_before += len(df)

            # Standardize and extract prefixes
            df['postcode_prefix'] = df['post_code'].apply(extract_postcode_prefix)
            
            # Marking Craven
            df['craven'] = df['postcode_prefix'].isin(craven_prefixes)
            total_craven_marked += df['craven'].sum()

            # Apply filtering
            df_filtered = df[df['postcode_prefix'].isin(bradford_prefixes.union(craven_prefixes))]
            total_rows_after += len(df_filtered)

            # Update dataframe without the temporary column
            df_final = df_filtered.drop(columns=['postcode_prefix'])
            dataframes[df_name] = df_final

    # Reporting
    print(f"Total rows before filtering: {total_rows_before}, after filtering: {total_rows_after}, Craven marked: {total_craven_marked}")

    if log_message:
        log_message(f"Completed postcode filtering. Rows before: {total_rows_before}, after: {total_rows_after}, Craven marked: {total_craven_marked}")

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
            print(
                f'> Validating {df_name} for required columns: {", ".join(required_columns)}'
            )
            log_message(
                f'> Validating {df_name} for required columns: {", ".join(required_columns)}'
            )
            # Identify missing columns
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                missing_columns_str = ", ".join(missing_columns)
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
        if df_name.lower().startswith("mib"):
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


def add_reason_to_file_closures(dataframes, log_message=None):
    print("Adding 'reason' column to file_closures and file_closures_and_goals...")
    try:
        df_file_closures_name = "File_Closures_Within_Reporting_Period"
        df_file_closures_goals_name = "File_Closures_And_Goals_Within_Reporting_Period"
        MIB_df_file_closures_goals_name = (
            "MIB_File_Closures_And_Goals_Within_Reporting_Period"
        )

        filtered_dataframes = {}

        for df_name, df in dataframes.items():
            print(f"Processing DataFrame: {df_name}")  # Logging current DataFrame
            if df_name in [
                df_file_closures_goals_name,
                MIB_df_file_closures_goals_name,
            ]:
                # Check if the required DataFrame exists
                if df_file_closures_name not in dataframes:
                    print(f"DataFrame '{df_file_closures_name}' not found.")
                    if log_message:
                        log_message(f"DataFrame '{df_file_closures_name}' not found.")
                    continue

                df = df.copy()
                df_file_closures = dataframes[df_file_closures_name].copy()

                if (
                    "client_id" not in df.columns
                    or "client_id" not in df_file_closures.columns
                    or "file_closure_date" not in df.columns
                    or "file_closure_date" not in df_file_closures.columns
                ):
                    print(
                        "Both DataFrames must contain 'client_id' and 'file_closure_date' columns."
                    )
                    if log_message:
                        log_message(
                            "Both file_closures and file_closures and goals must contain 'client_id' and 'file_closure_date' columns."
                        )
                    continue

                df.loc[:, "file_closure_date"] = pd.to_datetime(df["file_closure_date"])
                df_file_closures.loc[:, "file_closure_date"] = pd.to_datetime(
                    df_file_closures["file_closure_date"]
                )

                merged_df = pd.merge(
                    df,
                    df_file_closures[["client_id", "file_closure_date", "reason"]],
                    on=["client_id", "file_closure_date"],
                    how="left",
                )
                filtered_dataframes[df_name] = merged_df
            else:
                filtered_dataframes[df_name] = df.copy()

        return filtered_dataframes

    except Exception as e:
        print(f"An error occurred: {e}")
        if log_message:
            log_message(f"An error occurred: {e}")
        return None


def clean_date_column(df, column_name):
    """
    Cleans and standardizes the date column in the dataframe.
    Attempts to parse various date formats into standardized datetime objects.
    """
    # Repgs, 'nan', and None with np.nan to clean the data
    df[column_name] = df[column_name].replace({'': np.nan, 'nan': np.nan, None: np.nan})

    # First attempt a vectorized conversion for the most common format
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce', dayfirst=True)

    return df


def clean_dates(dataframes, log_message=None):
    """
    Iterates over each dataframe and cleans specified date columns.

    Parameters:
    - dataframes: Dictionary of pandas dataframes to clean.
    - date_cols: List of column names containing dates to be standardized.
    - log_message: Optional logging function for messages.

    Returns:
    - A dictionary of cleaned dataframes.
    """
    date_cols = ["referral_date", "first_contact_/_indirect_date", "second_contact_/_indirect_date", "file_closure","contact_date", "goal_date"]

    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        print(f"{df_name} columns: {df.columns.tolist()}")
        if log_message:
            log_message(f"Cleaning dates in {df_name}...")
        else:
            print(f"Cleaning dates in {df_name}...")

        for col in date_cols:
            if col in df.columns:
                df = clean_date_column(df, col)

        cleaned_dataframes[df_name] = df

    return cleaned_dataframes


    
    

def add_reason_to_contact(dataframes, log_message=None):
    print("Adding 'file_closure_reason' to specified DataFrames...")
    try:
        df_file_closures_goals_name = "File_Closures_And_Goals_Within_Reporting_Period"
        target_dfs = [
            "Contacts_Within_Twenty_One_Days",
            "MIB_Contacts_Within_Twenty_One_Days",
            "Contacts_Within_Seven_Days",
            "MIB_Contacts_Within_Seven_Days",
        ]

        filtered_dataframes = {}

        if df_file_closures_goals_name not in dataframes:
            print(f"DataFrame '{df_file_closures_goals_name}' not found.")
            if log_message:
                log_message(f"DataFrame '{df_file_closures_goals_name}' not found.")
            return None

        # Preprocess 'File_Closures_And_Goals_Within_Reporting_Period' DataFrame
        df_file_closures_goals = dataframes[df_file_closures_goals_name].copy()
        df_file_closures_goals["client_id"] = pd.to_numeric(
            df_file_closures_goals["client_id"], errors="coerce"
        )
        df_file_closures_goals["file_closure_date"] = pd.to_datetime(
            df_file_closures_goals["file_closure_date"]
        )

        for df_name, df in dataframes.items():
            print(f"Processing DataFrame: {df_name}")  # Logging current DataFrame
            if df_name in target_dfs:
                df = df.copy()
                df["client_id"] = pd.to_numeric(df["client_id"], errors="coerce")

                if (
                    "client_id" not in df.columns
                    or "file_closure_date" not in df.columns
                ):
                    print(
                        f"DataFrame '{df_name}' must contain 'client_id' and 'file_closure_date' columns."
                    )
                    if log_message:
                        log_message(
                            f"DataFrame '{df_name}' must contain 'client_id' and 'file_closure_date' columns."
                        )
                    continue

                df["file_closure_date"] = pd.to_datetime(df["file_closure_date"])

                # Merging with 'file_closure_reason'
                merged_df = pd.merge(
                    df,
                    df_file_closures_goals[
                        ["client_id", "file_closure_date", "file_closure_reason"]
                    ],
                    on=["client_id", "file_closure_date"],
                    how="left",
                )
                filtered_dataframes[df_name] = merged_df
            else:
                filtered_dataframes[df_name] = df

        return filtered_dataframes

    except Exception as e:
        print(f"An error occurred: {e}")
        if log_message:
            log_message(f"An error occurred: {e}")
        return None
