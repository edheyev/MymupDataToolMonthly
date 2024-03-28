import sys
import os
import threading
import queue
import datetime
import json

import pandas as pd
import tkinter as tk

# Add the directory of your script and modules to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import your local modules
from data_config import file_info, table_configs
from data_config import yim_providers as default_yim_providers, other_vcse as default_other_vcse

from data_cleaning import (
    clean_data,
    validate_data_files,
)

from MR_filters import filter_function_map

from data_utils import (
    find_dict_by_table_name,
    calculate_percentage,
    calculate_average,
    calculate_count,
    is_percentage_row,
    is_average_row,
    load_data_files,
)

from data_flowGUI import (
    create_logging_window,
    display_table_data,
    gui_log_message,
    update_table_data, 
)

CONFIG_FILE_PATH = "app_config.json"

# Global variables
log_queue = queue.Queue()
root = None
IS_HEADLESS = False  # Set to True for headless mode, False for GUI mode
# IS_HEADLESS = True  # Set to True for headless mode, False for GUI mode

# Global queue for cleaned data
cleaned_data_queue = queue.Queue()
queue_lock = threading.Lock()

def load_config(directory_path, config_file_path="config.json"):
    # Check if the config file exists
    config_file_path = directory_path + '/'+ config_file_path
    if not os.path.exists(config_file_path):
        # If the file doesn't exist, create it with the default values
        initial_config = {
            "yim_providers": default_yim_providers,
            "other_vcse": default_other_vcse
        }
        with open(config_file_path, "w") as config_file:
            json.dump(initial_config, config_file, indent=4)
        print(f"Config file created at {config_file_path} with default settings.")
        
    try:
    # Proceed to load the config file
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
        yim_providers = config.get("yim_providers", default_yim_providers)
        other_vcse = config.get("other_vcse", default_other_vcse)
        return yim_providers, other_vcse
    except json.JSONDecodeError:
        print("Error decoding JSON config. Using default configuration.")
    except Exception as e:
        print(f"Error loading configuration: {e}. Using default configuration.")
    
    # Return defaults if an error occurred during loading
    return default_yim_providers, default_other_vcse

def simple_test():
    print("Simple test function is running.")

def load_and_clean_data(folder_path, start_date, end_date):
    print("load start")
    try:
        raw_data = load_data_files(folder_path, file_info, log_message=log_message)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        # Put cleaned data into the queue
        cleaned_data_queue.put(cleaned_data)
        print("Cleaned data put in queue.")
        with queue_lock:
            log_message("Data loaded and cleaned.")
        

    except Exception as e:
        log_message(f"Error in data processing: {e}")
    print("Data loaded and cleaned.")  # Moved outside the try block


def start_processing(start_date_entry, end_date_entry, text_widget, directory):
    """Function to start the main processing."""
    print("start")
    threading.Thread(
        target=run_main_gui,
        args=(start_date_entry, end_date_entry, text_widget, directory, update_table_data),
        daemon=True,
    ).start()


def main_gui():
    global root
    root, file_button, start_date_entry, end_date_entry = create_logging_window(start_processing)
    root.protocol(
        "WM_DELETE_WINDOW", lambda: root.quit()
    )  # Proper shutdown on window close
    root.mainloop()


def log_message(message):
    """Log a message to the Tkinter text widget."""    
    gui_log_message(message, log_queue)

def run_main_gui(start_date_entry, end_date_entry, text_widget, directory, callback):
    try:
        
        gui_table_1 = []
        gui_table_2 = []
        print("main")
        yim_providers, other_vcse = load_config(directory)
        print("main2")
        date_range = start_date_entry.get(), end_date_entry.get()
        
        start_date, end_date = date_range
        
        
        raw_data = load_data_files(directory, file_info, log_message=log_message)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        # Put cleaned data into the queue
        cleaned_data_queue.put(cleaned_data)
        
        # Wait and get cleaned data from the queue
        with queue_lock:
            print("locked")
            cleaned_data = cleaned_data_queue.get(timeout=30)  # Wait for 30 seconds
        # Proceed with validated data and other processing
        print("hi2")
        validated_data = validate_data_files(
            cleaned_data, file_info, log_message=log_message
        )
        print("hasdi")
        
        
        # Generate filenames based on the current date
        date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        file_string_1 = f"output_csv_MR_{date_str}_YIM.csv"
        file_string_2 = f"output_csv_MR_{date_str}_OTHER.csv"

        
        # Generate CSV files for each franchise list
        gui_table_1 = produce_tables(validated_data, file_string_1, yim_providers, date_range)
        log_message("CSV saved. File name: " + file_string_1)

        gui_table_2 = produce_tables(validated_data, file_string_2, other_vcse, date_range)
        log_message("CSV saved. File name: " + file_string_2)

        # Optionally update the GUI with completion status
        text_widget.insert(tk.END, "CSV files have been successfully generated.\n")
        
        # display_table_data(gui_table_1)
        callback(gui_table_1, gui_table_2)
        
    except queue.Empty:
        log_message("Error: No cleaned data received within the timeout period.")
        text_widget.insert(
            tk.END, "Error: No cleaned data received within the timeout period.\n"
        )
    except Exception as e:
        log_message(f"Unexpected error: {e}")
        # text_widget.insert(tk.END, f"Unexpected error: {e}\n")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error

