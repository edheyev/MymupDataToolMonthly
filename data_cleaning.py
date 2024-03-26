# from data_config import yim_providers
import pandas as pd
import numpy as np
from data_config import craven_postcodes, yim_providers, other_vcse
from data_utils import isolate_date_range


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


# def remove_duplicates(dataframes, log_message=None):
#     print("removing duplicates")
#     if log_message:
#         log_message("Removing duplicates...")
#     else:
#         print("Removing duplicates...")
#     cleaned_dataframes = {}
#     for df_name, df in dataframes.items():
#         original_row_count = df.shape[0]
#         cleaned_df = df.drop_duplicates()
#         cleaned_dataframes[df_name] = cleaned_df
#         duplicates_removed = original_row_count - cleaned_df.shape[0]
#         if log_message:
#             print(f"Removed {duplicates_removed} duplicates from {df_name}.")
#             log_message(f"Removed {duplicates_removed} duplicates from {df_name}.")
#         else:
#             print(f"Removed {duplicates_removed} duplicates from {df_name}.")
#     return cleaned_dataframes

def remove_duplicates(dataframes, log_message=None):
    columns_to_ignore = ["file_closure", "referral_closure"]
    print("Removing duplicates...")
    if log_message:
        log_message("Removing duplicates...")

    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        original_row_count = df.shape[0]

        # Create a list of columns to consider for duplicate removal
        columns_to_consider = [
            col for col in df.columns if col not in columns_to_ignore
        ]

        # Use the `subset` parameter to ignore specified columns
        cleaned_df = df.drop_duplicates(subset=columns_to_consider)

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
            keep_rows = ((is_yim_provider & (df["age"] > 0) & (df["age"] < 26)) | 
             (~is_yim_provider & (df["age"] > 0) & (df["age"] < 19)))

            if "global_id" in df.columns:
                removal_ids.update(df[~keep_rows]["global_id"].unique())

            df_filtered = df[keep_rows].reset_index(drop=True)
            dataframes[df_name] = df_filtered

    for df_name, df in dataframes.items():
        if "global_id" in df.columns:
            df_final = df[~df["global_id"].isin(removal_ids)].reset_index(drop=True)
            dataframes[df_name] = df_final

    return dataframes


def clean_mib(dataframes, log_message=None):
    print("Isolating only correct MIB services")

    # Define allowed service types for Mind in Bradford
    allowed_service_types = [
        "Know Your Mind",
        "Know Your Mind Plus",
        "Hospital Buddies BRI",
        "Hospital Buddies AGH",
    ]

    # Container for global_id to keep for Mind in Bradford services
    global_id_to_keep = set()

    # First pass: Identify global_id to keep for Mind in Bradford
    for df_name, df in dataframes.items():
        if "franchise" in df.columns and "contact_service_type" in df.columns:
            print(df_name)
            # Filter for Mind in Bradford franchise and allowed service types
            allowed_rows = df[
                (df["franchise"] == "Mind in Bradford") & 
                df["contact_service_type"].isin(allowed_service_types)
            ]
            # Update set of global_id to keep
            global_id_to_keep.update(allowed_rows["global_id"].unique())
            if log_message:
                log_message(f"Identified global_id to keep in {df_name}.")
            else:
                print(f"Identified global_id to keep in {df_name}.")

    # Second pass: Apply filtering only to Mind in Bradford franchises
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        if "franchise" in df.columns:
            
            # where the datadump has the service type column do the filtering
            
            
            # Apply the global_id filter only to Mind in Bradford franchises
            if (df_name == "CYPMH_Contacts_All"):
                
                cleaned_df = df[
                    (df["franchise"] != "Mind in Bradford") | 
                    ((df["franchise"] == "Mind in Bradford") & (df["global_id"].isin(global_id_to_keep)))
                ]
            elif (df_name == "CYPMH_Two_Contacts"):
                not_mind_in_bradford_rows = df[df["franchise"] != "Mind in Bradford"]

                # Filter 'Mind in Bradford' rows that also meet the allowed service types criteria
                mind_in_bradford_allowed_rows = df[
                    (df["franchise"] == "Mind in Bradford") &
                    ((df["servicetype"].isin(allowed_service_types)) | 
                    (df["servicetype.1"].isin(allowed_service_types)))
                ]

                # Concatenate the two subsets to get the final DataFrame
                cleaned_df = pd.concat([not_mind_in_bradford_rows, mind_in_bradford_allowed_rows], ignore_index=True)

            else:
                cleaned_df = df
                
        
        else:
            # If franchise information is not available, leave the DataFrame unaltered
            cleaned_df = df

        cleaned_dataframes[df_name] = cleaned_df
        if log_message:
            log_message(f"Processed {df_name}.")
        else:
            print(f"Processed {df_name}.")

    return cleaned_dataframes



