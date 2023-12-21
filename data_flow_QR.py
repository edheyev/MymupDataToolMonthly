import pandas as pd
from data_config import file_info
from QR_filters import column_filter, SI_row_filter
import os


def main():
    print("Begin Processing files")

    # Load and process data
    # directory = r"../quarterly_data_dump"
    def main():
        print("Begin Processing files")

    # Load and process data
    directory = r"D:/OneDrive/Documents/src/python_testing/MyMupDataTool/quarterly_data_dump"
    raw_data = load_data_files(directory, file_info)

    # Define reporting period parameters
    start_date, end_date, date_column = "2020-04-01", "2020-06-30", "date_of_contact"

    # Data cleaning and validation
    cleaned_data = clean_data(raw_data, start_date, end_date, date_column)
    validated_data = validate_data_files(cleaned_data, file_info)

    # Produce and save tables
    output_df = produce_tables(validated_data)
    output_df[0].to_csv("output_report.csv", index=False)

    print("Report generated and saved as output_report.csv")


def load_data_files(directory, file_info):
    print("Loading data files...")
    dataframes = {}
    for key, info in file_info.items():
        full_path = os.path.join(directory, info["filename"])
        print(f"Attempting to load: {full_path}")  # Print the full path
        try:
            dataframes[key] = pd.read_csv(full_path)
            print(f'> Loaded {key} from {info["filename"]}')
        except Exception as e:
            print(f"Error loading {full_path}: {e}")
    return dataframes



def clean_data(dataframes, start_date, end_date, date_column):
    print("Cleaning dataframes...")
    cleaned_dataframes = clean_column_names(dataframes)
    cleaned_dataframes = remove_duplicates(cleaned_dataframes)
    # cleaned_dataframes = isolate_reporting_period(
        # cleaned_dataframes, start_date, end_date, date_column
    # )
    return cleaned_dataframes


def clean_column_names(dataframes):
    print("Standardizing column names...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        df.columns = [col.replace(" ", "_").lower() for col in df.columns]
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


def produce_tables(dataframes):
    print("Producing output tables...")
    report_dfs = []
    OT_service_information = filter_service_information(dataframes)
    report_dfs.append(OT_service_information)
    return report_dfs


def filter_service_information(dataframes):
    print("Generating service information table...")

    # Define your column headings and row names
    column_headings = [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ]
    row_names = [
        "Number of unique people supported (old rule)",
        "Number of unique people supported",
        "How many unique referrals",
        "How many new people referred",
        "How many were declined by the service?",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?",
        "Active cases",
        "How many people have moved on",
        "% clients with initial contact 5 days after referral (new rule)",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)",
        "% clients who had the first support session offered within 21 days of referral",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral",
    ]

    # Define rows that need placeholder text
    placeholder_rows = {
        "Number of unique people supported (old rule)": "MYMUP_URL",
        "How many unique referrals": "MYMUP_URL",
        "How many new people referred": "MYMUP_URL",
        "% clients with initial contact 5 days after referral (new rule)": "MYMUP_URL",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)": "MYMUP_URL",
        "% clients who had the first support session offered within 21 days of referral": "MYMUP_URL",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral": "MYMUP_URL",
        # Add other rows and their respective placeholders here
    }

    # Create an empty DataFrame
    result_df = pd.DataFrame(index=row_names, columns=column_headings)

    # Processing logic for each cell in the DataFrame
    for row in row_names:
        for column in column_headings:
            # Check if the row requires a placeholder
            if row in placeholder_rows:
                result_df.loc[row, column] = placeholder_rows[row]
                continue

            dataframe_key = get_dataframe_key(row, column)
            if dataframe_key is None:
                result_df.loc[row, column] = "error"
                continue

            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
            col_filtered_data = column_filter(this_row_dataframe, column, dfname=dataframe_key)

            if is_error_in_filter(col_filtered_data):
                result_df.loc[row, column] = "error"
                continue

            cell_output = SI_row_filter(col_filtered_data, row, dfname=dataframe_key)
            result_df.loc[row, column] = cell_output

    return result_df


def get_dataframe_key(row, column):
    if row in [
        "Number of unique people supported",
    ]:
        return (
            "MIB_Contacts_Or_Indirects_Within_Reporting_Period"
            if column.startswith("MIB")
            else "Contacts_Or_Indirects_Within_Reporting_Period"
        )
    elif row in [
        "How many young people disengaged, couldn’t be contacted or rejected a referral?", 
        "How many were declined by the service?",
        "How many people have moved on"
        ]:
        return (
            "file_closures_within_reporting_period"
        )
    elif row == "Active cases":
        return (
            "referrals_before_end_reporting_period"
        )
    else:
        return None


def is_error_in_filter(col_filtered_data):
    if "error" in col_filtered_data.columns and col_filtered_data["error"].iloc[0]:
        return True
    return False


if __name__ == "__main__":
    main()
