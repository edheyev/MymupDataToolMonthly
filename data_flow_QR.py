import pandas as pd
from data_config import file_info
from QR_filters import column_filter, row_filter

def main():
    print("Begin Processing files")
    
    directory = "../../../quarterly_data_dump"
    raw_data = load_data_files(directory, file_info)
        
    # Define reporting period parameters
    start_date = '2020-04-01'
    end_date = '2020-06-30'
    date_column = 'date_of_contact'  # Replace with your specific date column name

    # Clean the data
    cleaned_data = clean_data(raw_data, start_date, end_date, date_column)
    
    # Validate data files
    validated_data = validate_data_files(cleaned_data, file_info)
    
    # Produce tables
    output_df = produce_tables(validated_data)
    
    # Write output to file
    output_df[0].to_csv("output_report.csv", index=False)
    
    print("Report generated and saved as output_report.csv")

    

def produce_tables(dataframes):
    """
    Produces output tables from the cleaned and validated data.

    :param dataframes: A dictionary of pandas DataFrames.
    :return: A pandas DataFrame representing the compiled report.
    """
    print("Producing output tables...")

    report_dfs = []
    
    OT_service_information = filter_service_information(dataframes)
    
    report_dfs.append(OT_service_information)
    
    return report_dfs


def filter_service_information(dataframes):
    """
    Generates service information table.

    :param dataframe: A pandas DataFrame to process.
    :return: A pandas DataFrame representing the report.
    """
    column_headings = ["Q1_Totals","Barnardos (Wrap)", "BYS All", "Brathay Magic", "INCIC (CYP)", "MIB Know Your Mind", "MIB Know Your Mind +", "MIB Hospital Buddys Airedale General", "MIB Hospital Buddys BRI", "SELFA (Mighty Minds)"]
    
    # Your row names
    row_names = ["Number of unique people supported (old rule)",
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
                 "% clients attended the first contact by video/face to face/telephone within 21 days of referral"]

    # Create an empty DataFrame with the specified rows and columns
    result_df = pd.DataFrame(index=row_names, columns=column_headings)
    
    mymuprow = [row_names[0], row_names[2], row_names[3]]  # Array of specific row names


    for row in row_names:
        for column in column_headings:
            if row in mymuprow:
                dataframe_key = None
                print("Error: No dataframe key for row:", row, "and column:", column)
                result_df.loc[row, column] = "MYMUP"  # Assign an error message or a default value
                continue  # Skip to the next iteration
                
            if row == row_names[0]:
            
                if column.startswith('MIB'):
                    dataframe_key = 'MIB_Referrals_Within_Reporting_Period'
                else: 
                    dataframe_key = 'Contacts_Or_Indirects_Within_Reporting_Period'
            elif row == row_names[1]:
            
                if column.startswith('MIB'):
                    dataframe_key = 'MIB_Referrals_Within_Reporting_Period'
                else: 
                    dataframe_key = 'Contacts_Or_Indirects_Within_Reporting_Period'
            elif  row == row_names[4]:
             
                if column.startswith('MIB'):
                    dataframe_key = 'MIB_file_closures_within_reporting_period'
                else: 
                    dataframe_key = 'file_closures_within_reporting_period'
            
            else:
                dataframe_key = None
                print("Error: No dataframe key for row:", row, "and column:", column)
                result_df.loc[row, column] = "error"  # Assign an error message or a default value
                continue  # Skip to the next iteration
                
            this_row_dataframe = dataframes.get(dataframe_key, pd.DataFrame())
            col_filtered_data = column_filter(this_row_dataframe, column)
            
            # Check if an error occurred in column_filter
            if 'error' in col_filtered_data.columns and col_filtered_data['error'].iloc[0]:
                result_df.loc[row, column] = "error"
                continue

            cell_output = row_filter(col_filtered_data, row)

            # Directly assign the result of row_filter to the cell
            result_df.loc[row, column] = cell_output


    return result_df

   
    
def load_data_files(directory, file_info):
    """
    Loads multiple CSV files from a specified directory into a dictionary of pandas DataFrames.

    :param directory: Path to the directory containing the CSV files.
    :param file_info: A dictionary where keys are descriptive names related to the table keys,
                      and values are dictionaries with filenames and columns.
    :return: A dictionary of pandas DataFrames.
    """
    print("Loading data files...")

    dataframes = {}
    for key, info in file_info.items():
        full_path = f"{directory}/{info['filename']}"
        try:
            dataframes[key] = pd.read_csv(full_path)
            print('>' + key)
        except Exception as e:
            print(f"Error loading {full_path}: {e}")
    return dataframes

def clean_data(dataframes, start_date, end_date, date_column):
    print("Cleaning dataframes...")
    cleaned_dataframes = clean_column_names(dataframes)
    cleaned_dataframes = remove_duplicates(cleaned_dataframes)
    #cleaned_dataframes = isolate_reporting_period(cleaned_dataframes, start_date, end_date, date_column)
    return cleaned_dataframes
    

    
def clean_column_names(dataframes):
    """
    Cleans column names in all dataframes: replaces spaces with underscores and converts to lowercase.

    :param dataframes: A dictionary of pandas DataFrames.
    :return: A dictionary of pandas DataFrames with cleaned column names.
    """
    print("standardising column names...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        df.columns = [col.replace(' ', '_').lower() for col in df.columns]
        cleaned_dataframes[df_name] = df
    return cleaned_dataframes

def remove_duplicates(dataframes):
    """
    Removes duplicate rows from all dataframes.

    :param dataframes: A dictionary of pandas DataFrames.
    :return: A dictionary of pandas DataFrames with duplicate rows removed.
    """
    print("removing duplicates...")
    cleaned_dataframes = {}
    for df_name, df in dataframes.items():
        cleaned_dataframes[df_name] = df.drop_duplicates()
    return cleaned_dataframes

def isolate_reporting_period(dataframes, start_date, end_date, date_column):
    print("Isolating data within the reporting period...")
    isolated_dataframes = {}
    for df_name, df in dataframes.items():
        if date_column in df.columns:
            isolated_dataframes[df_name] = df[df[date_column].between(start_date, end_date)]
        else:
            print(f"Warning: '{date_column}' column not found in '{df_name}' dataframe.")
            isolated_dataframes[df_name] = df
    return isolated_dataframes


def validate_data_files(dataframes, file_info):
    """
    Validates the data in the dataframes.

    :param dataframes: A dictionary of pandas DataFrames.
    :param file_info: A dictionary that maps each DataFrame name to its filename and correct columns.
    :return: A dictionary of pandas DataFrames.
    """
    print("Validating data files...")
    
    for df_name, df in dataframes.items():
        if df_name in file_info:
            correct_columns = file_info[df_name]["columns"]
            print('> checking ' + df_name + ' for ' + ', '.join(correct_columns)) 
            if not set(correct_columns).issubset(df.columns):
                raise ValueError(f"DataFrame {df_name} is missing one or more of the correct columns.")
            print("...ok")
    
    return dataframes



if __name__ == "__main__":
    main()