# def filter_post_codes_add_craven(dataframes, log_message=None):
#     print("Filtering postcodes and adding Craven column...")
#     if log_message:
#         log_message("Filtering postcodes and adding Craven column...")

#     # Initialization
#     removed_client_ids_due_to_no_postcode = set()
#     total_rows_before = 0
#     total_rows_after = 0
#     total_craven_marked = 0

#     # Sets for postcode prefixes
#     bradford_prefixes = {"BD1", "BD10", "BD11", "BD12", "BD13", "BD14", "BD15", "BD16", "BD17", "BD18", "BD2", "BD20", "BD21", "BD22", "BD23", "BD3", "BD4", "BD5", "BD6", "BD7", "BD8", "BD9", "BD98", "BD99", "HD6", "HX2", "HX3", "HX7", "LS12", "LS19", "LS20", "LS21", "LS28", "LS29"}
#     craven_prefixes = {"BD20", "LS29"}
#     craven_postcodes = {"BD208NJ", "LS27KT", "LS297UI"}


#     def extract_postcode_prefix(postcode):
#         # Convert any input to string and remove spaces
#         cleaned_postcode = ''.join(filter(str.isalnum, str(postcode).upper()))

#         # Determine the prefix based on the length after removing spaces
#         # For postcodes with 6 characters (without spaces), the prefix is the first 3 characters
#         # For postcodes with 7 characters (without spaces), the prefix is the first 4 characters
#         if len(cleaned_postcode) == 6:
#             return cleaned_postcode[:3]
#         elif len(cleaned_postcode) == 7:
#             return cleaned_postcode[:4]
#         else:
#             # Handle other lengths conservatively, defaulting to the first 3 characters
#             return cleaned_postcode[:3]


#     # Loop through each dataframe
#     for df_name, df in dataframes.items():
#         if 'post_code' in df.columns:
#             # Initial count
#             total_rows_before += len(df)

#             # Standardize and extract prefixes
#             df['postcode_prefix'] = df['post_code'].apply(extract_postcode_prefix)

#             # # Marking Craven
#             # df['craven'] = df['postcode_prefix'].isin(craven_prefixes)
#             # total_craven_marked += df['craven'].sum()

#             # Apply filtering
#             df_filtered = df[df['postcode_prefix'].isin(bradford_prefixes.union(craven_prefixes))]
#             total_rows_after += len(df_filtered)

#             # Update dataframe without the temporary column
#             df_final = df_filtered.drop(columns=['postcode_prefix'])
#             dataframes[df_name] = df_final

#     # Reporting
#     print(f"Total rows before filtering: {total_rows_before}, after filtering: {total_rows_after}, Craven marked: {total_craven_marked}")

#     if log_message:
#         log_message(f"Completed postcode filtering. Rows before: {total_rows_before}, after: {total_rows_after}, Craven marked: {total_craven_marked}")

#     return dataframes


