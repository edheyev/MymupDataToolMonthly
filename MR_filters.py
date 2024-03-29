# -*- coding: utf-8 -*-
"""
Created on Tues Feb 06 15:58:58 2023

@author: Ed Heywood-Everett
"""
import pandas as pd
import numpy as np

from data_utils import calculate_date_differences, isolate_date_range, get_previous_month_date_range


def CIC_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'looked_after_child' column is 'YES'
    filtered_df = df.loc[df["looked_after_child"] == "YES"]
    return filtered_df


def SEN_FILTER(df, df_name="empty"):
    filtered_df = df.loc[df["special_education_needs"] == "YES"]
    return filtered_df


def EHCP_FILTER(df, df_name="empty"):
    filtered_df = df.loc[df["ehcp"] == "YES"]
    return filtered_df


def CRAVEN_FILTER(df, df_name="empty"):
    filtered_df = df.loc[df["craven"] == True]
    return filtered_df


def BRADFORD_FILTER(df, df_name="empty"):
    filtered_df = df.loc[df["craven"] == False]

    return filtered_df


# referalls sheet


def OCR_filter(df, row, dfname="empty", date_range=None):
    try:

        if row == "Number referrals":
            df = isolate_date_range(df, "referral_date", date_range)

            # unique count
            return df
        elif row == "Number unique referrals":
            df = isolate_date_range(df, "referral_date", date_range)

            # unique count
            filtered_df = df.drop_duplicates(subset=["global_id"])
            # Filter the DataFrame to keep only non-rejected referrals
            return filtered_df
        elif row == "Referrals accepted":
            df = isolate_date_range(df, "referral_date", date_range)

            unique_client_id_df = df
            # Filter the DataFrame to keep only non-rejected referrals
            filtered_df = unique_client_id_df[
                unique_client_id_df["referral_rejected"] == False
            ]
     
            return filtered_df
        elif row == "Referrals refused":
            df = isolate_date_range(df, "file_closure", date_range)
            innapropriate_map = ["Organisation rejects referral - Referral not suitable pre-assessment/post-assessment", 
                                 "Organisation rejects referral - Threshold too high",
                                 "Inappropriate Referral Request"]
            # innapropriate refs
            filtered_df = df[df["file_closure_reason"].isin(innapropriate_map)]


            # referrals refused count from file clusures data dump of innaproitare referrals
            # filtered_df = df[df["referral_rejected"] == True]
            return filtered_df
        elif row == "Number open cases":
            return "PLACEHOLDER"
        elif row == "Number closed cases":
            df = isolate_date_range(df, "file_closure", date_range)
            # closed cases - file closure dd all file closures that are not innapropriate UNIQUE
            # filtered_df = df[df["referral_rejected"] == False]
            # unique_client_id_df = df.drop_duplicates(subset=["client_id"])
            return df

        return "row not caught"
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )


def CIC_CLA_caseload_and_referrals_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df


def SEN_caseload_and_referrals_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df


def EHCP_caseload_and_referrals_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df


def CRAVEN_caseload_and_referrals_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df


def BRADFORD_DISTRICT_caseload_and_referrals_filter(
    df, row, dfname="empty", date_range=None
):

    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df


# demographics sheet


