import sys
import os
import threading
import queue

import pandas as pd
import tkinter as tk
import re

from tkinter import filedialog
from tkinter import scrolledtext

# Add the directory of your script and modules to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import your local modules
from data_config import file_info, table_configs
from data_cleaning import (
    clean_column_names,
    remove_duplicates,
    remove_trailing_spaces_from_values,
    isolate_reporting_period,
    filter_mib_services,
    validate_data_files,
    add_reason_to_file_closures,
    isolate_client_ages
)
from QR_filters import filter_function_map, column_filter

from data_utils import (
    find_dict_by_table_name,
    calculate_percentage,
    calculate_average,
    calculate_count,
    calculate_percentage_as_number,
    calculate_row_average,
    calculate_row_total,
    calculate_percentage_row_total,
    is_percentage_row,
    is_average_row
    )


# Global queue for log messages
log_queue = queue.Queue()

def log_message(message):
    """Log a message to the Tkinter text widget."""
    log_queue.put(message)

def update_text_widget(log_queue, text_widget):
    """Update the text widget with log messages."""
    while True:
        message = log_queue.get()
        if message == "QUIT":
            break
        text_widget.configure(state='normal')
        text_widget.insert(tk.END, message + '\n')
        text_widget.configure(state='disabled')
        text_widget.yview(tk.END)

def create_logging_window():
    """Create the logging window."""
    root = tk.Tk()
    root.title("Logging Window")

    text_widget = scrolledtext.ScrolledText(root, state='disabled', height=20)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    threading.Thread(target=update_text_widget, args=(log_queue, text_widget), daemon=True).start()
    return root

def select_folder():
    # Create a root window, but keep it hidden
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog
    folder_path = filedialog.askdirectory()

    # Destroy the root window after selection
    root.destroy()

    return folder_path

def main():
    print("Begin Processing files")
    log_message("Begin Processing files")
    
    
    
    # Define reporting period parameters
    start_date, end_date = "2020-10-01", "2024-02-01"

    # Load and process data
    directory = (
        r"./quarterly_data_dump"
    )
    
    
    #directory = select_folder()

    # Data cleaning and validation
    try:
        raw_data = load_data_files(directory, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date)
        validated_data = validate_data_files(cleaned_data, file_info)
    except Exception as e:
        print(f"Error cleaning data: {e}")
        log_message(f"Error cleaning data: {e}")

        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


    # Produce and save tables
    output_df = produce_tables(validated_data)


    print("Report generated and saved as output_report.csv")
    return output_df
    

def load_data_files(directory, file_info):
    print("Loading data files...")
    dataframes = {}

    # Iterate through file_info and try to match with files in the directory
    for key, info in file_info.items():
        filename_start = info["filename"].split(".")[0]  # Get the start of the filename
        found = False

        for f in os.listdir(directory):
            if f.startswith(filename_start):
                full_path = os.path.join(directory, f)
                print(f"Attempting to load: {full_path}")
                try:
                    dataframes[key] = pd.read_csv(full_path)
                    print(f'> Loaded {key} from {f}')
                    found = True
                    break
                except Exception as e:
                    print(f"Error loading {full_path}: {e}")

        if not found:
            error_message = f"Error: Required file starting with '{filename_start}' not found in directory."
            print(error_message)
            log_message(error_message)
            sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error

    return dataframes


def clean_data(dataframes, start_date, end_date):
    print("Cleaning dataframes...")
    log_message("Cleaning dataframes...")
    cleaned_dataframes = clean_column_names(dataframes)
    cleaned_dataframes = isolate_client_ages(dataframes, 3, 26) 
    cleaned_dataframes = isolate_reporting_period(
    cleaned_dataframes, start_date, end_date)
    # cleaned_dataframes = filter_mib_services(cleaned_dataframes)
    cleaned_dataframes = remove_trailing_spaces_from_values(cleaned_dataframes)
    cleaned_dataframes = remove_duplicates(cleaned_dataframes)
    cleaned_dataframes = add_reason_to_file_closures(cleaned_dataframes)

    return cleaned_dataframes


def produce_tables(dataframes):
    print("Producing output tables...")
    log_message("Producing output tables...")

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

#   mylooplist = [list(filter_function_map.keys())[i] for i in [0, 18, 19, 20]]#,  19, 20]]

    
    # Append each table to the CSV file
    #for name in mylooplist:
    for name in filter_function_map.keys():
        print(f"Processing {name}")
        log_message(f"Processing {name}")
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
            log_message(f"No data to write for {name}")

    return combined_df




    
def filter_service_information(dataframes, config):
    print("Generating table...", config["table_name"])
    log_message(f"Generating service information table... {config['table_name']}")
    
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
                elif is_average_row(row):
                    assert isinstance(filtered_df, tuple), "Expected a tuple for percentage row"
                    new_row[column] = calculate_average(filtered_df)  # Calculate and add percentage
                    row_dataframes.append(filtered_df)
                else:
                    assert isinstance(filtered_df, pd.DataFrame), "Expected a DataFrame for count row"
                    new_row[column] = calculate_count(filtered_df)  # Calculate and add count
                    row_dataframes.append(filtered_df)

            except Exception as e:
                print(f"Error processing row: {row}, column: {column}, dfkey: {dataframe_key} Error: {e}")
                log_message(f"Error processing row: {row}, column: {column}, dfkey: {dataframe_key} Error: {e}")
                error_message = f"Error: {e}"
                new_row[column] = error_message  # Add the error message to the cell
                row_dataframes.append(None)  # Append None to maintain structure


        # Calculate total for the row
        if is_percentage_row(row):
            new_row["Q1_Totals"] = calculate_percentage_row_total(row_dataframes)
        elif is_average_row(row):
            new_row["Q1_Totals"] = calculate_row_average(row_dataframes)
        else:
            new_row["Q1_Totals"] = calculate_row_total(row_dataframes)

        # Create DataFrame for the row and append
        new_row_df = pd.DataFrame([new_row])
        result_df = pd.concat([result_df, new_row_df], ignore_index=True)

    return result_df






if __name__ == "__main__":
    resultdf = main()
    # logging_window = create_logging_window()
    # threading.Thread(target=main, daemon=True).start()
    # logging_window.mainloop()
