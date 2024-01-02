import os
import pandas as pd
from data_config import file_info, service_info_config, table_configs
from data_cleaning import (
    clean_column_names,
    remove_duplicates,
    remove_trailing_spaces_from_values,
    validate_data_files,
    isolate_reporting_period,
    filter_mib_services
)
from QR_filters import (
    filter_function_map,
    column_filter,
)


def main():
    print("Begin Processing files")

    # Load and process data
    directory = (
        r"D:/OneDrive/Documents/src/python_testing/MyMupDataTool/quarterly_data_dump"
        # r"./quarterly_data_dump"
    )
    raw_data = load_data_files(directory, file_info)

    # TODO check that all necessary files are included !!

    # Define reporting period parameters
    start_date, end_date, date_column = "2020-04-01", "2020-06-30", "date_of_contact"

    # Data cleaning and validation
    cleaned_data = clean_data(raw_data, start_date, end_date, date_column)
    validated_data = validate_data_files(cleaned_data, file_info)

    # Produce and save tables
    produce_tables(validated_data)
    # output_df[0].to_csv("output_report.csv", index=False)

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
    cleaned_dataframes = filter_mib_services(cleaned_dataframes)
    cleaned_dataframes = remove_trailing_spaces_from_values(cleaned_dataframes)

    return cleaned_dataframes


def produce_tables(dataframes):
    print("Producing output tables...")

    report_dfs = []
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

    # Write the column headings to the CSV file
    with open("my_csv.csv", "w") as f:
        f.write(",".join(column_headings) + "\n")
    i = 0
    # Append each table to the CSV file
    for name in filter_function_map.keys():
        print(f"Processing {name}")
        thisconfig = find_dict_by_table_name(name, table_configs)
        this_table = filter_service_information(dataframes, thisconfig)

        # Check if DataFrame is not empty
        if not this_table.empty:
            # Write DataFrame without headers
            this_table.to_csv("my_csv.csv", mode="a", header=False, index=False)
            # Optionally, add an empty row or some separator after each table
            with open("my_csv.csv", "a") as f:
                f.write("\n")
        else:
            print(f"No data to write for {name}")
        if i == 4:
            break
        else:
            i = i+1
    return report_dfs


def find_dict_by_table_name(table_name, dict_array):
    for dictionary in dict_array:
        if dictionary.get("table_name") == table_name:
            return dictionary
    raise ValueError(
        f"Dictionary with table_name '{table_name}' not found in the array."
    )
    
    
def filter_service_information(dataframes, config):
    print("Generating service information table...", config["table_name"])
    
    row_names = config["row_names"]
    column_headings = config["column_headings"]
    placeholder_rows = config["placeholder_rows"]
    default_db_key = config.get('row_db_default', 'Default Logic')
    mib_default_db_key = config.get('mib_row_db_default', 'MIB Default Logic')

    result_df = pd.DataFrame(index=row_names, columns=column_headings)

    filter_func = filter_function_map.get(config["table_name"])
    if not filter_func:
        raise ValueError(f"No filter function found for table {config['table_name']}")

    for row in row_names:
        for column in column_headings:
            if column == "Q1_Totals":  # Skip the totals column for now
                continue
            if row in placeholder_rows:
                result_df.loc[row, column] = placeholder_rows[row]
                continue

            try:
                if column.startswith("MIB"):
                    dataframe_key = config["mib_row_db_logic"].get(row, mib_default_db_key)
                else:
                    dataframe_key = config["row_db_logic"].get(row, default_db_key)

                this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
                this_row_dataframe = column_filter(this_row_dataframe, column)
                cell_output = filter_func(this_row_dataframe, row, dfname=dataframe_key)
                result_df.loc[row, column] = cell_output
            except Exception as e:
                print(f"Error processing {row}, {column}: {e}")
                result_df.loc[row, column] = "error"


    for row in row_names:
        total = 0
        for col in column_headings:
            if col == "Q1_Totals":
                continue
            value = result_df.loc[row, col]
            # Convert value to numeric, non-numeric becomes NaN
            numeric_value = pd.to_numeric(value, errors='coerce')
            if numeric_value is not None and not pd.isna(numeric_value):
                total += numeric_value
        result_df.loc[row, "Q1_Totals"] = total

    return result_df




def is_error_in_filter(col_filtered_data):
    if "error" in col_filtered_data.columns and col_filtered_data["error"].iloc[0]:
        return True
    return False


if __name__ == "__main__":
    main()