def All_Referrals_by_demographics_filter(df, row, dfname="empty", date_range=None):
    df = df[df["referred_in_date_range"] == True]

    try:
        # List for age categories
        age_categories = [
            "Age 4",
            "Age 5",
            "Age 6",
            "Age 7",
            "Age 8",
            "Age 9",
            "Age 10",
            "Age 11",
            "Age 12",
            "Age 13",
            "Age 14",
            "Age 15",
            "Age 16",
            "Age 17",
            "Age 18",
            "Age 19",
            "Age 20",
            "Age 21",
            "Age 22",
            "Age 23",
            "Age 24",
            "Age 25",
            "Out of age range (data input error)",
        ]

        # List for gender categories
        gender_categories = [
            "Female (including Transgender Woman)",
            "Male (including Transgender Man)",
            "Non-Binary",
            "Not known (Person stated Gender Code not recorded)",
            "No Stated (patient asked but declined to provide a response)",
            "Other (not listed)",
        ]

        # List for ethnicity categories
        ethnicity_categories = [
            "African",
            "Arab",
            "Bangladeshi",
            "Caribbean",
            "Central and Eastern European",
            "Chinese",
            "Gypsy/Roma/Traveller",
            "Indian",
            "Irish",
            "Latin America",
            "Pakistani",
            "White and Asian",
            "White and Black African",
            "White and Black Caribbean",
            "White British",
            "Any other Asian background",
            "Any other Black background",
            "Any other Ethnic group",
            "Any other Mixed background",
            "Any other White background",
            "Unknown Ethnicity",
        ]
        
        df =  df.drop_duplicates(subset=["global_id"])

        # Determine the category of 'row' and filter accordingly
        if row in age_categories:
            # Extract the age from the row string, assuming row format is "Age X" where X is the age
            if row.startswith("Age "):
                age = int(row.split(" ")[1])  # Extract age from the row string
                filtered_df = df[
                    df["age"] == age
                ]  # Filter df for rows matching the age
            elif row == "Out of age range (data input error)":
                # Handle out of range ages if necessary, e.g., filter out known invalid ages
                # This part depends on how you want to handle this special case
                filtered_df = df[
                    df["age"] > 25
                ]  # Example: filtering ages greater than 25
            else:
                # If the row does not represent an age category, return the df as is or handle differently
                return df  # Or: return "Row does not represent an age category"

        elif row in gender_categories:

            gender_map = {
                "Female (including Transgender Woman)": "Female (including Transgender Woman)",
                "Male (including Transgender Man)": "Man (including Transgender Man)",
                "Non-Binary": "Non-Binary",
                "Not known (Person stated Gender Code not recorded)": "Not Known (not recorded)",
                "No Stated (patient asked but declined to provide a response)": "Not Stated (patient asked but declined to provide a response)",
                "Other (not listed)": "Other (not listed)",
                "Blank (nothing selected)": "Blank",  # Special handling for blank entries
            }
            # Check if the row corresponds to a gender category and fetch the mapped value
            if row in gender_map:
                mapped_value = gender_map[row]
                if mapped_value == "Blank":
                    # Filter for rows where 'client_ethnicity' is NaN
                    filtered_df = df[pd.isna(df["gender_name"])]
                else:
                    filtered_df = df[df["gender_name"] == mapped_value]

                return (
                    filtered_df  # Or: return "Row does not represent a gender category"
                )

        elif row in ethnicity_categories:
            ethnic_map = {
                "White British": "White - British",
                "Irish": "White - Irish",
                "Central and Eastern European": "Central and Eastern European",
                "Any other White background": "White - Any other White background",
                "Gypsy/Roma/Traveller": "Gypsy/Roma/Traveller",
                "White and Black Caribbean": "Mixed - White and Black Caribbean",
                "White and Black African": "Mixed - White and Black African",
                "White and Asian": "Mixed - White and Asian",
                "Any other Mixed background": "Mixed - Any other mixed background",
                "Indian": "Asian or Asian British - Indian",
                "Pakistani": "Asian or Asian British - Pakistani",
                "Bangladeshi": "Asian or Asian British - Bangladeshi",
                "Any other Asian background": "Asian or Asian British - Any other Asian background",
                "Caribbean": "Black or Black British - Caribbean",
                "African": "Black or Black British - African",
                "Any other Black background": "Black or Black British - Any other Black background",
                "Chinese": "Other Ethnic Groups - Chinese",
                "Any other Ethnic group": "Other Ethnic Groups - Any other ethnic group",
                "Unknown Ethnicity": ["Not known", "Not stated", " "],
                "Arab": "Arab",
                "Latin America": "Latin America",
            }

            mapped_value = ethnic_map.get(row, ["Unknown Ethnicity"])

            if row == "Unknown Ethnicity":
                # Handle "Unknown" with special conditions for NaN and empty strings
                conditions = (
                    df["ethnicity_name"].isin(mapped_value) | 
                    pd.isna(df["ethnicity_name"]) | 
                    (df["ethnicity_name"] == "")
                )
                filtered_df = df[conditions]
            elif isinstance(mapped_value, list):
                # If mapped_value is a list, filter rows matching any value in the list
                filtered_df = df[df["ethnicity_name"].isin(mapped_value)]
            else:
                # For single string values, proceed with the direct comparison
                filtered_df = df[df["ethnicity_name"] == mapped_value]

            return filtered_df
        else:
            return "Row category not recognized"
        
        # filtered_df = filtered_df[(filtered_df["client_state"] != 'Closed') & 
        #                   (filtered_df["client_state"].notna()) & 
        #                   (filtered_df["client_state"] != '')]
        return filtered_df  # Return the filtered dataframe
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )


def All_CIC_CLA_Referrals_by_demographics_filter(
    df, row, dfname="empty", date_range=None
):

    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df


def All_SEN_Referrals_by_demographics_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df


def All_EHCP_Referrals_by_demographics_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df


def All_CRAVEN_Referrals_by_demographics_filter(
    df, row, dfname="empty", date_range=None
):

    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df


def BRADFORD_DISTRICT_Referrals_by_demographics_filter(
    df, row, dfname="empty", date_range=None
):

    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df


# referral source sheet


