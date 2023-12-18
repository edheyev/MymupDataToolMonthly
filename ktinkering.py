import tkinter as tk
from tkinter import filedialog, IntVar
import pandas as pd
from pandastable import Table

def load_csv():
    global df  # Use global variable to store the DataFrame
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        update_table_with_rows([])  # Initially, no rows are displayed

def update_table_with_rows(rows_to_show, custom_filter=None):
    # Determine how to filter the DataFrame
    if custom_filter is not None:
        filtered_df = df[custom_filter]
    else:
        filtered_df = df.iloc[rows_to_show] if rows_to_show else pd.DataFrame()

    # Clear previous table display and show new data
    for widget in table_frame.winfo_children():
        widget.destroy()

    table = Table(table_frame, dataframe=filtered_df, showtoolbar=False, showstatusbar=False)
    table.show()
    
def toggle_row_display(toggle_index):
    # Reset all toggles except the one just activated
    for i, var in enumerate(row_vars):
        if i != toggle_index:
            var.set(0)

    # Determine which rows to show based on toggle states
    selected_rows = []
    custom_filter = None
    if toggle_index == 0 and row_vars[0].get() == 1:
        selected_rows.extend([0, 1, 2])  # First three rows for the first toggle
    elif toggle_index == 3 and row_vars[3].get() == 1:
        custom_filter = df['first_name'].isin(['Burty', 'Claire'])  # Custom filter for specific names
    elif row_vars[toggle_index].get() == 1:
        selected_rows.append(toggle_index)

    update_table_with_rows(selected_rows, custom_filter)

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