def extract_postcode_prefix(postcode):
    # Convert any input to string and remove spaces
    cleaned_postcode = "".join(filter(str.isalnum, str(postcode).upper()))

    # Determine the prefix based on the length after removing spaces
    if len(cleaned_postcode) == 6:
        return cleaned_postcode[:3]
    elif len(cleaned_postcode) == 7:
        return cleaned_postcode[:4]
    else:
        # Handle other lengths conservatively, defaulting to the first 3 characters
        return cleaned_postcode[:3]


def filter_post_codes_add_craven(dataframes, log_message=None):
    print("Filtering postcodes and adding Craven column...")
    if log_message:
        log_message("Filtering postcodes and adding Craven column...")

    # Craven postcodes for exact matching
    craven_postcodes
    total_craven_marked = 0

    # Loop through each dataframe
    for df_name, df in dataframes.items():
        if "post_code" in df.columns:
            # Marking Craven based on exact matches
            df["craven"] = df["post_code"].apply(
                lambda x: "".join(filter(str.isalnum, x.upper())) in craven_postcodes
            )
            total_craven_marked += df["craven"].sum()

    print(f"Craven marked: {total_craven_marked}")
    if log_message:
        print(f"Completed Craven marking. Craven marked: {total_craven_marked}")
        log_message(f"Completed Craven marking. Craven marked: {total_craven_marked}")

    return dataframes


def add_rejected_referral_col_to_referral(dataframes, log_message=None):
    # if log_message:
    #     log_message("Adding referral_rejected column to CYMPH_Referrals...")

    # # Check if the key for rejected referrals exists
    # if "CYPMH_File_Closures_All" in dataframes:
    #     # Define a list of file closure reasons to filter on
    #     file_closure_reasons_to_check = ["Organisation rejects referral - Threshold too high", "Organisation rejects referral - Referral not suitable pre-assessment/post-assessment"]  # Add your desired reasons

    #     # Filter global IDs based on file closure reasons
    #     filtered_global_ids = set(
    #         dataframes["CYPMH_File_Closures_All"][
    #             dataframes["CYPMH_File_Closures_All"]["file_closure_reason"].isin(file_closure_reasons_to_check)
    #         ]["global_id"]
    #     )

    #     # Check if the key for referrals exists
    #     if "CYPMH_Referrals" in dataframes:
    #         # Add referral_rejected column based on whether global_id is in filtered_global_ids
    #         dataframes["CYPMH_Referrals"]["referral_rejected"] = dataframes[
    #             "CYPMH_Referrals"
    #         ]["global_id"].isin(filtered_global_ids)

    #         if log_message:
    #             log_message("referral_rejected column added successfully.")
    #     else:
    #         if log_message:
    #             log_message("CYPMH_Referrals not found in dataframes.")
    # else:
    #     if log_message:
    #         log_message("CYPMH_File_Closures_All not found in dataframes.")

    # return dataframes

    # Check if the key for rejected referrals exists
    if "CYPMH_Referral_Rejections_All" in dataframes:
        # Extract global_id for rejected referrals
        rejected_global_id = set(
            dataframes["CYPMH_Referral_Rejections_All"]["global_id"]
        )

        # Check if the key for referrals exists
        if "CYPMH_Referrals" in dataframes:
            # Add referral_rejected column based on whether global_id is in rejected_global_id
            dataframes["CYPMH_Referrals"]["referral_rejected"] = dataframes[
                "CYPMH_Referrals"
            ]["global_id"].isin(rejected_global_id)
            
            dataframes["CYPMH_File_Closures_All"]["referral_rejected"] = dataframes[
                "CYPMH_Referrals"
            ]["global_id"].isin(rejected_global_id)

            if log_message:
                log_message("referral_rejected column added successfully.")
        else:
            if log_message:
                log_message("CYMPH_Referrals not found in dataframes.")
    else:
        if log_message:
            log_message("CYPMH_Referral_Rejections_All not found in dataframes.")

    return dataframes