def Source_of_All_Referrals_filter(df, row, dfname="empty", date_range=None):
    # df = isolate_date_range(df, "referral_date",date_range)

    referral_mapping = {
        "Accident and Emergency Department": "Accident And Emergency Department",
        "CAMHS - Crisis Team (Hospital Urgents)": "CAMHS Crisis",
        "CAMHS - Core/Step Down": "CAMHS Core/Step down",
        "CAMHS - Waiting List": "CAMHS Waiting List",
        "Child Health: Community-based Paediatrics": "Community-based Paediatrics",
        "Child Health: Hospital-based Paediatrics": "Hospital-based Paediatrics",
        "Child Health: School Nurse": "School Nurse",
        "Community Mental Health Team (Adult Mental Health)": "Other secondary care specialty",
        "Employer": "Other service or agency",
        "Employer: Occupational Health": "Other service or agency",
        "Family Support Worker": "Other Primary Health Care",
        "Improving Access to Psychological Therapies Service": "Other secondary care specialty",
        "Independent Sector - Medium Secure Inpatients": "Other secondary care specialty",
        "Independent Sector - Low Secure Inpatients": "Other secondary care specialty",
        "Inpatient Service (Older People)": "Other secondary care specialty",
        "Inpatient Service  (Forensics)": "Other secondary care specialty",
        "Inpatient Service (Learning Disabilities)": "Other secondary care specialty",
        "Inpatient Service (Adult Mental Health)": "Other secondary care specialty",
        "Inpatient Service (Child and Adolescent Mental Health)": "CAMHS Crisis",
        "Internal Referral": "Internal Referral",
        "Justice System: Courts": "Youth Offending Service",
        "Justice System: Police": "Police",
        "Justice System: Prison": "Police",
        "Justice System: Probation Service": "Youth Offending Service",
        "Justice System: Youth Offending Team": "Youth Offending Service",
        "Justice System: Court Liaison and Diversion Service": "Youth Offending Service",
        "Local Authority and Other Public Services: Education Service / Educational Establishment": "Education Service",
        "Local Authority and Other Public Services: Housing Service": "Housing Service",
        "Local Authority and Other Public Services: Social Services": "Social Services",
        "Mental Health Drop In Service": "Other service or agency",
        "Other: Asylum Services": "Other service or agency",
        "Other: Drug Action Team / Drug Misuse Agency": "Drug Action Team / Drug Misuse Agency",
        "Other Independent Sector Mental Health Services": "Other service or agency",
        "Other: Jobcentre Plus": "Other service or agency",
        "Other: Out of Area Agency": "Out of Area Agency",
        "Other Primary Health Care": "Other Primary Health Care",
        "Other: Secondary Care Speciality": "Other secondary care specialty",
        "Other SERVICE or agency": "Other service or agency",
        "Other: Single Point of Access Service": "Single Point of Access Service",
        "Other: Telephone or Electronic Access Service": "Other service or agency",
        "Other: Urgent and Emergency Care Ambulance Service": "Accident And Emergency Department",
        "Permanent transfer from another Mental Health NHS Trust": "Permanent transfer from another Mental Health NHS Trust",
        "Primary Health Care Family Support Worker": "Other Primary Health Care",
        "Primary Health Care: General Medical Practitioner Practice": "GP services",
        "Primary Health Care: Health Visitor": "Other Primary Health Care",
        "Primary Health Care: Maternity Service": "Other Primary Health Care",
        "Self-Referral: Self": "Self",
        "Self-Referral: Carer/Relative": "Carer",
        "Temporary transfer from another Mental Health NHS Trust": "Other service or agency",
        "Transfer by graduation from Child and Adolescent Mental Health Services to Adult Mental Health Services": "Transfer by graduation from Child Adolescent Mental Health Services to Adult",
        "Voluntary Sector": "Voluntary Sector",
        "Blanks": "Unknown",
        "Education": "Education Service",
        "Housing": "Housing Service",
        "Justice System": "Police",
        "Primary care": "GP services",
        "Self-referral": "Self",
        "Statutory health and social care": "Social Services",
        "Urgent and emergency care": "CAMHS Crisis",
        "VCS": "Voluntary Sector",
        "Other": "Other service or agency"
    }
    

    try:
        if row == "Unknown":
                return df[pd.isna(df["referral_source"])]
            
        # Find all keys in referral_mapping that have a value matching 'row'
        matching_keys = [key for key, value in referral_mapping.items() if value == row]
  
        # Check if there are matching keys to filter on
        if not matching_keys:
            print(
                f"No matching referral source found for '{row}'. Using unfiltered dataframe."
            )
            return df

        # Filter the dataframe for rows where 'referral_source' matches any of the matching keys
        filtered_df = df[df["referral_source"].isin(matching_keys)]

        return filtered_df

    except Exception as e:
        print(
            f"Error in Source_of_All_Referrals_filter with row: '{row}', {e}. Current df: '{dfname}'"
        )
        return pd.DataFrame()  # Return an empty DataFrame in case of error


def Source_of_Referrals___CIC_CLA_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df


def Source_of_Referrals___SEN_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df


def Source_of_Referrals___EHCP_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df


def Source_of_Referrals___CRAVEN_filter(df, row, dfname="empty", date_range=None):

    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df


def Source_of_Referrals___BRADFORD_DISTRICT_filter(
    df, row, dfname="empty", date_range=None
):

    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df


# two attended contacts sheet

