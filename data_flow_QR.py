import sys
import os
import threading
import queue
import re

import pandas as pd
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import scrolledtext
from tkinter import filedialog



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


# Global variables
log_queue = queue.Queue()
root = None

# Global queue for cleaned data
cleaned_data_queue = queue.Queue()

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
    global root
    root = tk.Tk()
    root.title("MyMup Data Tool: Quarterly Report")
    style = ttk.Style(root)
    style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' are some common themes

    # Instruction Frame
    instruction_frame = ttk.Frame(root, padding="10 10 10 10")
    instruction_frame.pack(fill=tk.X, expand=True)

    # Instruction Text
    instructions = (
        "Instructions for MyMup Data Tool:\n"
        "1. Select a folder containing all required data files for the quarterly report.\n"
        "2. Ensure the data files are named correctly as per the following list:\n"
        "   * Contacts or Indirects Within Reporting Period: 'contacts_or_indirects_within_reporting_period.csv'\n"
        "   * MIB Contacts or Indirects Within Reporting Period: 'mib_contacts_or_indirects_within_reporting_period.csv'\n"
        "   * File Closures And Goals Within Reporting Period: 'file_closures_and_goals_within_reporting_period.csv'\n"
        "   * MIB File Closures And Goals Within Reporting Period: 'mib_file_closures_and_goals_within_reporting_period.csv'\n"
        "   * File Closures Within Reporting Period: 'file_closures_within_reporting_period.csv'\n"
        "   * Initial Goals Within Reporting Period: 'initial_goals_within_reporting_period.csv'\n"
        "   * Referrals Within Reporting Period: 'referrals_within_reporting_period.csv'\n"
        "   * MIB Referrals Within Reporting Period: 'mib_referrals_within_reporting_period.csv'\n"
        "   * Referrals Before End Reporting Period: 'referrals_before_end_reporting_period.csv'\n"
        "   * MIB Referrals Before End Reporting Period: 'mib_referrals_before_end_of_reporting_period.csv'\n"
        "   * Contacts Within Seven Days: 'contacts_within_seven_days.csv'\n"
        "   * MIB Contacts Within Seven Days: 'mib_contacts_within_seven_days.csv'\n"
        "   * Contacts Within Twenty One Days: 'contacts_within_twenty_one_days.csv'\n"
        "   * MIB Contacts Within Twenty One Days: 'mib_contacts_within_twenty_one_days.csv'\n"
        "\nEnsure the files match the specified column structure as detailed in the documentation."
    )
    instruction_text = tk.Text(instruction_frame, height=10, wrap=tk.WORD)
    instruction_text.insert(tk.END, instructions)
    instruction_text.config(state=tk.DISABLED)  # Make text read-only
    instruction_text.pack(fill=tk.X, expand=True)

    # Input Frame
    input_frame = ttk.Frame(root, padding="10 10 10 10")
    input_frame.pack(fill=tk.X, expand=True)

    ttk.Label(input_frame, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT)
    start_date_entry = ttk.Entry(input_frame)
    start_date_entry.insert(0, "2020-10-01")
    start_date_entry.pack(side=tk.LEFT, padx="10 10")

    ttk.Label(input_frame, text="End Date (YYYY-MM-DD):").pack(side=tk.LEFT)
    end_date_entry = ttk.Entry(input_frame)
    end_date_entry.insert(0, "2024-02-01")
    end_date_entry.pack(side=tk.LEFT)

    # Button Frame
    button_frame = ttk.Frame(root, padding="10 10 10 10")
    button_frame.pack(fill=tk.X, expand=True)

    # File Selection and Start Processing Buttons
    file_button = ttk.Button(button_frame, text="Select Containing Folder", command=lambda: select_folder(start_date_entry, end_date_entry, root))
    file_button.pack(side=tk.LEFT, padx="10 10")

    start_button = ttk.Button(button_frame, text="Start Processing", command=lambda: start_processing(text_widget))
    start_button.pack(side=tk.LEFT)

    # Log Frame
    log_frame = ttk.Frame(root, padding="10 10 10 10")
    log_frame.pack(fill=tk.BOTH, expand=True)

    # Text Widget for Logs
    text_widget = scrolledtext.ScrolledText(log_frame, state='disabled', height=20)
    text_widget.pack(fill=tk.BOTH, expand=True)

    threading.Thread(target=update_text_widget, args=(log_queue, text_widget), daemon=True).start()

    return root, file_button, start_date_entry, end_date_entry



