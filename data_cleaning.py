from data_config import yim_providers

def clean_column_names(dataframes):
    print("Standardizing column names...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        new_columns = []
        for col in df.columns:
            col = col.replace(" ", "_").lower()
            if col == "service_type":
                col = "contact_service_type"
            new_columns.append(col)
        df.columns = new_columns
        cleaned_dataframes[df_name] = df
    return cleaned_dataframes


def remove_duplicates(dataframes):
    print("Removing duplicates...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
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
            print("...ok")
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
            # Process dataframes whose names start with 'mib'
            if 'contact_service_type' in df.columns and df_name in yim_providers:
                filtered_dataframes[df_name] = df[df["contact_service_type"].isin(yim_providers)]
            else:
                filtered_dataframes[df_name] = df
        else:
        # # Process dataframes whose names do not start with 'mib'
        # if 'franchise' in df.columns and 'contact_service_type' in df.columns:
        #     # Include all rows except those where 'franchise' is 'Inspiring neighborhoods' and 'service_type' is not 'CYP'
        #     filtered_df = df[~((df["franchise"] == "Inspiring neighborhoods") & (df["contact_service_type"] != "CYP"))]
        # else:
        #     # If the required columns are not present, keep the dataframe as is
            filtered_df = df
            filtered_dataframes[df_name] = filtered_df

    return filtered_dataframes