def No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_filter(
    df, row, dfname="empty", date_range=None
):

    df = isolate_date_range(df, "second_contact_/_indirect_date", date_range)
    
    try:
        if row == "All":
            return df
        elif row == "CIC/CLA":
            return CIC_FILTER(df, dfname)
        elif row == "SEN":
            return SEN_FILTER(df, dfname)
        elif row == "EHCP":
            return EHCP_FILTER(df, dfname)
        elif row == "CRAVEN":
            return CRAVEN_FILTER(df, dfname)
        elif row == "BRADFORD DISTRICT":
            return BRADFORD_FILTER(df, dfname)

        return "row not caught"
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )


# dna and cancellations sheet


def DNAs_and_cancellations_filter(df, row, dfname="empty", date_range=None):
    df = isolate_date_range(df, "contact_date", date_range)

    # ony filter f2f, tel, video, talk type
    allowed_contact_types = [
        "Face to Face",
        "Telephone",
        "Type talk",
        "Talk type for a person unable to speak",
        "Video consultation",
        "Instant Messaging (Synchronous)",
        "Other (not listed)"
    ]
    df = df[df["contact_approach"].isin(allowed_contact_types)]
    # only dna in attendace col

    # Initial filter based on the category
    if "CIC/CLA" in row:
        df = CIC_FILTER(df, dfname)
    elif "SEN" in row:
        df = SEN_FILTER(df, dfname)
    elif "EHCP" in row:
        df = EHCP_FILTER(df, dfname)
    elif "CRAVEN" in row:
        df = CRAVEN_FILTER(df, dfname)
    elif "BRADFORD DISTRICT" in row:
        df = BRADFORD_FILTER(df, dfname)

    # Now filter based on the type of appointment
    try:
        if "DNA Appointments" in row:
            filtered_df = df[df["attendance"] == "Did not Attend"]
            
        elif "Cancelled by patient" in row:
            filtered_df = df[
                df["attendance"] == "Cancelled By Client"
            ]  # Placeholder, replace with actual value
        elif "Cancelled by Provider" in row:
            filtered_df = df[
                df["attendance"] == "Cancelled By Professional"
            ]  
        else:
            # Return the df as is if the row doesn't match the expected patterns
            # This might need adjustment based on your specific needs
            return df

        return filtered_df

    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )


def Goals_Based_Outcomes_filter(df, row, dfname="empty", date_range=None):
    df = isolate_date_range(df, "goal_date", date_range)

    def calculate_average_scores(df):
        # Ensure you're working on a copy of the DataFrame to avoid affecting the original data
        df_copy = df.copy()

        # Convert score columns to numeric, treating non-numeric values as NaN
        for column in ["score_1", "score_2", "score_3"]:
            df_copy.loc[:, column] = pd.to_numeric(df_copy[column], errors="coerce")

        # Calculate the average of the score columns, ignoring NaN values
        df_copy.loc[:, "average_score"] = df_copy[
            ["score_1", "score_2", "score_3"]
        ].mean(axis=1, skipna=True)

        return df_copy

    try:
        # First, filter based on the category
        if "CIC/CLA" in row:
            df = CIC_FILTER(df, dfname)
        elif "SEN" in row:
            df = SEN_FILTER(df, dfname)
        elif "EHCP" in row:
            df = EHCP_FILTER(df, dfname)
        elif "CRAVEN" in row:
            df = CRAVEN_FILTER(df, dfname)
        elif "BRADFORD DISTRICT" in row:
            df = BRADFORD_FILTER(df, dfname)

        # Now, filter based on the specific goal outcome type
        if "Initials completed" in row:
            filtered_df = df[df["initial_or_follow_up"] == "Initial"]
            
        elif "Follow ups completed" in row:
            filtered_df = df[(df["initial_or_follow_up"] == "Follow  up")|(df["initial_or_follow_up"] == "Final")|(df["initial_or_follow_up"] == "Initial or Follow up")]

        elif "Initial score" in row:
            filtered_df = df[df["initial_or_follow_up"] == "Initial"]
            df_with_average = calculate_average_scores(filtered_df)
            return (df_with_average, "average_score")

        elif "Follow up score" in row:
            filtered_df = df[(df["initial_or_follow_up"] == "Follow  up")|(df["initial_or_follow_up"] == "Final")|(df["initial_or_follow_up"] == "Initial or Follow up")]
            df_with_average = calculate_average_scores(filtered_df)
            return (df_with_average, "average_score")

        else:
            # If the row doesn't match any expected pattern
            return df

        return filtered_df

    except Exception as e:
        print(
            f"Error in Goals_Based_Outcomes_filter with row: {row}, {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in Goals_Based_Outcomes_filter with row: {row}, {e}. Current df is {dfname}"
        )