def start_processing(text_widget):
    """Function to start the main processing."""
    # You can now use the global variable `directory` to access the selected directory
    global directory
    threading.Thread(target=main, args=(directory, text_widget), daemon=True).start()



def select_folder(start_date_entry, end_date_entry, root):
    global directory
    # Create a root window, but keep it hidden
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    root.deiconify()  # Show the main window again
    
    directory = folder_path  # Set the global variable

    if folder_path:
        try:
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            log_message("Directory selected: " + directory)
            log_message(f"Start Date: {start_date}, End Date: {end_date}")
            threading.Thread(target=load_and_clean_data, args=(folder_path, start_date, end_date), daemon=True).start()
        except Exception as e:
            log_message(f"Error in data processing: {e}")
            
            
def load_and_clean_data(folder_path, start_date, end_date):
    try:
        raw_data = load_data_files(folder_path, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date)
        # Put cleaned data into the queue
        cleaned_data_queue.put(cleaned_data)
        log_message("Data loaded and cleaned.")
    except Exception as e:
        log_message(f"Error in data processing: {e}")

# def main(directory, text_widget):
#     global root
#     print("Begin Processing files")
#     log_message("Begin Processing files")
    
#     # Wait and get cleaned data from the queue
#     try:
#         cleaned_data = cleaned_data_queue.get(timeout=30)  # Wait for 30 seconds
#         # Proceed with validated data and other processing
#         validated_data = validate_data_files(cleaned_data, file_info, log_message=log_message)
#         file_string = "output_csv_QR.csv"
#         output_df = produce_tables(validated_data, file_string)
#         log_message("CSV saved. File name: " + file_string)
#         return output_df
#     except queue.Empty:
#         log_message("Error: No cleaned data received within the timeout period.")
#         return None
#     except Exception as e:
#         log_message(f"Unexpected error: {e}")
#         sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


def main(directory, start_date, end_date):
    print("Begin Processing files in directory:", directory)
    log_message("Begin Processing files")

    try:
        raw_data = load_data_files(directory, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date)
        validated_data = validate_data_files(cleaned_data, file_info, log_message=log_message)
        file_string = "output_csv_QR.csv"
        output_df = produce_tables(validated_data, file_string)
        log_message("CSV saved. File name: " + file_string)
        return output_df
    except Exception as e:
        log_message(f"Unexpected error: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error



def load_data_files(directory, file_info):
    print("Loading data files...")
    log_message("Loading data files...")
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
    cleaned_dataframes = clean_column_names(dataframes, log_message=log_message)
    cleaned_dataframes = isolate_client_ages(dataframes, 3, 26, log_message=log_message) 
    cleaned_dataframes = isolate_reporting_period(
    cleaned_dataframes, start_date, end_date, log_message=log_message)
    # cleaned_dataframes = filter_mib_services(cleaned_dataframes)
    cleaned_dataframes = remove_trailing_spaces_from_values(cleaned_dataframes, log_message=log_message)
    cleaned_dataframes = remove_duplicates(cleaned_dataframes, log_message=log_message)
    cleaned_dataframes = add_reason_to_file_closures(cleaned_dataframes, log_message=log_message)

    return cleaned_dataframes


def produce_tables(dataframes, file_string):
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
    with open(file_string, "w", newline='') as f:
        f.write(",".join(column_headings) + "\n")
        
    #optionally initialise empty df
    combined_df = pd.DataFrame(columns=column_headings)

#   mylooplist = [list(filter_function_map.keys())[i] for i in [0, 18, 19, 20]]#,  19, 20]]

    
    # Append each table to the CSV file
    #for name in mylooplist:
    for name in filter_function_map.keys():
        # print(f"Processing {name}")
        # log_message(f"Processing {name}")
        thisconfig = find_dict_by_table_name(name, table_configs)
        try:
            this_table = filter_service_information(dataframes, thisconfig)
        except Exception as e:
            log_message(f"Error processing filter: {e}")        
        # Check if DataFrame is not empty and write to csv
        if not this_table.empty:
            with open(file_string, "a", newline='') as f:
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
    log_message(f"Generating table... {config['table_name']}")
    
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
    # Specify the directory and date range here
    directory_path = "./quarterly_data_dump"
    start_date = "2023-01-01"
    end_date = "2023-03-31"
    main(directory_path, start_date, end_date)


# if __name__ == "__main__":
#     root, file_button, start_date_entry, end_date_entry = create_logging_window()
#     root.protocol("WM_DELETE_WINDOW", lambda: root.quit())  # Proper shutdown on window close
#     root.mainloop()