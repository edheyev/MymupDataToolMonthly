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
from data_config import file_info, table_configs, yim_providers, other_vcse
from data_cleaning import (
    clean_column_names,
    remove_duplicates,
    remove_trailing_spaces_from_values,
    isolate_reporting_period,
    validate_data_files,
    add_reason_to_contact,
    isolate_client_ages,
    remove_invalid_rows,
    filter_post_codes_add_craven,
    clean_dates
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
    load_data_files
)


# Global variables
log_queue = queue.Queue()
root = None
IS_HEADLESS = True  # Set to True for headless mode, False for GUI mode


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
        raw_data = load_data_files(folder_path, file_info, log_message=log_message)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        # Put cleaned data into the queue
        cleaned_data_queue.put(cleaned_data)
        log_message("Data loaded and cleaned.")
    except Exception as e:
        log_message(f"Error in data processing: {e}")


def main_gui():
    global root
    root, file_button, start_date_entry, end_date_entry = create_logging_window()
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())  # Proper shutdown on window close
    root.mainloop()

    try:
        # Wait and get cleaned data from the queue
        cleaned_data = cleaned_data_queue.get(timeout=30)  # Wait for 30 seconds
        # Proceed with validated data and other processing
        validated_data = validate_data_files(cleaned_data, file_info, log_message=log_message)

        # Define your franchise lists for each CSV
        yim_providers = [
            "Barnardos",
            "Bradford Youth Service (BYS)",
            "Brathay -MAGIC service type only",
            "INCIC -service type CYP only",
            "Mind in Bradford (MiB) service type Know Your Mind, Know Your Mind plus, Hospital Buddies BRI and Hospital Buddies AGH only",
            "SELFA"
        ]

        other_vcse = [
            "All Star Youth Entertainment",
            "Bradford Counselling Service",
            "Bradford Bereavement Support",
            "Family Action Bradford",
            "Roshnighar",
            "STEP 2",
            "The Cellar Trust"
        ]
        # Generate filenames based on the current date
        date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        file_string_1 = f"output_csv_QR_{date_str}_franchise_group_1.csv"
        file_string_2 = f"output_csv_QR_{date_str}_franchise_group_2.csv"
        
        date_range = start_date_entry, end_date_entry
        # Generate CSV files for each franchise list
        produce_tables(validated_data, file_string_1, yim_providers, date_range)
        log_message("CSV saved. File name: " + file_string_1)

        produce_tables(validated_data, file_string_2, other_vcse, date_range)
        log_message("CSV saved. File name: " + file_string_2)

        # Optionally update the GUI with completion status
        text_widget.insert(tk.END, "CSV files have been successfully generated.\n")

    except queue.Empty:
        log_message("Error: No cleaned data received within the timeout period.")
        text_widget.insert(tk.END, "Error: No cleaned data received within the timeout period.\n")
    except Exception as e:
        log_message(f"Unexpected error: {e}")
        text_widget.insert(tk.END, f"Unexpected error: {e}\n")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


def main_headless(directory, start_date, end_date):
    print("Running in headless mode...")
    print("Begin Processing files in directory:", directory)
    log_message("Begin Processing files")
    date_range = (start_date,end_date)

    try:
        raw_data = load_data_files(directory, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        validated_data = validate_data_files(cleaned_data, file_info, log_message=log_message)

        # File names for each franchise list
        file_string_1 = "output_csv_QR_franchise_YIM.csv"
        file_string_2 = "output_csv_QR_franchise_other_VCSE.csv"
        
        # Generate CSV files for each franchise list
        output_df_1 = produce_tables(validated_data, file_string_1, yim_providers, date_range)
        log_message("CSV saved. File name: " + file_string_1)
        
        output_df_2 = produce_tables(validated_data, file_string_2, other_vcse, date_range)
        log_message("CSV saved. File name: " + file_string_2)
        
        # Return both DataFrames if needed, or adjust return statement as required
        return output_df_1, output_df_2
        
    except Exception as e:
        log_message(f"Unexpected error: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error


def clean_data(dataframes, start_date, end_date, log_message=None):
    print(f"log_message is callable: {callable(log_message)}")

    if log_message and not callable(log_message):
        print("here")
        raise ValueError("log_message should be a callable function")

    try:
        print("Cleaning dataframes...")
        
        if log_message:
            log_message("Cleaning dataframes...")

        cleaned_dataframes = remove_invalid_rows(dataframes, log_message=log_message)

        cleaned_dataframes = clean_column_names(cleaned_dataframes, log_message=log_message)
        
        cleaned_dataframes = isolate_client_ages(cleaned_dataframes, yim_providers, log_message=log_message)
        
        cleaned_dataframes = filter_post_codes_add_craven(cleaned_dataframes, log_message)
        
        cleaned_dataframes = remove_duplicates(cleaned_dataframes, log_message=log_message)
        
        cleaned_dataframes = clean_dates(cleaned_dataframes, log_message=log_message)
        
        
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


def produce_tables(dataframes, file_string, franchise_list, date_range):
    print("Producing output tables...")
    log_message("Producing output tables...")

    last_sheet_name = None  # Initialize variable to track the last processed sheet name

    with open(file_string, "w", newline="") as f:
        for name in filter_function_map.keys():
            config = find_dict_by_table_name(name, table_configs)
            this_table = filter_service_information(dataframes, config, franchise_list, date_range)

            # Check if the sheet name has changed (or if it's the first table being processed)
            if config["sheet_name"] != last_sheet_name:
                # Print the sheet name if it's the first table in the sheet or if the sheet name has changed
                f.write(f"{config['sheet_name']}\n")
                last_sheet_name = config["sheet_name"]  # Update the last processed sheet name
            try:                
                # Write the table name on its own line
                f.write(f"{name}\n")
                
                if not this_table.empty:
                    # Iterate over DataFrame rows and columns to write the entire table
                    for index, row in this_table.iterrows():
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


def filter_service_information(dataframes, config, franchise_list, date_range):
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
            # Filter the dataframe by franchise before applying further processing
            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
            
            this_row_dataframe = this_row_dataframe[this_row_dataframe['franchise'].isin(franchise_list)]
            filtered_data = filter_func(this_row_dataframe, row, dfname=dataframe_key, date_range=date_range)

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


if __name__ == "__main__":
    if IS_HEADLESS:
        # Specify the directory and date range for headless mode
        directory_path = "./data"
        start_date = "2023-01-01"
        end_date = "2023-02-01"
        date_range = (start_date, end_date)
        main_headless(directory_path, start_date, end_date)
    else:
        main_gui()