# goal themes sheet
def All_Goal_Themes_filter(df, row, dfname="empty", date_range=None):

    # date_range = get_previous_month_date_range(date_range)
    df = isolate_date_range(df, "goal_date", date_range)

    # TODO ADD percentages to ting
    try:
        # Filter based on goal theme
        if row in [
            "Being able to maintain and build positive relationships",
            "Being able to support others",
            "Being better at managing my emotional wellbeing",
            "Being better at managing risks and feeling safer",
            "Covid-19 Support",
            "Improving my confidence and self esteem",
            "Improving my physical wellbeing",
            "Reducing my isolation",
            "Understanding who I am",
        ]:
            # Assuming 'goal_theme' is the column where these themes are listed
            df_filtered = df[df["goal_theme"] == row]
            return df_filtered

        elif row == "TOTAL":
            # Assuming 'TOTAL' requires a different type of calculation, e.g., counting all themes
            # This could be a sum of counts for each theme, or a unique count of cases, etc.
            # Adjust this logic based on what 'TOTAL' means in your context
            # Example: return the count of all non-empty 'goal_theme' entries
            total_count = df["goal_theme"].notnull().sum()
            return f"Total Goal Themes: {total_count}"

        else:
            return "row not caught"

    except Exception as e:
        print(
            f"Error in All_Goal_Themes_filter with row: {row}, {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in All_Goal_Themes_filter with row: {row}, {e}. Current df is {dfname}"
        )


def CIC_Goal_Themes_filter(df, row, dfname="empty", date_range=None):
    initial_filter = CIC_FILTER(df, dfname)
    filtered_df = All_Goal_Themes_filter(initial_filter, row, dfname)
    return filtered_df


def SEN_Goal_Themes_filter(df, row, dfname="empty", date_range=None):
    initial_filter = SEN_FILTER(df, dfname)
    filtered_df = All_Goal_Themes_filter(initial_filter, row, dfname)
    return filtered_df


def EHCP_Goal_Themes_filter(df, row, dfname="empty", date_range=None):
    initial_filter = EHCP_FILTER(df, dfname)
    filtered_df = All_Goal_Themes_filter(initial_filter, row, dfname)
    return filtered_df


def CRAVEN_Goal_Themes_filter(df, row, dfname="empty", date_range=None):
    initial_filter = CRAVEN_FILTER(df, dfname)
    filtered_df = All_Goal_Themes_filter(initial_filter, row, dfname)
    return filtered_df


def Bradford_District_Goal_Themes_filter(df, row, dfname="empty", date_range=None):
    initial_filter = BRADFORD_FILTER(df, dfname)
    filtered_df = All_Goal_Themes_filter(initial_filter, row, dfname)
    return filtered_df


# Discharge Data sheet


def Overall_Discharges_filter(df, row, dfname="empty", date_range=None):
    df = isolate_date_range(df, "file_closure", date_range)

    # Mapping unique closure reasons to broader categories
    closure_reason_map = {
        "Planned ending met outcomes at Review Point": "Number completed treatment",
        "Planned ending met outcomes at Assessment Point": "Number completed treatment",
        "Treatment completed": "Number completed treatment",
        "Single episode": "Number completed treatment",
        "Open access ended": "Number completed treatment",
        "Planned ending without review": "Number completed treatment",
        "Decision made at review": "Number completed treatment",
        "No further treatment required": "Number completed treatment",
        "Organisation rejects referral - Referral not suitable pre-assessment/post-assessment": "Number inappropriate referrals",
        "Organisation rejects referral - Threshold too high": "Number inappropriate referrals",
        "Inappropriate Referral Request": "Number inappropriate referrals",
        "Organisation cannot contact Client prior to assessment": "Number who could not be contacted",
        "Client disengages": "Number disengaged",
        "Client rejects referral": "Number disengaged",
        "Client did not attend": "Number disengaged",
        "Client requested discharge": "Number disengaged",
        "Client declined a service prior to or during assessment": "Number disengaged",
        "Refused to be seen": "Number disengaged",
        "Client not available for pre-arranged appointments": "Number disengaged",
        "Client not available for assessment - failure to keep pre-arranged appointments": "Number disengaged",
        "Admitted elsewhere (at the same or other Health Care Provider)": "Number signposted to another CCG provider",
        "Referred to other speciality/service (at the same or other Health Care Provider)": "Number signposted to another CCG provider",
        "Referred to CAMHS": "Number signposted to another CCG provider",
        "Referred to Healthy Child Team": "Number signposted to another CCG provider",
        "Referred to VCS": "Number signposted to another CCG provider",
        "Referred to BDCfT Specialist CAMHS": "Number signposted to another CCG provider",
        "Referred to Step 2": "Number signposted to another CCG provider",
        "Referred to Relate Bradford": "Number signposted to another CCG provider",
        "Referred to another YIM provider": "Number signposted to another CCG provider",
        "Not disclosed": "Not Disclosed",
        "Blanks": "Unknown",
    }

    try:
        # Filter DataFrame based on the broader category
        filtered_reasons = {
            value: key for key, value in closure_reason_map.items() if value == row
        }
        if row in [
            "Number completed treatment",
            "Number inappropriate referrals",
            "Number who could not be contacted",
            "Number disengaged",
            "Number signposted to another CCG provider",
        ]:
            df_filtered = df[df["file_closure_reason"].map(closure_reason_map) == row]
        elif row == "Not Disclosed":
            # Assuming "Not Disclosed" means missing or unspecified closure reasons
            df_filtered = df[
                pd.isna(df["file_closure_reason"])  # This is equivalent to pd.isnull()
                | (df["file_closure_reason"] == "Not Disclosed")
            ]

        return df_filtered

    except Exception as e:
        print(
            f"Error in file_closure_reason_filter with row: {row}, {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in file_closure_reason_filter with row: {row}, {e}. Current df is {dfname}"
        )


