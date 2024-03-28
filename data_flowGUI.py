import sys
import os
import threading
import queue
import datetime
import re
import json

import pandas as pd
import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import scrolledtext
from tkinter import filedialog

# from data_flow_MRR import log_message, start_processing, load_and_clean_data
import pandas as pd

def create_logging_window( start_processing):
    from data_flow_MRR import log_queue
    global root
    root = tk.Tk()
    root.title("MyMup Data Tool: Monthly Report")
    style = ttk.Style(root)
    style.theme_use("clam")

    # Change the background color of the Button
    style.configure('TButton', background='#E1E1E1', foreground='black', font=('Helvetica', 10))

    # Change the background and foreground colors of the Label
    style.configure('TLabel', background='#D3D3D3', foreground='blue', font=('Helvetica', 10))

    # Change the background color of the Frame
    style.configure('TFrame', background='#C1C1C1')

    # You can also change the style of specific widgets like entry fields, comboboxes, etc.
    style.configure('TEntry', foreground='black', background='#F0F0F0')

    # Example: Adjusting the Treeview widget
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview', background=[('selected', 'blue')])

    # Example: Adjust Scrollbar
    style.configure("Vertical.TScrollbar", gripcount=0,
                    background="gray", darkcolor="gray", lightcolor="gray",
                    troughcolor="gray", bordercolor="gray", arrowcolor="white")

    # Instruction Frame
    instruction_frame = ttk.Frame(root, padding="10 10 10 10")
    instruction_frame.pack(fill=tk.X, expand=True)

    # Instruction Text
    instructions = (
        "Instructions for MyMup Data Tool Monthly reporter:\n"
        "1. Enter correct dates in the format YYYY-MM-DD.\n"
        "2. Select a folder containing all required data files for the monthly report.\n"
        "3. Ensure the data files are named correctly as per the following list (numbers can be different):\n"
        "note that there maybe multiple of the same file type (2 or 3 if a MIB file is included.\n"
        "   * CYPMH Clients All: 'cypmh_clients_all_00000000.csv'\n"
        "   * CYPMH Contacts All: 'cypmh_contacts_all_00000000.csv'\n"
        "   * CYPMH File Closures All: 'cypmh_file_closures_all_00000000.csv'\n"
        "   * CYPMH Goal Themes All: 'cypmh_goal_themes_all_00000000.csv'\n"
        "   * CYPMH Plans And Goals All: 'cypmh_plans_and_goals_all_00000000.csv'\n"
        "   * CYPMH Referral Rejections All: 'cypmh_referral_rejections_all_00000000.csv'\n"
        "   * CYPMH Referrals: 'cypmh_referrals_00000000.csv'\n"
        "   * CYPMH Two Contacts: 'cypmh_two_contacts_00000000.csv'\n"
        "Ensure the files match the specified column structure as detailed in the documentation.\n"
        "Press start when files are loaded and cleaned.\n"
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
    start_date_entry.insert(0, "2024-01-01")
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
        command=lambda: start_processing(start_date_entry, end_date_entry, text_widget),
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



def select_folder(start_date_entry, end_date_entry, root):
    
    from data_flow_MRR import (load_and_clean_data,log_message)
    
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
            

def gui_log_message(message, log_queue):
    """Log a message to the Tkinter text widget."""
    log_queue.put(message)
    
    print(message)
            
def update_text_widget(log_queue, text_widget):
    def poll_log_queue():
        while not log_queue.empty():
            message = log_queue.get_nowait()
            text_widget.configure(state='normal')
            text_widget.insert(tk.END, message + "\n")
            text_widget.configure(state='disabled')
            text_widget.yview(tk.END)
        text_widget.after(100, poll_log_queue)  # Schedule this function to run again after 100ms
    
    poll_log_queue()