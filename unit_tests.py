import unittest
import pandas as pd
import numpy as np

import unittest
from unittest.mock import patch, MagicMock

from data_cleaning import (
    clean_column_names,
    bradford_postcode_filter_function,
    isolate_client_ages,
    filter_post_codes_add_craven,
    filter_post_codes_add_craven,
)
from data_flow_MR import log_message
from data_utils import load_data_files, isolate_date_range


class TestDataCleaningFunctions(unittest.TestCase):
    def test_clean_column_names(self):
        # Sample DataFrame
        df = pd.DataFrame(columns=["UserID", " Service Type ", "File Closure"])
        dataframes = {"test_df": df}

        # Expected result
        expected_columns = ["client_id", "contact_service_type", "file_closure"]

        # Run the function
        cleaned_dataframes = clean_column_names(dataframes, log_message=log_message)

        # Assert
        self.assertListEqual(
            list(cleaned_dataframes["test_df"].columns), expected_columns
        )


class TestIsolateClientAges(unittest.TestCase):
    def setUp(self):
        # Sample data setup with age and franchise columns
        self.dataframes = {
            "df1": pd.DataFrame(
                {
                    "client_id": [1, 2, 3, 4],
                    "age": [25, 26, 18, 19],
                    "franchise": ["YiM", "YiM", "Non-YiM", "Non-YiM"],
                }
            ),
            "df2": pd.DataFrame(
                {"client_id": [5, 6], "age": [27, 18], "franchise": ["Non-YiM", "YiM"]}
            ),
        }
        # Define YiM providers list
        self.yim_providers = ["YiM"]

    def test_isolate_client_ages(self):
        # Expected DataFrame after filtering
        expected_df1 = pd.DataFrame(
            {
                "client_id": [
                    1,
                    3,
                ],  # Expected to remove client_id 1 due to age >= 26 and YiM provider
                "age": [25, 18],
                "franchise": ["YiM", "Non-YiM"],
            }
        ).reset_index(drop=True)

        expected_df2 = pd.DataFrame(
            {
                "client_id": [
                    6
                ],  # Expected to remove client_id 5 due to age >= 26 and Non-YiM provider
                "age": [18],
                "franchise": ["YiM"],
            }
        ).reset_index(drop=True)

        # Run the isolate_client_ages function with the sample data and YiM providers list
        result_dataframes = isolate_client_ages(self.dataframes, self.yim_providers)

        # Verify the result matches the expected output
        pd.testing.assert_frame_equal(
            result_dataframes["df1"], expected_df1, check_dtype=False
        )
        pd.testing.assert_frame_equal(
            result_dataframes["df2"], expected_df2, check_dtype=False
        )


class TestDataFilesLoading(unittest.TestCase):
    @patch("os.listdir")
    @patch("os.path.join")
    @patch("pandas.read_csv")
    def test_load_data_files(self, mock_read_csv, mock_join, mock_listdir):
        # Setup mock responses
        mock_listdir.return_value = [
            "cypmh_referrals_1705883521.csv",
            "cypmh_referrals_1705883581.csv",
            "cypmh_referrals_mib_1705926901.csv",
        ]
        mock_join.side_effect = lambda directory, filename: f"{directory}/{filename}"

        # Mock pandas.read_csv to return a simple DataFrame
        df_mock = pd.DataFrame({"column": [1, 2, 3]})
        mock_read_csv.return_value = df_mock

        # Define file_info dict
        file_info = {"referrals": {"filename": "cypmh_referrals.csv"}}

        # Expected DataFrame after concatenating the mock files
        expected_df = pd.DataFrame({"column": [1, 2, 3, 1, 2, 3, 1, 2, 3]})

        # Call the function under test
        dataframes = load_data_files("mock_directory", file_info)

        # Assertions
        pd.testing.assert_frame_equal(dataframes["referrals"], expected_df)
        self.assertEqual(
            mock_read_csv.call_count,
            3,
            "read_csv should be called three times for three files",
        )


class TestBradfordPostcodeFiltering(unittest.TestCase):
    def test_bradford_postcode_filter_function(self):
        # Mock data simulating your DataFrame structure
        data = {
            "client_id": [1, 2, 3, 4, 5, 6, 7],
            "post_code": [
                "BD1 2AB",
                "BD20 8HH",
                "LS29 8JH",
                "HX3 5AX",
                "BD99 1AB",
                "YO24 1AB",
                "LS1 4PL",
            ],
        }
        df = pd.DataFrame(data)
        dataframes = {"test_df": df}

        # Apply the Bradford postcode filtering function
        filtered_dataframes = bradford_postcode_filter_function(dataframes)

        # Expected postcodes to remain after filtering
        expected_postcodes = [
            "BD1 2AB",
            "BD20 8HH",
            "LS29 8JH",
            "HX3 5AX",
            "BD99 1AB",
        ]  # Adjust based on your function logic

        # Extract remaining postcodes after filtering
        remaining_postcodes = filtered_dataframes["test_df"]["post_code"].tolist()

        # Assert that only the expected Bradford postcodes remain
        self.assertListEqual(remaining_postcodes, expected_postcodes)


# class TestIsolateDateRange(unittest.TestCase):
#     def setUp(self):
#         # Create a sample DataFrame for testing
#         self.data = {
#             'date_column': [
#                 '01/01/2020', '15/03/2020', '10/06/2020',
#                 '20/08/2020', '25/12/2020'
#             ],
#             'value': [1, 2, 3, 4, 5]
#         }
#         self.df = pd.DataFrame(self.data)

#     def test_isolate_date_range(self):
#         # Define the start and end dates for filtering
#         start_date = '01/03/2020'  # DD/MM/YYYY format
#         end_date = '30/09/2020'    # DD/MM/YYYY format

#         # Call the function under test
#         filtered_df = isolate_date_range(self.df, 'date_column', (start_date, end_date))

#         # Check the number of rows in the filtered DataFrame
#         self.assertEqual(len(filtered_df), 3, "The filtered DataFrame should contain 3 rows.")

#         # Verify the filtered dates are within the specified range
#         expected_dates = ['15/03/2020', '10/06/2020', '20/08/2020']
#         filtered_dates = filtered_df['date_column'].dt.strftime('%d/%m/%Y').tolist()
#         self.assertListEqual(filtered_dates, expected_dates, "The dates in the filtered DataFrame do not match the expected dates.")


class TestCravenPostcodesFiltering(unittest.TestCase):
    def test_filter_post_codes_add_craven(self):
        # Mock data simulating your DataFrame structure
        data = {
            "client_id": [1, 2, 3, 4, 5, 6],
            "post_code": [
                "BD20 8NJ",
                "LS2 97 UI",
                "BD1 2AB",
                "LS27 KT",
                "UNKNOWN",
                " ",
            ],
        }
        df = pd.DataFrame(data)
        dataframes = {"test_df": df}

        # Expected results after applying the function
        expected_craven_marks = [True, True, False, True, False, False]

        # Apply the filtering function
        filtered_dataframes = filter_post_codes_add_craven(dataframes)

        # Assert that Craven postcodes are correctly identified
        self.assertTrue(
            (
                filtered_dataframes["test_df"]["craven"].values == expected_craven_marks
            ).all()
        )


if __name__ == "__main__":
    unittest.main()