def Discharges_CIC_CLA_filter(df, row, dfname="empty", date_range=None):
    initial_filter = CIC_FILTER(df, dfname)
    filtered_df = Overall_Discharges_filter(initial_filter, row, dfname)
    return filtered_df


def Discharges_SEN_filter(df, row, dfname="empty", date_range=None):
    initial_filter = SEN_FILTER(df, dfname)
    filtered_df = Overall_Discharges_filter(initial_filter, row, dfname)
    return filtered_df


def Discharges_EHCP_filter(df, row, dfname="empty", date_range=None):
    initial_filter = EHCP_FILTER(df, dfname)
    filtered_df = Overall_Discharges_filter(initial_filter, row, dfname)
    return filtered_df


def Discharges_CRAVEN_filter(df, row, dfname="empty", date_range=None):
    initial_filter = CRAVEN_FILTER(df, dfname)
    filtered_df = Overall_Discharges_filter(initial_filter, row, dfname)
    return filtered_df


def Discharges_BRADFORD_DISTRICT_filter(df, row, dfname="empty", date_range=None):
    initial_filter = BRADFORD_FILTER(df, dfname)
    filtered_df = Overall_Discharges_filter(initial_filter, row, dfname)
    return filtered_df


# wait list data sheet


def Overall_Number_on_Waiting_list_filter(df, row, dfname="empty", date_range=None):
    # remove any referral_date after date range.
    
    
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date).normalize()  # Normalize to remove time
    end_date = pd.to_datetime(end_date).normalize()  # Normalize to remove time


    try:
        df = df.copy()

        # Normalize datetime columns
        df["first_contact_/_indirect_date"] = pd.to_datetime(df["first_contact_/_indirect_date"], errors='coerce').dt.normalize()
        df["file_closures"] = pd.to_datetime(df["file_closures"], errors='coerce').dt.normalize()
        df["referral_rejections"] = pd.to_datetime(df["referral_rejections"], errors='coerce').dt.normalize()

        # Define the condition for 'first_contact_/_indirect_date' being empty
        condition1 = pd.isnull(df["first_contact_/_indirect_date"]) | (df["first_contact_/_indirect_date"] == "")

        # Conditions for 'file_closures' and 'referral_rejections' not having values before end_date
        condition2_file_closures = pd.isnull(df["file_closures"]) | (df["file_closures"] > end_date)
        condition2_referral_rejections = pd.isnull(df["referral_rejections"]) | (df["referral_rejections"] > end_date)

        # Conditions to exclude rows where specific columns are not null
        condition3_is_first_contact_indirect = pd.isnull(df["is_first_contact_/_indirect"])
        condition4_second_contact_indirect_date = pd.isnull(df["second_contact_/_indirect_date"])
        condition5_is_second_contact_indirect = pd.isnull(df["is_second_contact_/_indirect"])

        # Combine all conditions
        df_filtered = df[
            condition1 & 
            condition2_file_closures & 
            condition2_referral_rejections & 
            condition3_is_first_contact_indirect & 
            condition4_second_contact_indirect_date & 
            condition5_is_second_contact_indirect
        ]
        df = df_filtered[df_filtered['referral_date'] <= end_date]
        

        if row == "All":            df = df
        elif row == "CIC/CLA":
            df = CIC_FILTER(df, dfname)
        elif row == "SEN":
            df = SEN_FILTER(df, dfname)
        elif row == "EHCP":
            df = EHCP_FILTER(df, dfname)
        elif row == "CRAVEN":
            df = CRAVEN_FILTER(df, dfname)
        elif row == "BRADFORD DISTRICT":
            df = BRADFORD_FILTER(df, dfname)

        # unique_client_id_df = df.drop_duplicates(subset=["client_id"])
        return df

    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )


# wait times sheet
from dateutil import parser
import pandas as pd

def find_latest_datetime(column_value):
    datetime_strings = str(column_value).split(',')
    latest_datetime = None

    for datetime_str in datetime_strings:
        try:
            dt = parser.parse(datetime_str.strip(), dayfirst=False)
            if latest_datetime is None or dt > latest_datetime:
                latest_datetime = dt
        except (ValueError, TypeError):
            continue
    
    if latest_datetime:
        return latest_datetime.replace(tzinfo=None)
    else:
        return pd.NaT

