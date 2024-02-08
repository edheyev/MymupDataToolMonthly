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
    

# referalls sheet

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

# demographics sheet

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
                mapped_value = gender_map[row]
                if mapped_value == "Blank":
                    # Filter for rows where 'client_ethnicity' is NaN
                    filtered_df = df[pd.isna(df["gender_name"])]
                else:
                    filtered_df = df[df['gender_name'] == mapped_value]
                
                return filtered_df  # Or: return "Row does not represent a gender category"

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

# referral source sheet

def Source_of_All_Referrals_filter(df, row, dfname="empty"):
    try:
        # Mapping from 'row_names' to 'referral_source' column values in the dataframe
        source_map = {
            "GP services": "Primary Health Care: General Medical Practitioner Practice",
            "Primary care": "Primary care",  # Assuming 'Primary care' fits here
            "Other Primary Health Care": "Other Primary Health Care",
            "Self Referral": "Self-Referral: Self",
            "Self": "Self",
            "Carer": "Self-Referral: Carer/Relative",
            "Social Services": "Local Authority and Other Public Services: Social Services",
            "Education Service": "Local Authority and Other Public Services: Education Service / Educational Establishment",
            "Housing Service": "Local Authority and Other Public Services: Housing Service",
            "Police": "Justice System: Police",
            "Youth Offending Service": "Justice System: Youth Offending Team",
            "School Nurse": "Child Health: School Nurse",
            "Hospital-based Paediatrics": "Child Health: Hospital-based Paediatrics",
            "Community-based Paediatrics": "Child Health: Community-based Paediatrics",
            "Voluntary Sector": "Voluntary Sector",
            "Accident And Emergency Department": "Accident and Emergency Department",
            "Other secondary care specialty": "Other secondary care specialty",
            "Out of Area Agency": "Other: Out of Area Agency",
            "Drug Action Team / Drug Misuse Agency": "Other: Drug Action Team / Drug Misuse Agency",
            "Other service or agency": "Other SERVICE or agency",
            "Single Point of Access Service": "Other: Single Point of Access Service",
            "Internal Referral": "Internal Referral",
            "CAMHS Core/Step down": "CAMHS - Core/Step Down",
            "CAMHS Waiting List": "CAMHS - Waiting List",
            "CAMHS Crisis": "CAMHS - Crisis Team (Hospital Urgents)",
            "Transfer by graduation from Child Adolescent Mental Health Services to Adult": "Transfer by Graduation from CAMHS to Adult Mental Health Services",
            "VCS": "Voluntary Sector",
            "Unknown": "Not Known",

            # Adding missing entries from the old source_map
            "Community Mental Health Team (Adult Mental Health)": "Community Mental Health Team (Adult Mental Health)",
            "Employer": "Employer",
            "Employer: Occupational Health": "Employer: Occupational Health",
            "Family Support Worker": "Family Support Worker",
            "Improving Access to Psychological Therapies Service": "Improving Access to Psychological Therapies Service",
            "Independent Sector: Low secure Inpatients": "Independent Sector: Low secure Inpatients",
            "Independent Sector: Medium secure Inpatients": "Independent Sector: Medium secure Inpatients",
            "Inpatient Service Child and Adult Mental Health": "Inpatient Service Child and Adult Mental Health",
            "Inpatient Service Learning Disabilities": "Inpatient Service Learning Disabilities",
            "Justice System: Court Liaison and Diversion Service": "Justice System: Court Liaison and Diversion Service",
            "Justice System: Courts": "Justice System: Courts",
            "Justice System: Police": "Justice System: Police",
            "Justice System: Prison": "Justice System: Prison",
            "Justice System: Probation": "Justice System: Probation",
            "Justice System: Youth Offending Team": "Justice System: Youth Offending Team",
            "Local Authority and Other Public Services: Education Service / Educational Establishment": "Local Authority and Other Public Services: Education Service / Educational Establishment",
            "Local Authority and Other Public Services: Housing Service": "Local Authority and Other Public Services: Housing Service",
            "Local Authority and Other Public Services: Social Services": "Local Authority and Other Public Services: Social Services",
            "Mental Health Drop In Service": "Mental Health Drop In Service",
            "Not Known": "Not Known",
            "Other Independent Sector Mental Health Services": "Other Independent Sector Mental Health Services",
            "Other: Asylum Services": "Other: Asylum Services",
            "Other: Job Centre Plus": "Other: Job Centre Plus",
            "Other: Single Point of Access Service": "Other: Single Point of Access Service",
            "Other: Urgent and Emergency Care Ambulance Service": "Other: Urgent and Emergency Care Ambulance Service",
            "Permanent Transfer from Another Mental Health Trust": "Permanent Transfer from Another Mental Health Trust",
            "Primary Health Care: Health Visitor": "Primary Health Care: Health Visitor",
            "Primary Health Care: Maternity Service": "Primary Health Care: Maternity Service",
            "Temporary Transfer from Another Mental Health Trust": "Temporary Transfer from Another Mental Health Trust",
            "Blank (nothing selected)": "Blank (nothing selected)",
        }

        # Get the mapped value from the source_map; use a placeholder if the row is not found
        mapped_value = source_map.get(row, "Placeholder for unmapped row")

        # Filter the dataframe based on the referral_source column
        if mapped_value != "Placeholder for unmapped row" and mapped_value != "Blank (nothing selected)":
            # Filter for rows where referral_source matches mapped_value
            filtered_df = df[df['referral_source'] == mapped_value]
        elif mapped_value == "Blank (nothing selected)":
            # Filter for rows where referral_source is NaN or blank
            filtered_df = df[df['referral_source'].isna() | (df['referral_source'] == '')]
        else:
            # If we have a placeholder value, it means the row was not in source_map
            print(f"Row '{row}' not found in source_map. Using unfiltered dataframe.")
            filtered_df = df

        return filtered_df
    except Exception as e:
        print(f"Error in referral_source_filter with row: {row}, {e}. Current df: {dfname}")
        raise Exception(f"Error in referral_source_filter with row: {row}, {e}. Current df is {dfname}")