def bradford_postcode_filter_function(dataframes, log_message=None):
    # Initialization
    removed_global_id_due_to_no_postcode = set()
    total_rows_before = 0
    total_rows_after = 0

    # Sets for postcode prefixes
    bradford_prefixes = {
        "BD1",
        "BD10",
        "BD11",
        "BD12",
        "BD13",
        "BD14",
        "BD15",
        "BD16",
        "BD17",
        "BD18",
        "BD2",
        "BD20",
        "BD21",
        "BD22",
        "BD23",
        "BD24",
        "BD3",
        "BD4",
        "BD5",
        "BD6",
        "BD7",
        "BD8",
        "BD9",
        "BD98",
        "BD99",
        "HD6",
        "HX2",
        "HX3",
        "HX7",
        "LS12",
        "LS19",
        "LS20",
        "LS21",
        "LS28",
        "LS29",
    }

    # Loop through each dataframe for filtering with prefixes
    for df_name, df in dataframes.items():
        if "post_code" in df.columns:
            # Initial count
            total_rows_before += len(df)

            # Standardize and extract prefixes
            df["postcode_prefix"] = df["post_code"].apply(extract_postcode_prefix)

            # Apply filtering
            df_filtered = df[df["postcode_prefix"].isin(bradford_prefixes)]
            total_rows_after += len(df_filtered)

            # Update dataframe without the temporary column
            df_final = df_filtered.drop(columns=["postcode_prefix"])
            dataframes[df_name] = df_final

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


def filter_mib_services(dataframes, yim_providers, log_message=None):
    """
    Filters dataframes based on specified criteria and removes rows with 'global_id' found in any excluded rows
    across all dataframes.
    
    :param dataframes: A dictionary of pandas DataFrames to filter.
    :param yim_providers: A list of YIM provider service types.
    :param log_message: Optional; log message for additional information.
    :return: A dictionary of filtered pandas DataFrames.
    """
    print("Filtering MIB services...")
    excluded_global_ids = set()
    filtered_dataframes = {}

    # First pass: filter based on criteria and collect excluded 'global_id's
    for df_name, df in dataframes.items():
        if 'global_id' in df.columns:
            initial_count = len(df)
            if df_name.lower().startswith("mib"):
                # Assuming you need to include a condition for excluding based on 'service_type'
                if 'contact_service_type' in df.columns:
                    excluded_df = df[~df["contact_service_type"].isin(yim_providers)]
                    excluded_global_ids.update(excluded_df["global_id"])
                    filtered_df = df[df["contact_service_type"].isin(yim_providers)]
                else:
                    filtered_df = df
            else:
                # Add conditions for other dataframes if needed
                filtered_df = df  # Placeholder for actual filtering logic
                
            filtered_dataframes[df_name] = filtered_df
            if log_message and (len(df) - len(filtered_df) > 0):
                print(f"{log_message}: Excluded {initial_count - len(filtered_df)} rows from {df_name}")

    # Second pass: remove rows with 'global_id's that were excluded from any dataframe
    for df_name, df in filtered_dataframes.items():
        if 'global_id' in df.columns:
            df = df[~df["global_id"].isin(excluded_global_ids)]
            filtered_dataframes[df_name] = df

    return filtered_dataframes


def add_referred_this_reporting_period(dataframes, date_range, log_message=None):
    if "CYPMH_Referrals" in dataframes:
        # Isolate referrals within the date range
        isolated_df = isolate_date_range(
            dataframes["CYPMH_Referrals"], "referral_date", date_range
        )
        # Extract global_id for referrals within the date range
        referral_global_id = set(isolated_df["global_id"])

        # Loop through all dataframes
        for df_name, df in dataframes.items():
            # Add 'referred_in_date_range' column based on whether global_id is in global_id
            df["referred_in_date_range"] = df["global_id"].isin(referral_global_id)
            # Update the dataframe in the dictionary
            dataframes[df_name] = df

        if log_message:
            log_message(
                "Added 'referred_in_date_range' column to all dataframes based on CYPMH_Referrals within the specified date range."
            )
    else:
        if log_message:
            log_message(
                "CYPMH_Referrals dataframe not found in the provided dataframes dictionary."
            )

    return dataframes


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