def Overall_Wait_Times_filter(df, row, dfname="empty", date_range=None):
    start_date, end_date = date_range
    start_date, end_date = pd.to_datetime([start_date, end_date]).normalize()
    try:
        
        df = df.copy()
        # Apply the custom parser to columns that might contain multiple datetime values
        df['file_closures'] = df['file_closures'].apply(find_latest_datetime)
        df['referral_rejections'] = df['referral_rejections'].apply(find_latest_datetime)

        # Create a copy of the DataFrame to avoid SettingWithCopyWarning

        # Now proceed with your existing logic
        date_cols = [
            "first_contact_/_indirect_date",
            "referral_date",
            "second_contact_/_indirect_date",
        ]

        for col in date_cols:
            df.loc[:, col] = pd.to_datetime(df[col], format="%Y-%m-%d", errors="coerce").dt.normalize()
        
        # Now call the new function to calculate the differences
        df = calculate_date_differences(df)
        
        df_filtered = df[df['referral_date'] <= end_date]

        if pd.api.types.is_datetime64_any_dtype(df_filtered['file_closures']):
            # Safe to use .dt accessor
            # df_filtered['file_closures'] = df_filtered['file_closures'].dt.normalize()
            df_filtered.loc[:, 'file_closures'] = df_filtered['file_closures'].dt.normalize()

            
        if pd.api.types.is_datetime64_any_dtype(df_filtered['referral_rejections']):
            # Safe to use .dt accessor
            # df_filtered['referral_rejections'] = df_filtered['referral_rejections'].dt.normalize()
            df_filtered.loc[:, 'referral_rejections'] = df_filtered['referral_rejections'].dt.normalize()

                
        if row == "Average Weeks from referral to 1st attended contact/indirect":
            df_filtered = isolate_date_range(
                df_filtered, "first_contact_/_indirect_date", date_range
            )
                        # start_date, end_date = pd.to_datetime(date_range)
            df_filtered['file_closures'] = pd.to_datetime(df_filtered['file_closures'], errors='coerce')
            df_filtered['referral_rejections'] = pd.to_datetime(df_filtered['referral_rejections'], errors='coerce')
            
            # start_date, end_date = pd.to_datetime(date_range)
            mask_file_closures_within_range_or_na = (df_filtered['file_closures'].isna()) | ((df_filtered['file_closures'] >= start_date) & (df_filtered['file_closures'] <= end_date))
            mask_referral_rejections_within_range_or_na = (df_filtered['referral_rejections'].isna()) | ((df_filtered['referral_rejections'] >= start_date) & (df_filtered['referral_rejections'] <= end_date))
            combined_mask = mask_file_closures_within_range_or_na & mask_referral_rejections_within_range_or_na
            df_filtered = df_filtered.loc[combined_mask]
            
            return (df_filtered, "first_contact_referral_diff")

        elif row == "Average Weeks from referral to 2nd attended contact/indirect":
            df_filtered = df_filtered.dropna(subset=["second_contact_/_indirect_date"])
            df_filtered = isolate_date_range(
                df_filtered, "second_contact_/_indirect_date", date_range
            )
            # start_date, end_date = pd.to_datetime(date_range)
            df_filtered['file_closures'] = pd.to_datetime(df_filtered['file_closures'], errors='coerce')
            df_filtered['referral_rejections'] = pd.to_datetime(df_filtered['referral_rejections'], errors='coerce')

            mask_file_closures_within_range_or_na = (df_filtered['file_closures'].isna()) | ((df_filtered['file_closures'] >= start_date) & (df_filtered['file_closures'] <= end_date))
            mask_referral_rejections_within_range_or_na = (df_filtered['referral_rejections'].isna()) | ((df_filtered['referral_rejections'] >= start_date) & (df_filtered['referral_rejections'] <= end_date))
            combined_mask = mask_file_closures_within_range_or_na & mask_referral_rejections_within_range_or_na
            df_filtered = df_filtered.loc[combined_mask]

            
            
            return (df_filtered, "second_contact_referral_diff")

        elif (
            row
            == "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect"
        ):
            df_filtered = isolate_date_range(
                df_filtered, "second_contact_/_indirect_date", date_range
            )
            df_filtered['file_closures'] = pd.to_datetime(df_filtered['file_closures'], errors='coerce')
            df_filtered['referral_rejections'] = pd.to_datetime(df_filtered['referral_rejections'], errors='coerce')

            mask_file_closures_within_range_or_na = (df_filtered['file_closures'].isna()) | ((df_filtered['file_closures'] >= start_date) & (df_filtered['file_closures'] <= end_date))
            mask_referral_rejections_within_range_or_na = (df_filtered['referral_rejections'].isna()) | ((df_filtered['referral_rejections'] >= start_date) & (df_filtered['referral_rejections'] <= end_date))
            combined_mask = mask_file_closures_within_range_or_na & mask_referral_rejections_within_range_or_na
            df_filtered = df_filtered.loc[combined_mask]
            return (df_filtered, "second_first_contact_diff")

    except Exception as e:
        print(f"Error in Overall_Wait_Times_filter with row: {e}. Current df: {dfname}")
        raise

    return df


def CIC_CLA_Wait_Times_filter(
    df,
    row,
    dfname="empty",
    date_range=None,
):
    initial_filter = CIC_FILTER(df, dfname)
    filtered_df = Overall_Wait_Times_filter(initial_filter, row, dfname, date_range)
    return filtered_df


