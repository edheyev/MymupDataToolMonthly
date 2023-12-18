# main_script.py

import tkinter as tk
from tkinter import filedialog, IntVar
import pandas as pd
from pandastable import Table
from data_utils import filter_dataframe  # Import the utility function
import sys
sys.path.insert(0, '/path/to/parent/directory/of/MyMupDataTool')
from controller import DataController


# ... (Other parts of the code remain the same)
def load_csv():
    global df, controller  # Include 'controller' as a global variable
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        controller = DataController(df)  # Initialize the controller here
        update_table_with_rows(pd.DataFrame())  # Pass an empty DataFrame initially


def update_table_with_rows(filtered_df):
    # Check if DataFrame is not empty
    if not filtered_df.empty:
        # Clear previous table display and show new data
        for widget in table_frame.winfo_children():
            widget.destroy()

        table = Table(table_frame, dataframe=filtered_df, showtoolbar=False, showstatusbar=False)
        table.show()
    else:
        # Clear the table if DataFrame is empty
        for widget in table_frame.winfo_children():
            widget.destroy()
        # Optionally, you can display a message or leave the frame empty

   
def toggle_row_display(toggle_index=None):
    global df, controller  # Ensure 'df' and 'controller' are recognized globally
    # Reset all toggles except the one just activated
    for i, var in enumerate(row_vars):
        if i != toggle_index:
            var.set(0)

    # Use controller to get filtered DataFrame
    toggle_states = [var.get() for var in row_vars]
    filtered_df = controller.get_filtered_data_based_on_toggle(toggle_states, toggle_index)

    # Update the table display
    update_table_with_rows(filtered_df)



# Set up the main window
window = tk.Tk()
window.title("Data Processing Tool")

# Main frame for layout management
main_frame = tk.Frame(window)
main_frame.pack(fill='both', expand=True)

# Frame for buttons and toggles
button_frame = tk.Frame(main_frame)
button_frame.pack(side='left', fill='y')

# Frame for pandastable
table_frame = tk.Frame(main_frame, width=500, height=200)
table_frame.pack(side='right', fill='both', expand=True)
table_frame.pack_propagate(False)

# Button to load CSV
load_csv_btn = tk.Button(button_frame, text="Load CSV", command=load_csv)
load_csv_btn.pack()

# Toggle buttons for rows and custom filter
row_vars = [IntVar() for _ in range(4)]  # Added one more for the custom filter
for i in range(3):
    chk = tk.Checkbutton(button_frame, text=f"Row {i+1}", variable=row_vars[i], 
                         command=lambda i=i: toggle_row_display(i))
    chk.pack()

# Custom filter check button
custom_filter_chk = tk.Checkbutton(button_frame, text="Filter by Name (Burty, Claire)", 
                                   variable=row_vars[3], command=lambda: toggle_row_display(3))
custom_filter_chk.pack()

# Start the GUI event loop
window.mainloop()