def Source_of_Referrals___CIC_CLA_filter(df, row, dfname="empty"):
    
    initial_filtered_df = CIC_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df

def Source_of_Referrals___SEN_filter(df, row, dfname="empty"):
    
    initial_filtered_df = SEN_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df

def Source_of_Referrals___EHCP_filter(df, row, dfname="empty"):
    
    initial_filtered_df = EHCP_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df

def Source_of_Referrals___CRAVEN_filter(df, row, dfname="empty"):
    
    initial_filtered_df = CRAVEN_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df

def Source_of_Referrals___BRADFORD_DISTRICT_filter(df, row, dfname="empty"):
    
    initial_filtered_df = BRADFORD_FILTER(df, dfname)
    filtered_df = Source_of_All_Referrals_filter(initial_filtered_df, row, dfname)

    return filtered_df

# two attended contacts sheet

def No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_filter(df, row, dfname="empty"):
    # TODO some extra data cleaning - check pad
    
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

def DNAs_and_cancellations_filter(df, row, dfname="empty"):
    # isolate active month TODO
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
            filtered_df = df[df['attendance'] == "Did not Attend"]
        elif "Cancelled by patient" in row:
            filtered_df = df[df['attendance'] == "Cancelled by Patient"]  # Placeholder, replace with actual value
        elif "Cancelled by Provider" in row:
            filtered_df = df[df['attendance'] == "Cancelled by Provider"]  # Placeholder, replace with actual value
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
    "Source_of_All_Referrals":Source_of_All_Referrals_filter,
    "Source_of_Referrals_CIC_CLA":Source_of_Referrals___CIC_CLA_filter,
    "Source_of_Referrals_SEN":Source_of_Referrals___SEN_filter,
    "Source_of_Referrals_EHCP":Source_of_Referrals___EHCP_filter,
    "Source_of_Referrals_CRAVEN":Source_of_Referrals___CRAVEN_filter,
    "Source_of_Referrals_BRADFORD_DISTRICT":Source_of_Referrals___BRADFORD_DISTRICT_filter,
    "No_of_CYP_receiving_a_second_attended_contact_with_mental_health_services": No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_filter,
    "DNAs_and_cancellations":DNAs_and_cancellations_filter,
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