def main_headless(directory, start_date, end_date):
    print("Running in headless mode...")
    print("Begin Processing files in directory:", directory)
    log_message("Begin Processing files")
    date_range = (start_date, end_date)
    global yim_providers
    
    yim_providers, other_vcse = load_config(directory)
    try:
        raw_data = load_data_files(directory, file_info)
        cleaned_data = clean_data(raw_data, start_date, end_date, log_message)
        validated_data = validate_data_files(
            cleaned_data, file_info, log_message=log_message
        )

        # File names for each franchise list
        file_string_1 = "output_csv_QR_franchise_YIM.csv"
        file_string_2 = "output_csv_QR_franchise_other_VCSE.csv"

        # Generate CSV files for each franchise list
        output_df_2 = produce_tables(
            validated_data, file_string_2, other_vcse, date_range
        )
        log_message("CSV saved. File name: " + file_string_2)
        
        output_df_1 = produce_tables(
            validated_data, file_string_1, yim_providers, date_range
        )
        log_message("CSV saved. File name: " + file_string_1)


        # Return both DataFrames if needed, or adjust return statement as required
        return output_df_1, output_df_2

    except Exception as e:
        log_message(f"Unexpected error: {e}")
        sys.exit(1)  # Exit the program with a non-zero exit code to indicate an error

def produce_tables(dataframes, file_string, franchise_list, date_range):
    print("Producing output tables...")
    log_message("Producing output tables...")
    
    
    gui_table_data = []  # A list to hold data for GUI display
    
    last_sheet_name = None  # Initialize variable to track the last processed sheet name

    with open(file_string, "w", newline="") as f:
        for name in filter_function_map.keys():
            config = find_dict_by_table_name(name, table_configs)
            this_table = filter_service_information(
                dataframes, config, franchise_list, date_range
            )

            # Check if the sheet name has changed (or if it's the first table being processed)
            if config["sheet_name"] != last_sheet_name:
                # Print the sheet name if it's the first table in the sheet or if the sheet name has changed
                f.write(f"{config['sheet_name']}\n")
                last_sheet_name = config[
                    "sheet_name"
                ]  # Update the last processed sheet name
            try:
                # Write the table name on its own line
                f.write(f"{name}\n")

                if not this_table.empty:
                    # Iterate over DataFrame rows and columns to write the entire table
                    for index, row in this_table.iterrows():
                        row_dict = row.to_dict()
                        row_dict["filter_name"] = name  # Include filter name for reference
                        gui_table_data.append(row_dict)
                        row_str = ",".join(str(value) for value in row)
                        f.write(f"{row_str}\n")
                else:
                    print(f"No data to write for {name}")
                    log_message(f"No data to write for {name}")

                # Add a newline after the table has been added for separation
                f.write("\n")
        
            
            except Exception as e:
                log_message(f"Error processing filter for {name}: {e}")
                continue  # Skip to the next iteration if there's an error
    return gui_table_data

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

    #check in file_closures column to make sure that dates are within date range OR blank. 
    #do
    
    for row in row_names:
        try:
            if row in placeholder_rows:
                # Append placeholder text directly
                result_list.append(
                    {"Row Name": row, "Q1_Totals": placeholder_rows[row]}
                )
                continue
            if "row_db_logic" in config:
                if row in config["row_db_logic"]:
                    default_db_key = config["row_db_logic"][row]

            dataframe_key = default_db_key
            # Filter the dataframe by franchise before applying further processing
            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())

            this_row_dataframe = this_row_dataframe[
                this_row_dataframe["franchise"].isin(franchise_list)
            ]
            filtered_data = filter_func(
                this_row_dataframe, row, dfname=dataframe_key, date_range=date_range
            )

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
            log_message(
                f"Error processing row: {row}, dfkey: {dataframe_key} Error: {e}"
            )
            result_list.append({"Row Name": row, "Q1_Totals": f"Error: {e}"})

    return pd.DataFrame(result_list)


if __name__ == "__main__":
    if IS_HEADLESS:
        # Specify the directory and date range for headless mode
        directory_path = "./data"

        start_date = "2024-02-01"
        end_date = "2024-02-29"
        date_range = (start_date, end_date)
        main_headless(directory_path, start_date, end_date)
    else:
        main_gui()