# from dateutil.parser import parse

# import re

# def clean_date_column(df, column_name, df_name):
#     """
#     Cleans and standardizes the date column in the dataframe.
#     This includes handling cells with single or multiple date entries,
#     and ensuring that dates with a year of '0000' or other parsing errors are properly handled.
#     """
#     # Replace '', 'nan', and None with np.nan to clean the data
#     df[column_name] = df[column_name].replace({"": np.nan, "nan": np.nan, None: np.nan})

#     def is_valid_date(date_str):
#         # Check for the specific invalid format '0000-00-00' or similar
#         if date_str.startswith("0000"):
#             return False
#         return True
    
#     if column_name == "referral_date" and df_name == "CYPMH_Referrals":
#     # Replace '', 'nan', and None with np.nan to clean the data
#         df[column_name] = df[column_name].replace({"": np.nan, "nan": np.nan, None: np.nan})
        
#         # Directly convert dates to datetime format assuming "YYYY-MM-DD"
#         df[column_name] = pd.to_datetime(df[column_name], format="%Y-%m-%d", errors="coerce")

#         return df

#     def parse_dates(cell):
#         if pd.isna(cell) or not cell.strip():
#             return np.nan
        
#         # Split the cell on comma in case of multiple dates and filter out invalid dates
#         date_strings = filter(is_valid_date, cell.split(","))
#         latest_date = None

#         for date_str in date_strings:
#             try:
#                 current_date = parse(date_str.strip(), dayfirst=True).date()
#                 if latest_date is None or current_date > latest_date:
#                     latest_date = current_date
#             except (ValueError, OverflowError):
#                 # Skip any dates that cause parsing errors, including out-of-range errors
#                 continue

#         return latest_date

#     # Apply the parsing function to each cell in the column
#     df[column_name] = df[column_name].apply(parse_dates)
#     # Convert the date back into datetime format for consistency
#     df[column_name] = pd.to_datetime(df[column_name], errors="coerce")

#     return df


import pandas as pd
import numpy as np

def clean_date_column(df, column_name):
    """
    Cleans and standardizes the date column in the dataframe.
    This includes handling cells with single or multiple date entries,
    and ensuring that dates with parsing errors or out of valid range are properly handled and converted to NaT.
    """
    # Replace '', 'nan', and None with np.nan to clean the data
    df[column_name] = df[column_name].replace({"": np.nan, "nan": np.nan, None: np.nan})

    def parse_dates(cell):
        if pd.isna(cell) or not cell.strip():
            return np.nan

        try:
            parsed_date = pd.to_datetime(cell, errors='coerce')
            if parsed_date is not pd.NaT:
                return parsed_date.normalize()  # This removes the time component
            return np.nan
            # Return the parsed date or NaT if parsing failed
            return parsed_date if parsed_date is not pd.NaT else np.nan
        except (ValueError, OverflowError, pd.errors.OutOfBoundsDatetime):
            # Handle specific parsing errors including OutOfBoundsDatetime by returning NaT
            return np.nan

    # Apply the parsing function to each cell in the column
    df[column_name] = df[column_name].apply(parse_dates)

    return df

def clean_dates(dataframes, log_message=None):
    """
    Iterates over each dataframe and cleans specified date columns.
    """
    date_cols = [
        "referral_date",
        "first_contact_/_indirect_date",
        "second_contact_/_indirect_date",
        "file_closure",
        "file_closures",  # This column can have multiple dates
        "contact_date",
        "goal_date",
        "referral_rejections"
    ]

    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
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
