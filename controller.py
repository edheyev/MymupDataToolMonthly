# controller.py

from data_utils import filter_by_indices, filter_by_isin

class DataController:
    def __init__(self, dataframe):
        self.df = dataframe

    def get_filtered_data_by_indices(self, indices):
        return filter_by_indices(self.df, indices)

    def get_filtered_data_by_isin(self, column_name, values):
        return filter_by_isin(self.df, column_name, values)

    def get_filtered_data_based_on_toggle(self, toggle_states, toggle_index):
        # Logic to determine how to filter based on toggle states
        if toggle_index == 3:  # For example, custom filter
            return self.get_filtered_data_by_isin('first_name', ['Burty', 'Claire'])
        
        # Filtering by indices logic
        selected_rows = []
        if toggle_states[0]:  # First three rows for the first toggle
            selected_rows.extend([0, 1, 2])
        if toggle_states[1]:
            selected_rows.append(1)
        if toggle_states[2]:
            selected_rows.append(2)

        return self.get_filtered_data_by_indices(selected_rows)
    def update_data(self, new_dataframe):
        # Perform any necessary preprocessing or validation here
        # For example, you might want to check if the new_dataframe is valid
        # or if it needs any cleaning or transformation.

        # Assuming new_dataframe is a pandas DataFrame and is ready to be used:
        self.dataframe = new_dataframe

        # If you have any observers or listeners that need to be notified
        # about the data update, notify them here.
        # For example, you might have a method to refresh the UI or a specific widget.