def SEN_Wait_Times_filter(
    df,
    row,
    dfname="empty",
    date_range=None,
):
    initial_filter = SEN_FILTER(df, dfname)
    filtered_df = Overall_Wait_Times_filter(initial_filter, row, dfname, date_range)
    return filtered_df


def EHCP_Wait_Times_filter(
    df,
    row,
    dfname="empty",
    date_range=None,
):
    initial_filter = EHCP_FILTER(df, dfname)
    filtered_df = Overall_Wait_Times_filter(initial_filter, row, dfname, date_range)
    return filtered_df


def CRAVEN_Wait_Times_filter(
    df,
    row,
    dfname="empty",
    date_range=None,
):
    initial_filter = CRAVEN_FILTER(df, dfname)
    filtered_df = Overall_Wait_Times_filter(initial_filter, row, dfname, date_range)
    return filtered_df


def BRADFORD_DISTRICT_Wait_Times_filter(
    df,
    row,
    dfname="empty",
    date_range=None,
):
    initial_filter = BRADFORD_FILTER(df, dfname)
    filtered_df = Overall_Wait_Times_filter(initial_filter, row, dfname, date_range)
    return filtered_df


def Yim_Live_filter(df, row, dfname="empty", date_range=None):
    return df


def KCU_filter(df, row, dfname="empty", date_range=None):
    return df


filter_function_map = {
    "Overall_caseload_and_referrals": OCR_filter,
    "CIC_CLA_caseload_and_referrals": CIC_CLA_caseload_and_referrals_filter,
    "SEN_caseload_and_referrals": SEN_caseload_and_referrals_filter,
    "EHCP_caseload_and_referrals": EHCP_caseload_and_referrals_filter,
    "CRAVEN_caseload_and_referrals": CRAVEN_caseload_and_referrals_filter,
    "BRADFORD_DISTRICT_caseload_and_referrals": BRADFORD_DISTRICT_caseload_and_referrals_filter,
    "All_Referrals_by_demographics": All_Referrals_by_demographics_filter,
    "All_CIC_CLA_Referrals_by_demographics": All_CIC_CLA_Referrals_by_demographics_filter,
    "All_SEN_Referrals_by_demographics": All_SEN_Referrals_by_demographics_filter,
    "All_EHCP_Referrals_by_demographics": All_EHCP_Referrals_by_demographics_filter,
    "All_CRAVEN_Referrals_by_demographics": All_CRAVEN_Referrals_by_demographics_filter,
    "BRADFORD_DISTRICT_Referrals_by_demographics": BRADFORD_DISTRICT_Referrals_by_demographics_filter,
    "Source_of_All_Referrals": Source_of_All_Referrals_filter,
    "Source_of_Referrals_CIC_CLA": Source_of_Referrals___CIC_CLA_filter,
    "Source_of_Referrals_SEN": Source_of_Referrals___SEN_filter,
    "Source_of_Referrals_EHCP": Source_of_Referrals___EHCP_filter,
    "Source_of_Referrals_CRAVEN": Source_of_Referrals___CRAVEN_filter,
    "Source_of_Referrals_BRADFORD_DISTRICT": Source_of_Referrals___BRADFORD_DISTRICT_filter,
    "No_of_CYP_receiving_a_second_attended_contact_with_mental_health_services": No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_filter,
    "DNAs_and_cancellations": DNAs_and_cancellations_filter,
    "Goals_Based_Outcomes": Goals_Based_Outcomes_filter,
    "All_Goal_Themes": All_Goal_Themes_filter,
    "CIC_Goal_Themes": CIC_Goal_Themes_filter,
    "SEN_Goal_Themes": SEN_Goal_Themes_filter,
    "EHCP_Goal_Themes": EHCP_Goal_Themes_filter,
    "CRAVEN_Goal_Themes": CRAVEN_Goal_Themes_filter,
    "Bradford_District_Goal_Themes": Bradford_District_Goal_Themes_filter,
    "Overall_Discharges": Overall_Discharges_filter,
    "Discharges_CIC_CLA": Discharges_CIC_CLA_filter,
    "Discharges_SEN": Discharges_SEN_filter,
    "Discharges_EHCP": Discharges_EHCP_filter,
    "Discharges_CRAVEN": Discharges_CRAVEN_filter,
    "Discharges_BRADFORD_DISTRICT": Discharges_BRADFORD_DISTRICT_filter,
    "Overall_Number_on_Waiting_list": Overall_Number_on_Waiting_list_filter,
    "Overall_Wait_Times": Overall_Wait_Times_filter,
    "CIC_CLA_Wait_Times": CIC_CLA_Wait_Times_filter,
    "SEN_Wait_Times": SEN_Wait_Times_filter,
    "EHCP_Wait_Times": EHCP_Wait_Times_filter,
    "CRAVEN_Wait_Times": CRAVEN_Wait_Times_filter,
    "BRADFORD_DISTRICT_Wait_Times": BRADFORD_DISTRICT_Wait_Times_filter,
    "Yim_Live": Yim_Live_filter,
    "KCU": KCU_filter,
}
