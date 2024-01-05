import sys
import os
import pandas as pd
from data_config import file_info, service_info_config, table_configs

from data_cleaning import (
    clean_column_names,
    remove_duplicates,
    remove_trailing_spaces_from_values,
    isolate_reporting_period,
    filter_mib_services,
    validate_data_files,
)
from QR_filters import (
    filter_function_map,
    column_filter,
)


#todo: make sure global filtering is good
# todo fix duplicate removal to only remove if date is also teh same

def main():
    print("Begin Processing files")
    
    # Define reporting period parameters
    start_date, end_date, date_column = "2020-04-01", "2020-06-30", "date_of_contact"

    # Load and process data
    directory = (
        r"D:/OneDrive/Documents/src/python_testing/MyMupDataTool/quarterly_data_dump"
        # r"./quarterly_data_dump"
    )
    raw_data = load_data_files(directory, file_info)

    # Data cleaning and validation
    try:
        cleaned_data = clean_data(raw_data, start_date, end_date, date_column)
        validated_data = validate_data_files(cleaned_data, file_info)
    except Exception as e:
        print(f"Error cleaning data: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


    # Produce and save tables
    output_df = produce_tables(validated_data)


    print("Report generated and saved as output_report.csv")
    return output_df


def load_data_files(directory, file_info):
    print("Loading data files...")
    dataframes = {}

    # Check if all files exist
    missing_files = []
    for key, info in file_info.items():
        full_path = os.path.join(directory, info["filename"])
        if not os.path.exists(full_path):
            missing_files.append(info["filename"])

    # If there are missing files, stop the function and report
    if missing_files:
        missing_files_str = ", ".join(missing_files)
        raise FileNotFoundError(f"The following required files are missing: {missing_files_str}")

    # If all files are present, proceed to load them
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
    # cleaned_dataframes = isolate_reporting_period(
    # cleaned_dataframes, start_date, end_date, date_column
    # )
    # cleaned_dataframes = filter_mib_services(cleaned_dataframes)
    # cleaned_dataframes = isolate_client_ages(3, 26) 
    cleaned_dataframes = remove_trailing_spaces_from_values(cleaned_dataframes)
    cleaned_dataframes = remove_duplicates(cleaned_dataframes)

    return cleaned_dataframes


def produce_tables(dataframes):
    print("Producing output tables...")

    column_headings = [
        "Row Name",
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

    # Write column headings to the CSV file
    with open("my_csv.csv", "w", newline='') as f:
        f.write(",".join(column_headings) + "\n")
        
    #optionally initialise empty df
    combined_df = pd.DataFrame(columns=column_headings)

    mylooplist = list(filter_function_map.keys())[24:25]
    
    # Append each table to the CSV file
    # for name in filter_function_map.keys():
    for name in mylooplist:
        print(f"Processing {name}")
        thisconfig = find_dict_by_table_name(name, table_configs)
        this_table = filter_service_information(dataframes, thisconfig)

        # Check if DataFrame is not empty and write to csv
        if not this_table.empty:
            with open("my_csv.csv", "a", newline='') as f:
                f.write(f"{name}\n")
                this_table.to_csv(f, header=False, index=False)
                f.write("\n")
                
            # Creating a row with the name and merging it with this_table
            name_row = pd.DataFrame([[name] + [None] * (len(column_headings) - 1)], columns=column_headings)
            combined_row = pd.concat([name_row, this_table], ignore_index=True)
            combined_df = pd.concat([combined_df, combined_row], ignore_index=True) 
        else:
            print(f"No data to write for {name}")

    return combined_df



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

    # Create the result DataFrame with the specified column headings
    result_df = pd.DataFrame(columns=["Row Name"] + column_headings)

    filter_func = filter_function_map.get(config["table_name"])
    if not filter_func:
        raise ValueError(f"No filter function found for table {config['table_name']}")

    # Loop through each row
    for row in row_names:
        new_row = {'Row Name': row}
        row_dataframes = []  # Store DataFrames or tuples of DataFrames for each row

        # Loop through each column
        for column in column_headings:
            if column == "Q1_Totals":
                continue
            if row in placeholder_rows:
                new_row[column] = placeholder_rows[row]
                row_dataframes.append(None)  # Add a marker for placeholder
                continue

            try:
                #overwrite df with exceptions if they exist in the config
                if column.startswith("MIB"):
                    dataframe_key = config["mib_row_db_logic"].get(row, mib_default_db_key)
                else:
                    dataframe_key = config["row_db_logic"].get(row, default_db_key)

                this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
                this_row_dataframe = column_filter(this_row_dataframe, column, dataframe_key)  # Apply column filter
                filtered_df = filter_func(this_row_dataframe, row, dfname=dataframe_key)

                if is_percentage_row(row):
                    assert isinstance(filtered_df, tuple), "Expected a tuple for percentage row"
                    numerator_df, denominator_df = filtered_df
                    new_row[column] = calculate_percentage(numerator_df, denominator_df)  # Calculate and add percentage
                    row_dataframes.append(filtered_df)
                else:
                    assert isinstance(filtered_df, pd.DataFrame), "Expected a DataFrame for count row"
                    new_row[column] = calculate_count(filtered_df)  # Calculate and add count
                    row_dataframes.append(filtered_df)

            except Exception as e:
                print(f"Error processing row: {row}, column: {column}, dfkey: {dataframe_key} Error: {e}")
                error_message = f"Error: {e}"
                new_row[column] = error_message  # Add the error message to the cell
                row_dataframes.append(None)  # Append None to maintain structure


        # Calculate total for the row
        if is_percentage_row(row):
            new_row["Q1_Totals"] = calculate_percentage_row_total(row_dataframes)
        else:
            new_row["Q1_Totals"] = calculate_row_total(row_dataframes)

        # Create DataFrame for the row and append
        new_row_df = pd.DataFrame([new_row])
        result_df = pd.concat([result_df, new_row_df], ignore_index=True)

    return result_df



def calculate_percentage(numerator_df, denominator_df):
    # Example: calculate a simple percentage
    numerator = len(numerator_df)
    denominator = len(denominator_df)

    if denominator == 0:
        return "0%"  # Avoid division by zero
    else:
        percentage = (numerator / denominator) * 100
        return f"{percentage:.2f}%"  # Format to two decimal places


def calculate_count(filtered_df):
    count = len(filtered_df)
    return count

def calculate_row_total(row_dataframes):
    # Sum up counts, skipping placeholders
    total = sum(len(df) for df in row_dataframes if isinstance(df, pd.DataFrame))
    return total

def calculate_percentage_row_total(row_dataframes):
    total_percentage = 0
    for cell in row_dataframes:
        if cell is None:
            continue  # Skip None values

        # Ensure that the cell is a tuple before unpacking
        if isinstance(cell, tuple):
            numerator_df, denominator_df = cell
            total_percentage += calculate_percentage_as_number(numerator_df, denominator_df)
        else:
            # Handle unexpected types or add a warning if necessary
            print(f"Unexpected type in row_dataframes: {type(cell)}")

    return f"{total_percentage:.2f}%"



def calculate_percentage_as_number(numerator_df, denominator_df):
    # Calculate percentage as a numeric value for summing
    numerator = len(numerator_df)
    denominator = len(denominator_df)

    if denominator == 0:
        return 0  # Avoid division by zero
    else:
        return (numerator / denominator) * 100


def is_percentage_row(row_name):
    return row_name.startswith('%') or row_name.startswith('average') or row_name.startswith('Percentage')




if __name__ == "__main__":
    resultdf = main()
