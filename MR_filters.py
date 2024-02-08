# -*- coding: utf-8 -*-
"""
Created on Tues Feb 06 15:58:58 2023

@author: Ed Heywood-Everett
"""
import pandas as pd

def isolate_active_month(df, column, active_month):
    return df

def CIC_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'looked_after_child' column is 'YES'
    filtered_df = df.loc[df['looked_after_child'] == 'YES']
    return filtered_df

def SEN_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'special_education_needs' column is 'YES'
    filtered_df = df.loc[df['special_education_needs'] == 'YES']
    return filtered_df

def EHCP_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'EHCP' column is 'YES'
    filtered_df = df.loc[df['ehcp'] == 'YES']
    return filtered_df

def CRAVEN_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'EHCP' column is 'YES'
    filtered_df = df.loc[df['craven'] == True]
    return filtered_df

def BRADFORD_FILTER(df, df_name="empty"):
    # Filter DataFrame where 'EHCP' column is 'YES'
    filtered_df = df.loc[df['craven'] == False]

    return filtered_df
    

def OCR_filter(df, row, dfname="empty"):
    # isolate active month TODO
    try:
        if row == "Number referrals":
            return df
        elif row == "Number unique referrals":
            df_filtered = df.drop_duplicates(subset="client_id")
            return df_filtered
        elif row == "Referrals accepted":
            return "make checks"
        elif row == "Referrals refused":
            return "make checks"
        elif row == "Number open cases":
            return "make checks"
        elif row == "Number closed cases":
            return "make checks"
        
        return "row not caught"
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )
         
def CIC_CLA_caseload_and_referrals_filter(df, row, dfname="empty"):
    
    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df

def SEN_caseload_and_referrals_filter(df, row, dfname="empty"):

    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df

def EHCP_caseload_and_referrals_filter(df, row, dfname="empty"):

    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df

def CRAVEN_caseload_and_referrals_filter(df, row, dfname="empty"):

    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df

def BRADFORD_DISTRICT_caseload_and_referrals_filter(df, row, dfname="empty"):

    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = OCR_filter(initial_filtered_df, row, dfname)

    return filtered_df

def All_Referrals_by_demographics_filter(df, row, dfname="empty"):
    try:
        # List for age categories
        age_categories = [
            "Age 4", "Age 5", "Age 6", "Age 7", "Age 8", "Age 9", "Age 10",
            "Age 11", "Age 12", "Age 13", "Age 14", "Age 15", "Age 16",
            "Age 17", "Age 18", "Age 19", "Age 20", "Age 21", "Age 22",
            "Age 23", "Age 24", "Age 25", "Out of age range (data input error)"
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
            "African", "Arab", "Bangladeshi", "Caribbean", "Central and Eastern European",
            "Chinese", "Gypsy/Roma/Traveller", "Indian", "Irish", "Latin America",
            "Pakistani", "White and Asian", "White and Black African", "White and Black Carribean",
            "White British", "Any other Asian background", "Any other Black background",
            "Any other Ethnic group", "Any other Mixed background", "Any other White background",
            "Unknown Ethnicity"  
        ]
        
        # Determine the category of 'row' and filter accordingly
        if row in age_categories:
            # Extract the age from the row string, assuming row format is "Age X" where X is the age
            if row.startswith("Age "):
                age = int(row.split(" ")[1])  # Extract age from the row string
                filtered_df = df[df['age'] == age]  # Filter df for rows matching the age
            elif row == "Out of age range (data input error)":
                # Handle out of range ages if necessary, e.g., filter out known invalid ages
                # This part depends on how you want to handle this special case
                filtered_df = df[df['age'] > 25]  # Example: filtering ages greater than 25
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
                mapped_gender = gender_map[row]
                # Filter df for rows matching the mapped gender
                filtered_df = df[df['gender_name'] == mapped_gender]
            else:
                
                # If the row does not represent a gender category, you can choose to return the df as is or handle differently
                return df  # Or: return "Row does not represent a gender category"

        elif row in ethnicity_categories:
            ethnic_map = {
                "African": "Black or Black British - African",
                "Any other Asian background": "Asian or Asian British - Any other Asian background",
                "Any other Black background": "Black or Black British - Any other Black background",
                "Any other Ethnic group": "Other Ethnic Groups - Any other ethnic group",
                "Any other Mixed background": "Mixed - Any other mixed background",
                "Any other White background": "White - Any other White background",
                "Arab": "Arab",
                "Bangladeshi": "Asian or Asian British - Bangladeshi",
                "British": "White - British",
                "Caribbean": "Black or Black British - Caribbean",
                "Central and Eastern European": "Central and Eastern European",
                "Chinese": "Other Ethnic Groups - Chinese",
                "Gypsy/Roma/Traveller": "Gypsy/Roma/Traveller",
                "Indian": "Asian or Asian British - Indian",
                "Irish": "White - Irish",
                "Latin America": "Latin America",
                # "Not known": "Not known", 
                # "Not stated": "Not stated",
                "Pakistani": "Asian or Asian British - Pakistani",
                "White and Asian": "Mixed - White and Asian",
                "White and Black African": "Mixed - White and Black African",
                "White and Black Caribbean": "Mixed - White and Black Caribbean",
                "White British":"White - British",
                # "Blank (nothing selected)": "Blank",
                "Unknown Ethnicity":"Blank",
            }

            mapped_value = ethnic_map.get(row, "Unknown Ethnicity")  # Default to "Unknown Ethnicity" if not found
            if mapped_value == "Blank":
                # Filter for rows where 'client_ethnicity' is NaN
                filtered_df = df[pd.isna(df["ethnicity_name"])]
            else:
                filtered_df =  df[df['ethnicity_name'] == mapped_value]

            return filtered_df
        else:
            return "Row category not recognized"

        return filtered_df  # Return the filtered dataframe
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )
        
        
def All_CIC_CLA_Referrals_by_demographics_filter(df, row, dfname="empty"):
    
    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df

