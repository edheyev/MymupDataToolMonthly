import os
import pandas as pd
from data_config import file_info, service_info_config
from data_cleaning import (
    clean_column_names,
    remove_duplicates,
    remove_trailing_spaces_from_values,
    validate_data_files,
    isolate_reporting_period,
)
from QR_filters import column_filter, SI_row_filter


def main():
    print("Begin Processing files")

    # Load and process data
    directory = (
        # r"D:/OneDrive/Documents/src/python_testing/MyMupDataTool/quarterly_data_dump"
        r"./quarterly_data_dump"
    )
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
    cleaned_dataframes = remove_trailing_spaces_from_values(cleaned_dataframes)

    return cleaned_dataframes


def produce_tables(dataframes):
    print("Producing output tables...")
    report_dfs = []
    OT_service_information = filter_service_information(dataframes)
    report_dfs.append(OT_service_information)
    return report_dfs


def filter_service_information(dataframes):
    print("Generating service information table...")
    config = service_info_config

    # Define your column headings and row names
    row_names = config["row_names"]
    column_headings = config["column_headings"]
    placeholder_rows = config[
        "placeholder_rows"
    ]  # Rows that require a placeholder value

    # Create an empty DataFrame
    result_df = pd.DataFrame(index=row_names, columns=column_headings)

    # Processing logic for each cell in the DataFrame
    for row in row_names:
        for column in column_headings:
            # Check if the row requires a placeholder
            if row in placeholder_rows:
                result_df.loc[row, column] = placeholder_rows[row]
                continue

            try:
                if column.startswith("MIB"):
                    dataframe_key = config["mib_row_db_logic"][row]
                else:
                    dataframe_key = config["row_db_logic"][row]

            except KeyError as e:
                print(f"Error in row_db_logic with row {row}: {e}")
                result_df.loc[row, column] = "error"
                continue

            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())

            col_filtered_data = column_filter(
                this_row_dataframe, column, dfname=dataframe_key
            )

            if is_error_in_filter(col_filtered_data):
                result_df.loc[row, column] = "error"
                continue

            cell_output = SI_row_filter(col_filtered_data, row, dfname=dataframe_key)
            result_df.loc[row, column] = cell_output

    return result_df


def is_error_in_filter(col_filtered_data):
    if "error" in col_filtered_data.columns and col_filtered_data["error"].iloc[0]:
        return True
    return False


if __name__ == "__main__":
    main()
