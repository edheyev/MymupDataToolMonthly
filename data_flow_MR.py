import sys
import os
import threading
import queue
import datetime
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
    validate_data_files,
    add_reason_to_contact,
    isolate_client_ages,
)
from MR_filters import filter_function_map

from data_utils import (
    find_dict_by_table_name,
    calculate_percentage,
    calculate_average,
    calculate_count,
    calculate_row_average,
    calculate_row_total,
    calculate_percentage_row_total,
    is_percentage_row,
    is_average_row,
)


# Global variables
log_queue = queue.Queue()
root = None

# Global queue for cleaned data
cleaned_data_queue = queue.Queue()


def log_message(message):
    """Log a message to the Tkinter text widget."""
    # print("l ", message)
    log_queue.put(message)


def update_text_widget(log_queue, text_widget):
    """Update the text widget with log messages."""
    while True:
        message = log_queue.get()
        if message == "QUIT":
            break
        text_widget.configure(state="normal")
        text_widget.insert(tk.END, message + "\n")
        text_widget.configure(state="disabled")
        text_widget.yview(tk.END)


def create_logging_window():
    global root
    root = tk.Tk()
    root.title("MyMup Data Tool: Quarterly Report")
    style = ttk.Style(root)
    style.theme_use(
        "clam"
    )  # 'clam', 'alt', 'default', 'classic' are some common themes

    # Instruction Frame
    instruction_frame = ttk.Frame(root, padding="10 10 10 10")
    instruction_frame.pack(fill=tk.X, expand=True)

    # Instruction Text
    instructions = (
        "Instructions for MyMup Data Tool:\n"
        "1. Enter correct dates in the format YYYY-MM-DD \n"
        "2. Select a folder containing all required data files for the quarterly report.\n"
        "3. Ensure the data files are named correctly as per the following list:\n"
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
        "Ensure the files match the specified column structure as detailed in the documentation. \n"
        "Press start when files are loaded and cleaned. \n"
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
    file_button = ttk.Button(
        button_frame,
        text="Select Containing Folder",
        command=lambda: select_folder(start_date_entry, end_date_entry, root),
    )
    file_button.pack(side=tk.LEFT, padx="10 10")

    start_button = ttk.Button(
        button_frame,
        text="Start Processing",
        command=lambda: start_processing(text_widget),
    )
    start_button.pack(side=tk.LEFT)

    # Log Frame
    log_frame = ttk.Frame(root, padding="10 10 10 10")
    log_frame.pack(fill=tk.BOTH, expand=True)

    # Text Widget for Logs
    text_widget = scrolledtext.ScrolledText(log_frame, state="disabled", height=20)
    text_widget.pack(fill=tk.BOTH, expand=True)

    threading.Thread(
        target=update_text_widget, args=(log_queue, text_widget), daemon=True
    ).start()

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
            threading.Thread(
                target=load_and_clean_data,
                args=(folder_path, start_date, end_date),
                daemon=True,
            ).start()
        except Exception as e:
            log_message(f"Error in data processing: {e}")


def load_and_clean_data(folder_path, start_date, end_date):
    try:
        raw_data = load_data_files(folder_path, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
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
#         validated_data = validate_data_files(
#             cleaned_data, file_info, log_message=log_message
#         )

#         # Format the date as DD-MM-YYYY
#         date_str = datetime.datetime.now().strftime("%d-%m-%Y")

#         # Start with a basic file name
#         file_string = f"output_csv_QR_{date_str}.csv"

#         # Initialize file counter
#         file_counter = 1

#         # Check if file already exists; if so, append a counter to the filename
#         if os.path.exists(os.path.join(directory, file_string)):
#             file_string = f"output_csv_QR_{date_str}_{file_counter}.csv"
#             while os.path.exists(os.path.join(directory, file_string)):
#                 file_counter += 1
#                 file_string = f"output_csv_QR_{date_str}_{file_counter}.csv"

#         output_df = produce_tables(validated_data, file_string)
#         log_message("CSV saved. File name: " + file_string)
#         return output_df
#     except queue.Empty:
#         log_message("Error: No cleaned data received within the timeout period.")
#         return None
#     except Exception as e:
#         log_message(f"Unexpected error: {e}")
#         sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


# uncomment for headless mode
def main(directory, start_date, end_date):
    print("Begin Processing files in directory:", directory)
    log_message("Begin Processing files")

    try:
        raw_data = load_data_files(directory, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        validated_data = validate_data_files(
            cleaned_data, file_info, log_message=log_message
        )
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
    
    # Check if the directory is empty
    if not os.listdir(directory):
        raise ValueError(f"The directory {directory} is empty")

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
                    print(f"> Loaded {key} from {f}")
                    found = True
                    break
                except Exception as e:
                    print(f"Error loading {full_path}: {e}")

        if not found:
            error_message = f"Error: Required file starting with '{filename_start}' not found in directory."
            print(error_message)
            print("error_message")
            log_message(error_message)
            sys.exit(
                1
            )  # Exit the program with a non-zero exit code to indicate an error

    return dataframes


def clean_data(dataframes, start_date, end_date, log_message=None):
    print(f"log_message is callable: {callable(log_message)}")

    if log_message and not callable(log_message):
        print("here")
        raise ValueError("log_message should be a callable function")

    try:
        print("Cleaning dataframes...")
        
        if log_message:
            log_message("Cleaning dataframes...")

        # Perform each cleaning step inside a try-except block
        cleaned_dataframes = clean_column_names(dataframes, log_message=log_message)
        
        cleaned_dataframes = isolate_client_ages(cleaned_dataframes, 3, 26, log_message=log_message)
        
        # cleaned_dataframes = isolate_reporting_period(
        #     cleaned_dataframes, start_date, end_date, log_message=log_message
        # )

    except Exception as e:
        error_message = f"An error occurred while cleaning dataframes: {e}"
        print(error_message)
        if log_message:
            log_message(error_message)
        raise  # Re-raise the exception after logging it

    return cleaned_dataframes

def produce_tables(dataframes, file_string):
    print("Producing output tables...")
    log_message("Producing output tables...")

    with open(file_string, "w", newline="") as f:
        for name in filter_function_map.keys():
            try:
                this_table = filter_service_information(dataframes, find_dict_by_table_name(name, table_configs))
                
                # Write the table name on its own line
                f.write(f"{name}\n")
                
                if not this_table.empty:
                    # Iterate over DataFrame rows and columns to write the entire table
                    for index, row in this_table.iterrows():
                        # Join all column values in a row into a single string separated by commas
                        row_str = ','.join(str(value) for value in row)
                        f.write(f"{row_str}\n")
                else:
                    print(f"No data to write for {name}")
                    log_message(f"No data to write for {name}")
                
                # Add a newline after the table has been added for separation
                f.write("\n")
                
            except Exception as e:
                log_message(f"Error processing filter for {name}: {e}")
                continue  # Skip to the next iteration if there's an error


def filter_service_information(dataframes, config):
    print("Generating table...", config["table_name"])
    log_message(f"Generating table... {config['table_name']}")

    row_names = config["row_names"]
    placeholder_rows = config.get("placeholder_text", {})
    default_db_key = config.get("row_db_default", "Default Logic")
    mib_default_db_key = config.get("mib_row_db_default", "MIB Default Logic")

    result_list = []
    filter_func = filter_function_map.get(config["table_name"])
    if not filter_func:
        raise ValueError(f"No filter function found for table {config['table_name']}")

    for row in row_names:
        try:
            if row in placeholder_rows:
                # Append placeholder text directly
                result_list.append({"Row Name": row, "Q1_Totals": placeholder_rows[row]})
                continue

            dataframe_key = default_db_key
            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
            filtered_data = filter_func(this_row_dataframe, row, dfname=dataframe_key)

            if isinstance(filtered_data, str):
                # If filtered_data is a string, append it directly
                result_list.append({"Row Name": row, "Q1_Totals": filtered_data})
            elif is_percentage_row(row):
                numerator, denominator = filtered_data
                percentage = calculate_percentage(numerator, denominator)
                result_list.append({"Row Name": row, "Q1_Totals": percentage})
            elif is_average_row(row):
                average = calculate_average(filtered_data)
                result_list.append({"Row Name": row, "Q1_Totals": average})
            else:
                # Assuming filtered_data is numerical data for counts
                count = calculate_count(filtered_data)
                result_list.append({"Row Name": row, "Q1_Totals": count})

        except Exception as e:
            print(f"Error processing row: {row}, dfkey: {dataframe_key} Error: {e}")
            log_message(f"Error processing row: {row}, dfkey: {dataframe_key} Error: {e}")
            result_list.append({"Row Name": row, "Q1_Totals": f"Error: {e}"})

    return pd.DataFrame(result_list)




# if __name__ == "__main__":
#     root, file_button, start_date_entry, end_date_entry = create_logging_window()
#     root.protocol(
#         "WM_DELETE_WINDOW", lambda: root.quit()
#     )  # Proper shutdown on window close
#     root.mainloop()

#     # uncomment for headless mode
if __name__ == "__main__":
    # Specify the directory and date range here
    directory_path = "./data"
    start_date = "2020-01-01"
    end_date = "2024-03-31"
    result = main(directory_path, start_date, end_date)
