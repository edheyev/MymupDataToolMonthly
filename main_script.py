import tkinter as tk
from tkinter import ttk  # Corrected import for ttk
from tkinter import filedialog
import pandas as pd
from pandastable import Table
from data_utils import filter_dataframe
from controller import DataController
from ttkthemes import ThemedTk


class DataProcessingToolGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Processing Tool")
        self.df = pd.DataFrame()

        self.create_widgets()

    def create_widgets(self):
        # Main frame for layout management
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.grid(sticky='nsew')

        # Frame for buttons and toggles
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, sticky='ns')

        # Frame for displaying data (like a table)
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, sticky='nsew')

        # Configure the grid behavior in the main frame
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Add widgets to button_frame
        self.load_csv_btn = ttk.Button(self.button_frame, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.row_vars = [tk.IntVar() for _ in range(4)]
        for i in range(3):
            chk = ttk.Checkbutton(self.button_frame, text=f"Row {i+1}", variable=self.row_vars[i], command=lambda i=i: self.toggle_row_display(i))
            chk.grid(row=i+1, column=0, padx=10, pady=5, sticky='ew')

        self.custom_filter_chk = ttk.Checkbutton(self.button_frame, text="Filter by Name (Burty, Claire)", variable=self.row_vars[3], command=lambda: self.toggle_row_display(3))
        self.custom_filter_chk.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

        # Add widgets to table_frame
        # Assuming you have a pandas DataFrame named self.df
        self.table = Table(self.table_frame, dataframe=self.df)
        self.table.show()
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)



    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.controller = DataController(self.df)
            self.update_table_with_rows(pd.DataFrame())

    def update_table_with_rows(self, filtered_df):
        # Clear the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if not filtered_df.empty:
            table = Table(self.table_frame, dataframe=filtered_df, showtoolbar=False, showstatusbar=False)
            table.show()

    def toggle_row_display(self, toggle_index=None):
        # Reset all toggles except the one just activated
        for i, var in enumerate(self.row_vars):
            if i != toggle_index:
                var.set(0)

        # Filter data and update table
        toggle_states = [var.get() for var in self.row_vars]
        filtered_df = self.controller.get_filtered_data_based_on_toggle(toggle_states, toggle_index)
        self.update_table_with_rows(filtered_df)


if __name__ == '__main__':
    root = ThemedTk(theme="clam")
    app = DataProcessingToolGUI(root)
    root.mainloop()