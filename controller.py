# controller.py

from data_utils import filter_by_indices, filter_by_isin


class DataController:
    def __init__(self, dataframe, update_callback=None):
        self.df = dataframe
        self.update_callback = update_callback

    def get_filtered_data_based_on_toggle(self, toggle_index):
        if self.df.empty or "id" not in self.df.columns:
            raise ValueError("DataFrame is empty or does not have an 'id' column")

        # Check which toggle is active and apply the appropriate filter
        if toggle_index == 0:  # Filter 1: ID less than 5
            return self.df[self.df["id"] < 5]
        elif toggle_index == 1:  # Filter 2: First name is John or Jane
            return self.get_filtered_data_by_isin("first_name", ["John", "Jane"])
        elif toggle_index == 2:  # Filter 3: Email domain is example.com
            return self.df[self.df["email"].str.contains("google")]
        elif toggle_index == 3:  # Filter 4: for even IDs
            return self.df[self.df["id"] % 2 == 0]  # Assuming 'id' is a numeric column
        else:
            return (
                self.df
            )  # No filter selected, or an invalid index, return the original DataFrame

    def get_filtered_data_by_indices(self, indices):
        return filter_by_indices(self.df, indices)

    def get_filtered_data_by_isin(self, column_name, values):
        return filter_by_isin(self.df, column_name, values)

    def update_data(self, new_dataframe):
        # Perform any necessary preprocessing or validation here
        # For example, you might want to check if the new_dataframe is valid
        # or if it needs any cleaning or transformation.

        # Assuming new_dataframe is a pandas DataFrame and is ready to be used:
        self.df = new_dataframe

        # If you have any observers or listeners that need to be notified
        # about the data update, notify them here.

        # Call the update callback to refresh the UI
        if self.update_callback:
            self.update_callback()
