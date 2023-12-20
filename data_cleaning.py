import tkinter as tk
import pandas as pd
import data_utils as dp

def setup_window():
    window = tk.Tk()
    window.title("Data Cleaning Pipeline")

    # Create a scrollable Text widget
    text_widget = tk.Text(window, height=10, width=50)
    scrollbar = tk.Scrollbar(window, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    # Layout the Text widget and the Scrollbar in the window
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    return window, text_widget

def update_status(text_widget, status):
    text_widget.insert(tk.END, status + "\n")
    text_widget.see(tk.END)  # Auto-scrolls to the bottom

def main():
    window, text_widget = setup_window()

    file_names = ['MOCK_1.csv', 'MOCK_2.csv']
    for file_name in file_names:
        try:
            update_status(text_widget, f"Processing started for {file_name}")
           
            
            # Read the file
            df = pd.read_csv(f'./data/{file_name}')
            
            # Clean data
            cleaned_df = dp.clean_data(df)

            # Additional processing steps...
            # [Aggregation, Filtering, etc.]

            update_status(text_widget, f"Processing finished for {file_name}")

        except Exception as e:
            # Handle the error
            update_status(text_widget, f"Error in processing {file_name}: {e}")

    window.mainloop()

if __name__ == "__main__":
    main()
