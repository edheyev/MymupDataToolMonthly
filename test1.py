import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """Loads data from a CSV file."""
    return pd.read_csv(file_path)

def get_unique_ids(df, column_name):
    """Extracts unique IDs from a specified column."""
    return set(df[column_name].unique())

def compare_ids(ids_7_days, ids_21_days):
    """Finds IDs in the 7-day set but not in the 21-day set."""
    return ids_7_days.difference(ids_21_days)

def plot_comparison(count_7_days, count_21_days, count_difference):
    """Plots a bar graph comparing the counts."""
    labels = ['7-Day Contacts', '21-Day Contacts', '7-Day Not in 21-Day']
    counts = [count_7_days, count_21_days, count_difference]

    plt.bar(labels, counts, color=['blue', 'green', 'red'])
    plt.ylabel('Count of Unique Client IDs')
    plt.title('Comparison of Client IDs in Different Contact Periods')
    plt.show()

# File paths
file_seven_days = "D:\OneDrive\Documents\src\python_testing\MyMupDataTool\quarterly_data_dump\contacts_within_twenty_one_days.csv"
file_twenty_one_days = "D:\OneDrive\Documents\src\python_testing\MyMupDataTool\quarterly_data_dump\contacts_within_seven_days.csv"

# Load datasets
df_7_days = load_data(file_seven_days)
df_21_days = load_data(file_twenty_one_days)

# Extract unique IDs
unique_ids_7_days = get_unique_ids(df_7_days, 'client_id')
unique_ids_21_days = get_unique_ids(df_21_days, 'client_id')

# Compare IDs
ids_not_in_21_days = compare_ids(unique_ids_7_days, unique_ids_21_days)
print(len(ids_not_in_21_days))

# Plotting the comparison
plot_comparison(len(unique_ids_7_days), len(unique_ids_21_days), len(ids_not_in_21_days))