def All_SEN_Referrals_by_demographics_filter(df, row, dfname="empty"):
    
    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df

def All_EHCP_Referrals_by_demographics_filter(df, row, dfname="empty"):
    
    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df

def All_CRAVEN_Referrals_by_demographics_filter(df, row, dfname="empty"):
    
    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df

def BRADFORD_DISTRICT_Referrals_by_demographics_filter(df, row, dfname="empty"):
    
    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = All_Referrals_by_demographics_filter(initial_filtered_df, row, dfname)

    return filtered_df

filter_function_map = {
    "Overall_caseload_and_referrals":OCR_filter,
    "CIC_CLA_caseload_and_referrals":CIC_CLA_caseload_and_referrals_filter,
    "SEN_caseload_and_referrals": SEN_caseload_and_referrals_filter,
    "EHCP_caseload_and_referrals": EHCP_caseload_and_referrals_filter,
    "CRAVEN_caseload_and_referrals":CRAVEN_caseload_and_referrals_filter,
    "BRADFORD_DISTRICT_caseload_and_referrals":BRADFORD_DISTRICT_caseload_and_referrals_filter,
    "All_Referrals_by_demographics":All_Referrals_by_demographics_filter,
    "All_CIC_CLA_Referrals_by_demographics":All_CIC_CLA_Referrals_by_demographics_filter,
    "All_SEN_Referrals_by_demographics":All_SEN_Referrals_by_demographics_filter,
    "All_EHCP_Referrals_by_demographics":All_EHCP_Referrals_by_demographics_filter,
    "All_CRAVEN_Referrals_by_demographics":All_CRAVEN_Referrals_by_demographics_filter,
    "BRADFORD_DISTRICT_Referrals_by_demographics":BRADFORD_DISTRICT_Referrals_by_demographics_filter,
    # "Source_of_All_Referrals":,
    # "Source_of_Referrals___CIC_CLA":,
    # "Source_of_Referrals___SEN":,
    # "Source_of_Referrals___EHCP":,
    # "Source_of_Referrals___CRAVEN":,
    # "Source_of_Referrals___BRADFORD_DISTRICT":,
    # "No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_":,
    # "DNAs_and_cancellations":,
    # "Goals_Based_Outcomes":,
    # "All_Goal_Themes":,
    # "CIC_Goal_Themes":,
    # "SEN_Goal_Themes":,
    # "EHCP_Goal_Themes":,
    # "CRAVEN_Goal_Themes":,
    # "Bradford_District_Goal_Themes":,
    # "Overall_Discharges":,
    # "Discharges___CIC_CLA":,
    # "Discharges___SEN":,
    # "Discharges___EHCP":,
    # "Discharges___CRAVEN":,
    # "Discharges___BRADFORD_DISTRICT":,
    # "Overall_Number_on_Waiting_list__CYP_referred_but_yet_to_attend_1st_appointment_":,
    # "Overall_Wait_Times":,
    # "CIC_CLA_Wait_Times":,
    # "SEN_Wait_Times":,
    # "EHCP_Wait_Times":,
    # "CRAVEN_Wait_Times":,
    # "BRADFORD_DISTRICT_Wait_Times":,
    # "Yim_Live":,
    # "KCU":,
}
