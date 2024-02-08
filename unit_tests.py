import unittest
import pandas as pd
import numpy as np

from data_cleaning import clean_column_names,isolate_client_ages, filter_post_codes_add_craven
from data_flow_MR import log_message

class TestDataCleaningFunctions(unittest.TestCase):
    def test_clean_column_names(self):
        # Sample DataFrame
        df = pd.DataFrame(columns=['UserID', ' Service Type ', 'File Closure'])
        dataframes = {'test_df': df}

        # Expected result
        expected_columns = ['client_id', 'contact_service_type', 'file_closure']

        # Run the function
        cleaned_dataframes = clean_column_names(dataframes, log_message=log_message)

        # Assert
        self.assertListEqual(list(cleaned_dataframes['test_df'].columns), expected_columns)



class TestFilterPostCodesAddCraven(unittest.TestCase):
    def setUp(self):
        # Sample data setup
        self.dataframes = {
            'test_df': pd.DataFrame({
                'client_id': [1, 2, 3, 4, 5, 6,7,8],
                'post_code': ['BD1 2RE', 'LS29 8JQ', 'BD20 7RT', 'HX3 5AX', 'ZZ99 9ZZ', 'ZZ999ZZ', 'BD19ZZ', np.nan],
                'data': ['a', 'b', 'c', 'd', 'e', 'f','g','h']
            })
        }
        # Expected Bradford and Craven postcodes
        self.expected_bradford_craven_postcodes = {'BD1', 'LS29', 'BD20', 'HX3', 'BD1'}

    def test_filter_post_codes_add_craven(self):
        # Applying the filter function
        filtered_dataframes = filter_post_codes_add_craven(self.dataframes)
        
        # Verify rows are correctly filtered and marked
        df = filtered_dataframes['test_df']
        
        # Assert the correct number of rows remain
        self.assertEqual(len(df), 5)  # Adjusted to match the actual expected number of valid postcodes
        
        # Assert correct marking of Craven
        self.assertTrue(all(df[df['post_code'].str.startswith('BD20') | df['post_code'].str.startswith('LS29')]['craven']))
        
        # Assert only valid postcodes remain
        postcodes_processed = set(df['post_code'].str.replace(" ", "").apply(lambda x: x[:4] if len(x) > 6 else x[:3]))
        self.assertTrue(postcodes_processed.issubset(self.expected_bradford_craven_postcodes))

    # You can add more test cases for other scenarios, such as handling empty DataFrames,
    # DataFrames without 'post_code' or 'client_id' columns, etc.

class TestIsolateClientAges(unittest.TestCase):
    def setUp(self):
        # Sample data setup with age and franchise columns
        self.dataframes = {
            'df1': pd.DataFrame({
                'client_id': [1, 2, 3, 4],
                'age': [25, 26, 18, 19],
                'franchise': ['YiM', 'YiM', 'Non-YiM', 'Non-YiM']
            }),
            'df2': pd.DataFrame({
                'client_id': [5, 6],
                'age': [27, 18],
                'franchise': ['Non-YiM', 'YiM']
            })
        }
        # Define YiM providers list
        self.yim_providers = ['YiM']

    def test_isolate_client_ages(self):
        # Expected DataFrame after filtering
        expected_df1 = pd.DataFrame({
            'client_id': [1, 3],  # Expected to remove client_id 1 due to age >= 26 and YiM provider
            'age': [25, 18],
            'franchise': ['YiM', 'Non-YiM']
        }).reset_index(drop=True)

        expected_df2 = pd.DataFrame({
            'client_id': [6],  # Expected to remove client_id 5 due to age >= 26 and Non-YiM provider
            'age': [18],
            'franchise': ['YiM']
        }).reset_index(drop=True)

        # Run the isolate_client_ages function with the sample data and YiM providers list
        result_dataframes = isolate_client_ages(self.dataframes, self.yim_providers)

        # Verify the result matches the expected output
        pd.testing.assert_frame_equal(result_dataframes['df1'], expected_df1, check_dtype=False)
        pd.testing.assert_frame_equal(result_dataframes['df2'], expected_df2, check_dtype=False)


if __name__ == '__main__':
    unittest.main()
