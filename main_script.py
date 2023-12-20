import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from pandastable import Table
from ttkthemes import ThemedTk
from controller import DataController

class DataProcessingToolGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Processing Tool")
        self.df = pd.DataFrame()
        self.controller = DataController(self.df, self.refresh_ui)

        self.setup_layout()
        self.create_button_frame()
        self.create_filter_frame()
        self.create_table_frame()
        self.create_log_window()

        self.log_message("Welcome to the Data Processing Tool!")


    def setup_layout(self):
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.grid(sticky='nsew', padx=5, pady=5)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)  # Changed columnconfigure to 0
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def create_button_frame(self):
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5) 

        self.load_csv_btn = ttk.Button(self.button_frame, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.grid(row=0, column=0, sticky='e', padx=5, pady=5)

        self.file_name_entry = ttk.Entry(self.button_frame, state='readonly')
        self.file_name_entry.grid(row=0, column=1, sticky='e', padx=5, pady=5)

        self.button_frame.columnconfigure(1, weight=1)

    
    def create_filter_frame(self):
        self.filter_frame = ttk.Frame(self.main_frame)
        self.filter_frame.grid(row=1, column=0, sticky='ns', padx=5, pady=5)  

        self.filter_vars = []
        self.filter_buttons = []  
        # Create filters 1 to 3
        for i in range(1, 4):
            filter_var = tk.BooleanVar()
            filter_check = ttk.Checkbutton(
                self.filter_frame, text=f'Filter {i}', variable=filter_var, state='disabled',
                command=lambda i=i: self.toggle_row_display(i-1)
            )
            filter_check.grid(row=i-1, column=0, sticky='w', padx=5, pady=2)
            self.filter_vars.append(filter_var)
            self.filter_buttons.append(filter_check)  # Store the widget

        # Adding the fourth filter for even IDs
        filter_var = tk.BooleanVar()
        filter_check = ttk.Checkbutton(
            self.filter_frame, text="Even ID Filter", variable=filter_var, state='disabled',
            command=lambda: self.toggle_row_display(3)  # Assuming this is the fourth filter
        )
        filter_check.grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.filter_vars.append(filter_var)
        self.filter_buttons.append(filter_check)  # Store the widget
        
    

        



    def create_table_frame(self):
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)  # Changed row to 0 and added rowspan
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)
        self.table = Table(self.table_frame, dataframe=self.df, showtoolbar=True, showstatusbar=True)
        self.table.show()

    def create_log_window(self):
        self.log_window = tk.Text(self.main_frame, height=4, state='disabled', bg='lightgray')
        self.log_window.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=5)


    def load_csv(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.df = pd.read_csv(file_path)
                self.controller.update_data(self.df)
                self.update_table_with_rows(self.df)
                
                # Display file name in the entry
                self.file_name_entry.config(state='normal')
                self.file_name_entry.delete(0, 'end')
                self.file_name_entry.insert(0, file_path.split('/')[-1])
                self.file_name_entry.config(state='readonly')
                
                # Enable the Checkbuttons
                for button in self.filter_buttons:
                    button.config(state='normal')

            self.log_message(f"CSV loaded: {file_path.split('/')[-1]}")
        except Exception as e:
            self.log_message(f"Error loading CSV: {e}")
            
    def log_message(self, message):
        self.log_window.config(state='normal')
        self.log_window.insert('end', message + '\n')
        self.log_window.config(state='disabled')
        self.log_window.see('end')
        
    def update_table_with_rows(self, dataframe):
        try:
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            if not dataframe.empty:
                self.table = Table(self.table_frame, dataframe=dataframe, showtoolbar=False, showstatusbar=False)
                self.table.show()
        except Exception as e:
            self.log_message(f"Error updating table: {e}")

    def toggle_row_display(self, toggle_index=None):
        try:
            # Reset all filters except the one that was just toggled
            for i, var in enumerate(self.filter_vars):
                if i != toggle_index:
                    var.set(False)

            # Find which filter is active
            active_filter_index = next((i for i, var in enumerate(self.filter_vars) if var.get()), None)
            
            # Log the action
            if active_filter_index is not None:
                self.log_message(f"Filter {active_filter_index + 1} applied.")
            else:
                self.log_message("All filters cleared.")

            # Filter the dataframe based on the active filter
            filtered_df = self.controller.get_filtered_data_based_on_toggle(active_filter_index)
            self.update_table_with_rows(filtered_df)

        except Exception as e:
            self.log_message(f"Error in toggle display: {e}")


    def refresh_ui(self):
        # Update the table with the new data
        self.update_table_with_rows(self.controller.df)

        # Disable all Checkbutton widgets
        for button in self.filter_buttons:
            button.config(state='disabled')

                
if __name__ == '__main__':
    root = ThemedTk(theme="arc")
    app = DataProcessingToolGUI(root)
    root.mainloop()