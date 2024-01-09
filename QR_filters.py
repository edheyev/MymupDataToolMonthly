# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:58:58 2023

@author: Ed Heywood-Everett
"""
import pandas as pd


def column_filter(df, column, dfname="empty"):
    
    if dfname == "File_Closures_And_Goals_Within_Reporting_Period" or dfname == "MIB_File_Closures_And_Goals_Within_Reporting_Period":
        contact_service = "file_closure_service_type"
    else:
        contact_service = "contact_service_type"
        
    if dfname == "Contacts_Within_Seven_Days" or dfname == "MIB_Contacts_Within_Seven_Days"or dfname == "Contacts_Within_Twenty_One_Days"or dfname == "MIB_Contacts_Within_Twenty_One_Days":
        contact_service = "file_closure_service_type"
    
    try:
        if column == "Q1_Totals":
        # totals calculated in the main script
            pass
        
        elif column == "Barnardos (Wrap)":
            return df[df["franchise"] == "Barnardos WRAP"]
        elif column == "BYS All":
            return df[df["franchise"] == "Bradford Youth Service"]
        elif column == "Brathay Magic":
            return df[
                (df["franchise"] == "Brathay") & (df[contact_service] == "MAGIC")
            ]
        elif column == "INCIC (CYP)":
            return df[
                (df["franchise"] == "Inspired Neighbourhoods")
                & (df[contact_service] == "CYP")
            ]
        elif column == "MIB Know Your Mind":
            return df[df[contact_service] == "Know Your Mind"]
        elif column == "MIB Know Your Mind +":
            return df[df[contact_service] == "Know Your Mind Plus"]
        elif column == "MIB Hospital Buddys Airedale General":
            return df[df[contact_service] == "Hospital Buddies AGH"]
        elif column == "MIB Hospital Buddys BRI":
            return df[df[contact_service] == "Hospital Buddies BRI"]
        elif column == "SELFA (Mighty Minds)":
            return df[
                (df["franchise"] == "Selfa")
                & (df[contact_service] == "Mighty Minds")
            ]
        else:
            print("column not recognised by filters")
            raise Exception(f"Error in reason_for_referral_filter with column {column}: {e} . current df is {dfname}")
            
            return pd.DataFrame()
    except Exception as e:
        print(f"Error in col_filter with column {column}: {e} . current df is {dfname} error: {e}")
        return pd.DataFrame({"error": [True]})  # Return DataFrame with an error flag

def SI_row_filter(df, row, dfname="empty"):
    try:
        mib = True if dfname.startswith("MIB") else False

        if row == "Number of unique people supported":
            if not mib:
                # exclude admin contacts
                df = df[~df["contact_themes"].str.contains("Administrative", na=False)]

                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches).
                contact_approaches = [
                    "Face to Face",
                    "Telephone",
                    "Type talk",
                    "Video consultation",
                    "Instant Messaging (Synchronous)",
                ]
                df_filtered = df[df["contact_approach"].isin(contact_approaches)]

                return df_filtered
            else:
 
                # Exclude rows where 'contact_themes' column contains 'Administrative'
                df = df[~df["contact_themes"].str.contains("Administrative", na=False)]


                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches).
                contact_approaches = [
                    "Face to Face",
                    "Telephone",
                    "Type talk",
                    "Video consultation",
                    "Instant Messaging (Synchronous)",
                ]
                df = df[df["contact_approach"].isin(contact_approaches)]

                # contact session option must be either 'Support Session' or '24 hr call back'
                df = df[
                    df["contact_session_option"].isin(
                        ["Support Session", "24 hour call back"]
                    )
                ]

                return df

        elif row == "How many were declined by the service?":
            # count all unique client ids within reporting period (within file closures db)
            unique_clients_df = df.drop_duplicates(subset='client_id')
            
            return unique_clients_df

        elif (
            row
            == "How many young people disengaged, couldn’t be contacted or rejected a referral?"
        ):
            # Filter by specific file closure reasons and count unique clients
            closure_reasons = [
                "Client did not attend",
                "Client requested discharge",
                "Client disengages",
                "Refused to be seen",
                "Client rejects referral",
                "Client not available for pre-arranged appointments",
                "Organisation cannot contact Client prior to assessment",
                "Client declined a service prior or during assessment",
            ]
            df_filtered = df[df["reason"].isin(closure_reasons)]
            unique_clients_df = df_filtered.drop_duplicates(subset='client_id')
            return unique_clients_df

        elif row == "Active cases":
            # Count clients with no file closure date and status active, pending, processing, or waiting list
            active_statuses = ["Active", "Pending", "Processing", "Waiting List"]
            df_filtered = df[df["client_status"].isin(active_statuses)]
            return df_filtered

        elif row == "How many people have moved on":
            # Filter by specific file closure reasons for moving on and count unique clients
            move_on_reasons = [
                "Planned ending met outcomes at Assessment Point",
                "Planned ending without review",
                "Treatment completed",
                "Decision made at review",
                "No further treatment required",
                "Single episode",
            ]
            df_moved_on = df[df["reason"].isin(move_on_reasons)]
            
            unique_clients_df = df_moved_on.drop_duplicates(subset='client_id')
            
            return unique_clients_df
        
        
        elif row == "% clients with initial contact within 7 days of referral (old rule not including admin contacts)":
            try:
                df_contacts = df
                
                # Drop rows where any of the specified date columns have NaN values
                df_contacts = df_contacts.dropna(subset=['referral_date', 'file_closure_date', 'contact_/_indirect_date'])

                # Exclude clients with file closure reason "organisation cannot contact client prior to assessment"
                df_filtered = df_contacts[df_contacts['file_closure_service_type'] != 'organisation cannot contact client prior to assessment']

                # Error handling for invalid dates
                def safe_convert_date(date_str):
                    try:
                        return pd.to_datetime(date_str)
                    except:
                        return pd.NaT  # Not a Time (NaT) for invalid dates

                df_filtered['file_closure_date'] = df_filtered['file_closure_date'].apply(safe_convert_date)
                df_filtered['referral_date'] = df_filtered['referral_date'].apply(safe_convert_date)
                df_filtered['contact_/_indirect_date'] = df_filtered['contact_/_indirect_date'].apply(safe_convert_date)

                # Drop rows with invalid dates
                df_filtered = df_filtered.dropna(subset=['file_closure_date', 'referral_date', 'contact_/_indirect_date'])

                df_first_contact = df_filtered.groupby('client_id')['contact_/_indirect_date'].min().reset_index()

                df_merged = df_first_contact.merge(df_filtered[['client_id', 'referral_date', 'within_7_days']], on='client_id')

                df_within_7_days = df_merged[df_merged['within_7_days'] == 'Yes']
                
                if df_within_7_days.empty:
                    return (pd.DataFrame(), df_merged)
                elif df_merged.empty:
                    error_message = f"Error in row_filter with row {row}: {e} . current df is {dfname}"
                    print(error_message)
                    return (pd.DataFrame([error_message]), pd.DataFrame([error_message]))

                else:
                    return (df_within_7_days, df_merged)
            except Exception as e:
                print(f"Error in row_filter with row {row}: {e} . current df is {dfname}")
                return (pd.DataFrame(), pd.DataFrame())  # Return empty DataFrames in case of an error
            
        elif row == "% clients who had the first support session offered within 21 days of referral":
            # Error handling for invalid dates
            def safe_convert_date(date_str):
                try:
                    return pd.to_datetime(date_str)
                except:
                    return pd.NaT  # Not a Time (NaT) for invalid dates

            try:
                # Define excluded file closure reasons
                excluded_closure_reasons = [
                    'organisation cannot contact client prior to assessment',
                    'client rejects referral',
                    'organisation rejects referral threshold too high',
                    'organisation rejects referral referral not suitable pre/post assessment'
                ]

                # Define qualifying contact approaches
                qualifying_approaches = [
                    'Face to Face', 'Telephone', 'Talk Type', 'Video', 'Instant Messaging Synchronous'
                ]

                # Drop rows with NaN in essential columns and explicitly create a copy
                df_filtered = df.dropna(subset=['referral_date', 'file_closure_date', 'contact_/_indirect_date']).copy()

                # Exclude clients with specified file closure reasons
                # df_filtered = df_filtered[~df_filtered['file_closure_reason'].isin(excluded_closure_reasons)]

                # Convert date strings to datetime objects, handling errors safely
                df_filtered['file_closure_date'] = df_filtered['file_closure_date'].apply(safe_convert_date)
                df_filtered['referral_date'] = df_filtered['referral_date'].apply(safe_convert_date)
                df_filtered['contact_/_indirect_date'] = df_filtered['contact_/_indirect_date'].apply(safe_convert_date)

                # Drop rows with invalid dates
                df_filtered = df_filtered.dropna(subset=['file_closure_date', 'referral_date', 'contact_/_indirect_date'])

                # Filter for qualifying contact approaches
                df_filtered = df_filtered[df_filtered['contact_approach'].isin(qualifying_approaches)]

                # Group by client_id to find the first qualifying contact date
                df_first_contact = df_filtered.groupby('client_id')['contact_/_indirect_date'].min().reset_index()

                # Merge with original dataframe to get referral dates and within 21 days flag
                df_merged = df_first_contact.merge(df_filtered[['client_id', 'referral_date', 'within_21_days']], on='client_id')

                # Filter for clients whose first contact was within 21 days of referral
                df_within_21_days = df_merged[df_merged['within_21_days'] == 'Yes']

                if df_within_21_days.empty:
                    return (pd.DataFrame(), df_merged)
                elif df_merged.empty:
                    return (pd.DataFrame([error_message]), pd.DataFrame([error_message]))

                return (df_within_21_days, df_merged)
            except Exception as e:
                print(f"Error in filter_clients_first_support_session_offered: {e}")
                return (pd.DataFrame(), pd.DataFrame())  # Return empty DataFrames in case of an error

        elif row == "% clients attended the first contact by video/face to face/telephone within 21 days of referral":
            # Error handling for invalid dates
            def safe_convert_date(date_str):
                try:
                    return pd.to_datetime(date_str)
                except:
                    return pd.NaT  # Not a Time (NaT) for invalid dates

            try:
                # Define excluded file closure reasons
                excluded_closure_reasons = [
                    'organisation cannot contact client prior to assessment',
                    'client rejects referral',
                    'organisation rejects referral threshold too high',
                    'organisation rejects referral referral not suitable pre/post assessment'
                ]

                # Define qualifying contact approaches and attendance status
                qualifying_approaches = [
                    'Face to Face', 'Telephone', 'Talk Type', 'Video', 'Instant Messaging Synchronous'
                ]
                qualifying_attendance_status = ['Attended']  # Only include 'Attended' status

                # Explicitly create a copy of the DataFrame to avoid SettingWithCopyWarning
                df_filtered = df.dropna(subset=['referral_date', 'file_closure_date', 'contact_/_indirect_date']).copy()

                # Exclude clients with specified file closure reasons
                # df_filtered = df_filtered[~df_filtered['file_closure_reason'].isin(excluded_closure_reasons)]

                # Convert date strings to datetime objects, handling errors safely
                df_filtered['file_closure_date'] = df_filtered['file_closure_date'].apply(safe_convert_date)
                df_filtered['referral_date'] = df_filtered['referral_date'].apply(safe_convert_date)
                df_filtered['contact_/_indirect_date'] = df_filtered['contact_/_indirect_date'].apply(safe_convert_date)

                # Drop rows with invalid dates
                df_filtered = df_filtered.dropna(subset=['file_closure_date', 'referral_date', 'contact_/_indirect_date'])

                # Filter for qualifying contact approaches and attendance status
                df_filtered = df_filtered[df_filtered['contact_approach'].isin(qualifying_approaches) & 
                                        df_filtered['attendance_code'].isin(qualifying_attendance_status)]

                # Group by client_id to find the first qualifying contact date
                df_first_contact = df_filtered.groupby('client_id')['contact_/_indirect_date'].min().reset_index()

                # Merge with original dataframe to get referral dates and within 21 days flag
                df_merged = df_first_contact.merge(df_filtered[['client_id', 'referral_date', 'within_21_days']], on='client_id')

                # Filter for clients whose first contact was within 21 days of referral
                df_within_21_days = df_merged[df_merged['within_21_days'] == 'Yes']
                # print(len(df_within_21_days), len(df_merged))
                if df_within_21_days.empty:
                    return (pd.DataFrame(), df_merged)
                elif df_merged.empty:
                    return (pd.DataFrame([error_message]), pd.DataFrame([error_message]))

                return (df_within_21_days, df_merged)
            except Exception as e:
                print(f"Error in row_filter with row {row}: {e}")
                return (pd.DataFrame(), pd.DataFrame())  # Return empty DataFrames in case of an error

        else:
            print("Row not recognised by filters")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in row_filter with row {row}: {e} . current df is {dfname}")
    return None

def gender_category_filter(df, row, dfname="empty"):
    gender_map = {
        "Female (including Transgender Woman)": "Female (including Transgender Woman)",
        "Male (including Transgender Man)": "Man (including Transgender Man)",
        "Non-Binary": "Non-Binary",
        "Not known (Person stated Gender Code not recorded)": "Not Known (not recorded)",
        "No Stated (patient asked but declined to provide a response)": "Not Stated (patient asked but declined to provide a response)",
        "Prefer not to say": "Prefer not to say",
        "Transgendered": "Transgendered",
        "Other (not listed)": "Other (not listed)",
        "Blank (nothing selected)": "Blank"  # Special handling for blank entries
    }

    def filter_logic(mapped_value):
        if mapped_value == "Blank":
            # Filter for rows where 'client_disability' is NaN
            return df[pd.isna(df['client_gender'])]
        return df[df['client_gender'] == mapped_value]

    try:
        mapped_value = gender_map.get(row)
        if mapped_value is not None:
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in gender_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in gender_category_filter with row {row}: {e}. Current df: {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error

def ethnic_category_filter(df, row, dfname="empty"):
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
        "Latin America": "Latin America",  # Not found in the data
        "Not known": "Not known",
        "Not stated": "Not stated",
        "Pakistani": "Asian or Asian British - Pakistani",
        "White and Asian": "Mixed - White and Asian",
        "White and Black African": "Mixed - White and Black African",
        "White and Black Caribbean": "Mixed - White and Black Caribbean",
        "Blank (nothing selected)": "Blank"  # Special handling for blank entries
    }
    
    def filter_logic(mapped_value):
        if mapped_value == "Blank":
            # Filter for rows where 'client_disability' is NaN
            return df[pd.isna(df['client_ethnicity'])]
        return df[df['client_ethnicity'] == mapped_value]

    try:
        mapped_value = ethnic_map.get(row)
        if mapped_value is not None:
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in ethnicity_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in ethnicity_category_filter with row {row}: {e}. Current df: {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error

def disability_category_filter(df, row, dfname="empty"):
    disability_map = {
        "Autism or other Neurological condition": "Autism or other Neurological condition",
        "Behaviour and Emotional": "Behaviour and Emotional",
        "Hearing": "Hearing",
        "Manual Dexterity": "Manual Dexterity",  # Not found in the data
        "Memory or ability to concentrate, learn or understand (Learning Disability)": "Memory or ability to concentrate, learn or understand (Learning Disability)",
        "Mobility and Gross Motor": "Mobility and Gross Motor",
        "No disability": "No disability",
        "Not Known": "Not Known",
        "Not stated (Person asked but declined to provide a response)": "Not stated (Person asked but declined to provide a response)",
        "Other": "Other (not listed)",  
        "Perception of Physical Danger": "Perception of Physical Danger",  # Not found in the data
        "Personal, Self-Care and Continence": "Personal, Self Care and Continence",  # Not found in the data
        "Progressive Conditions and Physical Health (such as HIV, Cancer, Multiple Sclerosis, Fits)": "Progressive Conditions and Physical Health (such as HIV, cancer, multiple sclerosis, fits etc)", 
        "Sight": "Sight",
        "Speech": "Speech",
        "Yes": "Yes",
        "Blank (nothing selected)": "Blank"  # Special handling for blank entries
    }

    def filter_logic(mapped_value):
        if mapped_value == "Blank":
            # Filter for rows where 'client_disability' is NaN
            return df[pd.isna(df['client_disability'])]
        return df[df['client_disability'] == mapped_value]

    try:
        mapped_value = disability_map.get(row)
        if mapped_value is not None:
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in disability_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        
        print(f"Error in disability_category_filter with row {row}: {e}. Current df: {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error

def sexual_orientation_filter(df, row, dfname="empty"):
    sexuality_map = {
        "Asexual": "Asexual",
        "Bisexual": "Bisexual",
        "Gay": "Gay",
        "Heterosexual or Straight": "Heterosexual or Straight",
        "Lesbian": "Lesbian",
        "Not asked/Unknown": "Not asked/Unknown",
        "Not stated (Person asked but declined to provide a response)": "Not stated (Person asked but declined to provide a response)",
        "Other": "Other",
        "Pansexual": "Pansexual",
        "Person asked and did not know/is unsure or undecided": "Person asked and did not know/is unsure or undecided",
        "Blank (nothing selected)": "Blank"  # Special handling for blank entries
    }
    
    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_sexuality'])]
        return df[df['client_sexuality'] == mapped_value]

    try:
        mapped_value = sexuality_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in sexual_orientation_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in sexual_orientation_filter with row {row}: {e}. Current df: {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error

def age_category_filter(df, row, dfname="empty"):
    age_groups = {
        "Age 4": 4, "Age 5": 5, "Age 6": 6, "Age 7": 7, "Age 8": 8, "Age 9": 9,
        "Age 10": 10, "Age 11": 11, "Age 12": 12, "Age 13": 13, "Age 14": 14,
        "Age 15": 15, "Age 16": 16, "Age 17": 17, "Age 18": 18, "Age 19": 19,
        "Age 20": 20, "Age 21": 21, "Age 22": 22, "Age 23": 23, "Age 24": 24,
        "Age 25": 25, "Out of age Range": None
    }

    def filter_logic(age):
        if age is None:
            # Handling "Out of age Range" by filtering ages not in the specified range
            specified_ages = list(age_groups.values())
            specified_ages.remove(None)
            return df[~df['client_age'].isin(specified_ages)]
        return df[df['client_age'] == age]
    try:
        age = age_groups.get(row)
        if age is not None or row == "Out of age Range":
            return filter_logic(age)
        else:
            print(f"Row '{row}' not recognised in age_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in age_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def area_category_filter(df, row, dfname="empty"):
    area_map = {
        "BAILDON": "BAILDON",
        "Bentham": "Bentham",
        "BINGLEY": "BINGLEY",
        "BINGLEY RURAL": "BINGLEY RURAL",
        "BOLTON & UNDERCLIFFE": "BOLTON & UNDERCLIFFE",
        "BOWLING & BARKEREND": "BOWLING & BARKEREND",
        "BRADFORD MOOR": "BRADFORD MOOR",
        "CITY": "CITY",
        "CLAYTON & FAIRWEATHER GREEN": "CLAYTON & FAIRWEATHER GREEN",
        "CRAVEN": "CRAVEN",
        "Craven Ward - Aire Valley-with-Lothersdale": "Craven Ward - Aire Valley-with-Lothersdale",
        "Craven Ward - Barden Fell": "Craven Ward - Barden Fell",
        "Craven Ward - Cowling": "Craven Ward - Cowling",
        "Craven Ward - Embsay-with-Eastby": "Craven Ward - Embsay-with-Eastby",
        "Craven Ward - Gargrave and Malhamdale": "Craven Ward - Gargrave and Malhamdale",
        "Craven Ward - Glusburn": "Craven Ward - Glusburn",
        "Craven Ward - Grassington": "Craven Ward - Grassington",
        "Craven Ward - Hellifield and Long Preston": "Craven Ward - Hellifield and Long Preston",  
        "Craven Ward - Penyghent": "Craven Ward - Penyghent",
        "Craven Ward - Settle and Ribblebanks": "Craven Ward - Settle and Ribblebanks",
        "Craven Ward - Skipton North": "Craven Ward -  Skipton North",
        "Craven Ward - Skipton West": "Craven Ward -  Skipton West",
        "Craven Ward - Skipton East": "Craven Ward -  Skipton East",
        "Craven Ward - Skipton South": "Craven Ward -  Skipton South",
        "Craven Ward - Sutton-in-Craven": "Craven Ward -  Sutton-in-Craven",
        "Craven Ward - Upper Wharfedale": "Craven Ward - Upper Wharfedale",
        "Craven Ward - West Craven": "Craven Ward - West Craven",
        "ECCLESHILL": "ECCLESHILL",
        "GREAT HORTON": "GREAT HORTON",
        "HEATON": "HEATON",
        "IDLE & THACKLEY": "IDLE & THACKLEY",
        "ILKLEY": "ILKLEY",
        "KEIGHLEY CENTRAL": "KEIGHLEY CENTRAL",
        "KEIGHLEY EAST": "KEIGHLEY EAST",
        "KEIGHLEY WEST": "KEIGHLEY WEST",
        "LITTLE HORTON": "LITTLE HORTON",
        "MANNINGHAM": "MANNINGHAM",
        "OUT OF AREA": "OUT OF AREA",
        "QUEENSBURY": "QUEENSBURY",
        "ROYDS": "ROYDS",
        "SHIPLEY": "SHIPLEY",
        "THORNTON & ALLERTON": "THORNTON & ALLERTON",
        "TOLLER": "TOLLER",
        "TONG": "TONG",
        "WHARFEDALE": "WHARFEDALE",
        "WIBSEY": "WIBSEY",
        "WINDHILL & WROSE": "WINDHILL & WROSE",
        "WORTH VALLEY": "WORTH VALLEY",
        "WYKE": "WYKE",
        "Blank (nothing selected )": None  # Special handling for blank entries
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_area'])]
        return df[df['client_area'] == mapped_value]

    try:
        mapped_value = area_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected )":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in area_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in area_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def asylum_status_filter(df, row, dfname="empty"):
    asylum_seeker_map = {
        "Yes": "Yes",
        "No": "No",
        "Not known": "Unknown",  
        "Blank (nothing selected )": None  
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_asylum_seeker'])]
        return df[df['client_asylum_seeker'] == mapped_value]

    try:
        mapped_value = asylum_seeker_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected )":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in asylum_status_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in asylum_status_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def sen_category_filter(df, row, dfname="empty"):
    sen_map = {
        "No": "No",
        "Not known": "Not Known",
        "Yes": "Yes",
        "Not applicable": "Not Applicable",
        "Blank (nothing selected )": None
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_sen'])]
        return df[df['client_sen'] == mapped_value]

    try:
        mapped_value = sen_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected )":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in sen_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in sen_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error

def ehcp_category_filter(df, row, dfname="empty"):
    ehcp_map = {
        "No": "No",
        "Not known": "Not Known",
        "Yes": "Yes",
        "Not applicable": "Not Applicable",
        "Blank (nothing selected )": None
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_ehcp'])]
        return df[df['client_ehcp'] == mapped_value]

    try:
        mapped_value = ehcp_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected )":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in ehcp_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in ehcp_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def at_risk_exploitation_filter(df, row, dfname="empty"):
    are_map = {
        "No": "No",
        "Not known": "Unknown",
        "Yes": "Yes",
        "Blank (nothing selected )": None
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_exploitation_risk'])]
        return df[df['client_exploitation_risk'] == mapped_value]

    try:
        mapped_value = are_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected )":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in at_risk_exploitation_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in at_risk_exploitation_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def leaving_care_filter(df, row, dfname="empty"):
    lc_map = {
        "Yes": "Yes",
        "No": "No",
        "Not Known": "Unknown",  # Adjusted to match the row name
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_leaving_care'])]
        return df[df['client_leaving_care'] == mapped_value]

    try:
        mapped_value = lc_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in leaving_care_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in leaving_care_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def lac_category_filter(df, row, dfname="empty"):
    lac_map = {
        "Yes": "Yes (Is a child looked after)",
        "No": "No (Is not a child looked after)",
        "Not known": "Not Known",
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_lac'])]
        return df[df['client_lac'] == mapped_value]

    try:
        mapped_value = lac_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in lac_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in lac_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def cpp_category_filter(df, row, dfname="empty"):
    cpp_map = {
        "No": "No",
        "Has never been subject to a plan": "Has never been subject to a plan",
        "Not known": "Not Known",
        "Has been previously subject to a plan": "Has been previous subject to a plan",  # Adjusted to match dataset
        "Is currently subject to a plan": "Is currently subject to a plan",
        "Under assessment": "Under assessment",  # Not found in your dataset
        "Blank (nothing selected)": None  # Handling for blank entries
    }


    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_cpp'])]
        return df[df['client_cpp'] == mapped_value]

    try:
        mapped_value = cpp_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in cpp_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in cpp_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def cinp_category_filter(df, row, dfname="empty"):
    cinp_map = {
        "Is currently subject to a Child in need plan": "Is currently subject to a Children In Need Plan",
        "No": "No",
        "Has never been subject to a Child in need plan": "Has never been subject to a Children In Need Plan",
        "Not known": "Not known",
        "Has previously been subject to a Child in need plan": "Has previously been subject to a Children In Need Plan",
        "Under assessment": "Under Assessment", 
        "Blank (nothing selected)": None  # Handling for blank entries
    }
    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_cinp'])]
        return df[df['client_cinp'] == mapped_value]

    try:
        mapped_value = cinp_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in cinp_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in cinp_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def young_carer_category_filter(df, row, dfname="empty"):
    young_carer_map = {
        "Yes": "Yes - child or young PERSON has a caring role for an ill or disabled parent, carer or sibling",
        "No": "No - child or young PERSON does not have a caring role for an ill or disabled parent, carer or sibling",
        "Not known": "Not Known",
        "Not stated": "Not Stated (Person asked but declined to provide a response)",
        "Blank (nothing selected)": None  # Handling for blank entries
    }


    def filter_logic(mapped_value):
        if mapped_value is None:
            return df[pd.isna(df['client_young_carer'])]
        return df[df['client_young_carer'] == mapped_value]

    try:
        mapped_value = young_carer_map.get(row)
        if mapped_value is not None or row == "Blank (nothing selected)":
            return filter_logic(mapped_value)
        else:
            print(f"Row '{row}' not recognised in young_carer_category_filter. Current df: {dfname}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    except Exception as e:
        print(f"Error in young_carer_category_filter with row {row}: {e}. Current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame in case of error


def attended_contacts_filter(df, row, dfname="empty"):
    is_mib = dfname.startswith("MIB")

    if row == "Total Number of Attended Contacts":
        return total_attended_contacts(df, is_mib)

    elif row == "One to One Contacts":
        initial_filtering = total_attended_contacts(df, is_mib)
        if is_mib:
            session_types = ["1 to 1", "2 to 1"]
            return initial_filtering[initial_filtering['contact_session_type'].isin(session_types)]
        else:
            return initial_filtering[initial_filtering['contact_therapy_mode'] == 'Individual patient']

    elif row == "Group Contacts":
        initial_filtering = total_attended_contacts(df, is_mib)
        if is_mib:
            return initial_filtering[(initial_filtering['contact_session_type'] == 'Group')]
        else:
            return initial_filtering[(initial_filtering['contact_therapy_mode'] == 'group therapy')]



    elif row == "Indirect Activities":
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        df = df[df['contact_attendance'] == 'Attended']
        # Filter for rows where 'indirect service type' is not empty or NA
        indirect_approaches = ["Email", "Text Message (Asynchronous)"]
        dfout = df[df['contact_approach'].isin(indirect_approaches)]

        return dfout

    elif row == "Other (email and text)":
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        df = df[df['contact_attendance'] == 'Attended']
        other_approachs = ["Email", "Text Message (Asynchronous)", "Chat Room (Asynchronous)","Message Board (Asynchronous)" "Chat Room (Asynchronous)", "Instant Messaging (Asynchronous)", "Other (not listed)"]
        dfout = df[df['contact_approach'].isin(other_approachs)]
        return dfout
        
        
    elif row == "Admin Contacts":
        if is_mib:
            dfout = df[df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            dfout = df[df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        return dfout

    elif row == "Total number of DNA Contacts":
        # MIB-specific or general filters
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
            df = df[df['contact_service_type'] == 'Know Your Mind'] # not sure about this
            contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
            df = df[df['contact_approach'].isin(contact_approaches)]
            # Include additional MIB-specific filters here
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
            contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
            df = df[df['contact_approach'].isin(contact_approaches)]
            # Include additional general filters here.
        dfout = df[df['contact_attendance'] == 'Did not Attend']
        
        return dfout



    elif row == "Percentage of DNA Contacts":
       # MIB-specific or general filters
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
            df = df[df['contact_service_type'] == 'Know Your Mind'] # not sure about this
            contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
            df = df[df['contact_approach'].isin(contact_approaches)]
            # Include additional MIB-specific filters here
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
            contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
            df = df[df['contact_approach'].isin(contact_approaches)]
            # Include additional general filters here.
        dftotal = df
        dfdna = df[df['contact_attendance'] == 'Did not Attend']
        
        if len(dftotal) == 0:
            return (pd.DataFrame(), dftotal)
        else:
            return (dfdna, dftotal)
    
    else:
        print("Row not recognised by filters: " + row)
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

    return pd.DataFrame()  # Fallback return for unexpected cases

def total_attended_contacts(df, is_mib):
    # Common filters
    df = df[df['contact_attendance'] == 'Attended']

    # MIB-specific or general filters
    if is_mib:
        df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        df = df[df['contact_service_type'] == 'Know Your Mind'] # not sure about this
        contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
        df = df[df['contact_approach'].isin(contact_approaches)]
        # Include additional MIB-specific filters here
    else:
        df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video", "Instant Messaging (Synchronous)"]
        df = df[df['contact_approach'].isin(contact_approaches)]
        # Include additional general filters here

    return df

def goals_based_outcomes_filter(df, row, dfname="empty"):
    pass

def average_goals_based_outcomes_filter(df, row, dfname="empty"):
    
    is_mib = dfname.startswith("MIB")
    
        
    def convert_dates(df, date_columns):
        for column in date_columns:
            df[column] = pd.to_datetime(df[column], errors='coerce')
        return df.dropna(subset=date_columns)
    
    def merge_and_filter_gbo(df_initial, df_followup_final):
        # Merging the initial and follow-up/final GBOs on client_id and goal_id
        df_paired_gbo = pd.merge(df_initial, df_followup_final, on=['client_id', 'goal_id'], suffixes=('_initial', '_followup_final'))
        
        # Filtering the paired GBOs based on the date criteria
        df_paired_gbo = df_paired_gbo[
            (df_paired_gbo['goal_score_date_initial'] >= df_paired_gbo['referral_date_initial']) & 
            (df_paired_gbo['goal_score_date_initial'] <= df_paired_gbo['file_closure_date_initial']) &
            (df_paired_gbo['goal_score_date_followup_final'] <= df_paired_gbo['file_closure_date_followup_final'])
        ]
        
        return df_paired_gbo
    
    def filter_for_reliable_change(df_paired_gbo):
        """
        Filters the DataFrame of paired GBOs to identify cases with reliable change.
        A reliable change is defined as a change of +3 or more in the average scores 
        from the initial to the follow-up/final GBO.
    
        :param df_paired_gbo: DataFrame containing paired initial and follow-up/final GBOs.
        :return: DataFrame with GBOs showing a reliable change.
        """
         # Drop rows where the precalculated change column is null
        df_paired_gbo = df_paired_gbo.dropna(subset=['t1_to_t2_change_followup_final'])
    
        # Filter for GBOs that show a reliable change of +3 or more
        # Assuming a positive value indicates improvement
        df_reliable_change = df_paired_gbo[df_paired_gbo['t1_to_t2_change_followup_final'] >= 3]
    
        return df_reliable_change

    def add_average_column(df):
        
        # Ensure the columns exist and are not null
        if 't1_average_followup_final' in df.columns and 't2_average_followup_final' in df.columns:
            # Calculate the average of the two columns
            df['average_t1_t2'] = (df['t1_average_followup_final'] + df['t2_average_followup_final']) / 2
        else:
            print("Required columns are not available in the DataFrame")
        return df



    if row == "% of closed cases that have an initial and follow-up/final paired GBO":

        try:
            

            # Drop rows with missing 'referral_date' or 'reason'
            df_filtered = df.dropna(subset=['referral_date', 'reason', 'goal_score_date', 'file_closure_date'])
          

            # Check for any remaining missing values
            if df_filtered['referral_date'].isnull().any() or df_filtered['reason'].isnull().any():

                return (pd.DataFrame(), pd.DataFrame())

            # Define the file closure reason for selection
            file_closure_reason = 'Treatment completed'

            # Filter for the specified file closure reason
            df_filtered = df_filtered[df_filtered['reason'] == file_closure_reason]

            # Convert dates safely
            for column in ['goal_score_date', 'referral_date', 'file_closure_date']:
                df_filtered.loc[:, column] = pd.to_datetime(df_filtered[column], errors='coerce')

            # Drop rows with invalid dates
            df_filtered = df_filtered.dropna(subset=['goal_score_date', 'referral_date', 'file_closure_date'])

            # Check if there are rows left to process
            if df_filtered.empty:

                return (pd.DataFrame(), pd.DataFrame())

            # Filter for initial and follow-up/final GBOs
            df_initial_gbo = df_filtered[df_filtered['initial_/_followup_/_final'] == 'Initial']
            df_followup_final_gbo = df_filtered[df_filtered['initial_/_followup_/_final'].isin(['Follow up', 'Final'])]


            # Merge and filter paired GBOs
            df_paired_gbo = merge_and_filter_gbo(df_initial_gbo, df_followup_final_gbo)
            
            
            
            

            return (df_paired_gbo, df_filtered)
        
        except Exception as e:
            print(f"Error in processing paired GBO: {e}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return (pd.DataFrame(), pd.DataFrame())

            


    elif row == "% of closed cases with reliable change in paired GBO":
        try:
            # Drop rows with missing 'referral_date' or 'reason'
            df_filtered = df.dropna(subset=['referral_date', 'reason', 'goal_score_date', 'file_closure_date'])
          

            # Check for any remaining missing values
            if df_filtered['referral_date'].isnull().any() or df_filtered['reason'].isnull().any():

                return (pd.DataFrame(), pd.DataFrame())

            # Define the file closure reason for selection
            file_closure_reason = 'Treatment completed'

            # Filter for the specified file closure reason
            df_filtered = df_filtered[df_filtered['reason'] == file_closure_reason]

            # Convert dates safely
            for column in ['goal_score_date', 'referral_date', 'file_closure_date']:
                df_filtered.loc[:, column] = pd.to_datetime(df_filtered[column], errors='coerce')

            # Drop rows with invalid dates
            df_filtered = df_filtered.dropna(subset=['goal_score_date', 'referral_date', 'file_closure_date'])

            # Check if there are rows left to process
            if df_filtered.empty:
                return (pd.DataFrame(), pd.DataFrame())

            # Filter for initial and follow-up/final GBOs
            df_initial_gbo = df_filtered[df_filtered['initial_/_followup_/_final'] == 'Initial']
            df_followup_final_gbo = df_filtered[df_filtered['initial_/_followup_/_final'].isin(['Follow up', 'Final'])]


            # Merge and filter paired GBOs
            df_paired_gbo = merge_and_filter_gbo(df_initial_gbo, df_followup_final_gbo)
            
            # Filter for GBOs with reliable change
            df_reliable_change_gbo = filter_for_reliable_change(df_paired_gbo)
        
            # The filtered DataFrame for GBOs with reliable change
            result_reliable_change = df_reliable_change_gbo
        
            
            return (result_reliable_change, df_paired_gbo)
            
            
        except Exception as e:
            print(f"Error in filtering GBOs for reliable change: {e}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            result_reliable_change = pd.DataFrame()

    elif row == "Average impact score of all paired goals":
        
        try:
            # Drop rows with missing 'referral_date' or 'reason'
            df_filtered = df.dropna(subset=['referral_date', 'reason', 'goal_score_date', 'file_closure_date'])
          

            # Check for any remaining missing values
            if df_filtered['referral_date'].isnull().any() or df_filtered['reason'].isnull().any():

                return (pd.DataFrame(), pd.DataFrame())

            # Define the file closure reason for selection
            file_closure_reason = 'Treatment completed'

            # Filter for the specified file closure reason
            df_filtered = df_filtered[df_filtered['reason'] == file_closure_reason]

            # Convert dates safely
            for column in ['goal_score_date', 'referral_date', 'file_closure_date']:
                df_filtered.loc[:, column] = pd.to_datetime(df_filtered[column], errors='coerce')

            # Drop rows with invalid dates
            df_filtered = df_filtered.dropna(subset=['goal_score_date', 'referral_date', 'file_closure_date'])

            # Check if there are rows left to process
            if df_filtered.empty:
                return (pd.DataFrame(), "NULL")

            # Filter for initial and follow-up/final GBOs
            df_initial_gbo = df_filtered[df_filtered['initial_/_followup_/_final'] == 'Initial']
            df_followup_final_gbo = df_filtered[df_filtered['initial_/_followup_/_final'].isin(['Follow up', 'Final'])]


            # Merge and filter paired GBOs
            df_paired_gbo = merge_and_filter_gbo(df_initial_gbo, df_followup_final_gbo)
            

            
            df_with_average = add_average_column(df_paired_gbo)
        
            return (df_with_average, "average_t1_t2")
            
            
        except Exception as e:
            print(f"Error in filtering GBOs for reliable change: {e}")
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            result_reliable_change = pd.DataFrame()
        
        pass

    else:
        print(f"Row not recognised: {row}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return "error"

    return "result after filtering"

def goal_themes_filter(df, row, dfname="empty"):
    
    theme_map = {
    "Being able to maintain and build positive relationships":"Being able to maintain and build positive relationships",
    "Being able to support others":"Being able to support others",
    "Being better at managing my emotional wellbeing":"Being better at managing my emotional wellbeing",
    "Being better at managing risks and feeling safer":"Being better at managing risks and feeling safer",
    "Covid-19 Support":"Covid-19 Support",
    "Improving my confidence and self-esteem":"Improving my confidence and self esteem",
    "Improving my physical wellbeing":"Improving my physical wellbeing",
    "Reducing my isolation":"Reducing my isolation",
    "Understanding who I am":"Understanding who I am",}
    
    
        
    try:
        if row in theme_map:
            if theme_map[row] is not None:
                this_theme_df = df[df['goal_themes'] == theme_map[row]]
            elif row == "Blank (nothing selected )":
                # Counting rows where 'client area' is NaN
                this_theme_df = df[df['goal_themes'].isna()]
        else:
            print("Row not recognised by filters: " + row)
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
            
            return "error"
        
        return this_theme_df

    except Exception as e:
        print(f"Error in area_category_filter with row {row}: {e} . current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        
        return "error"

def dss_goal_filter(df, row, dfname="empty"):

    if row == "How many unique clients have had a distress scale score in reporting period":
        return "to do"

    elif row == "Average change score for distress scale":
        return "to do"

    else:
        print(f"Row not recognised: {row}")
        return "error"

def contact_by_theme_filter(df, row, dfname="empty"):
    theme_map = {        
    "Abuse / exploitation":"Abuse / exploitation",
    "Administrative":"Administrative",
    "Activities / opportunities":"Activities / opportunities",
    "Anger":"Anger issues",
    "Anxiety / stress":"Anxiety / stress",
    "Bereavement / grief / loss":"Bereavement / grief / loss",
    "Boyfriend / girlfriend relationships":"Boyfriend / girlfriend relationships",
    "Bullying":"Bullying",
    "Caring for others":"Caring for others", 
    "Covid-19 support":"Covid-19 support",
    "Depression / low mood":"Depression / low mood",
    "Domestic abuse":"Domestic abuse",
    "Eating difficulties":"Eating difficulties",
    "Family relationships / home life":"Family relationships / home life",
    "Finances / debt /poverty":"Finances / debt /poverty",
    "Friendships":"Friendships",
    "Harm to others":"Harm to others",
    "Hearing Voices":"Hearing voices",
    "Homelessness":"Homelessness",
    "Identity issues":"Identity issues",
    "Ill Health":"Ill health",
    "In Crisis/De-escalation":"In Crisis/De-escalation",
    "Issues with medication":"Issues with medication",
    "Loss Job/house":"Loss of job/house",
    "Loneliness / isolation":"Loneliness / isolation",
    "Low confidence / self-worth":" Low confidence / self worth",
    "Low mood":"Low mood",
    "Neurodevelopmental issues":"Neurodevelopmental issues",
    "OCD":"OCD",
    "Offending behaviour":"Offending behaviour",
    "Panic":"Panic",
    "Phobias":"Phobias",
    "Physical health / illness / disability":"Physical health / illness / disability",
    "Psychosis / psychotic episodes":"Psychosis / psychotic episodes",
    "PTSD":"PTSD",
    "School / college / employment":"School / college / employment",
    "Self-Care":"Self Care",
    "Self-Harm":"Self Harm",
    "Sexual Violence":"Sexual violence",# not found in data
    "Sleep problems":"Sleep problems",
    "Substance Misuse":"Substance Misuse",
    "Suicidal Ideation":"Suicidal Ideation",
    "Transition":"Transition",
    "Trauma":"Trauma",
    }
    try:
      if row in theme_map:
          if theme_map[row] is not None:
              themes = theme_map[row].split(', ')
              df.loc[df['contact_themes'].isna(), 'contact_themes'] = ''
              this_theme_df = df[df['contact_themes'].str.contains('|'.join(themes))]
          elif row == "Blank (nothing selected)":
              this_theme_df = df[df['contact_themes'].isna()]
      else:
          print("Row not recognized by filters: " + row)
          return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

      return this_theme_df
  
    except Exception as e:
        print("An error occurred:", str(e))
        return pd.DataFrame()  # Return empty DataFrame in case of error


def source_of_referral_filter(df, row, dfname="empty"):
    reason_map = {
        "Primary Health Care: General Medical Practitioner Practice": "Primary Health Care: General Medical Practitioner Practice",
        "Accident and Emergency Department": "Accident and Emergency Department",
        "CAMHS - Core/Step Down": "CAMHS - Core/Step Down",
        "CAMHS - Crisis Team (Hospital Urgents)": "CAMHS - Crisis Team (Hospital Urgents)",
        "CAMHS - Waiting List": "CAMHS - Waiting List",
        "Child Health: Community-based Paediatrics": "Child Health: Community-based Paediatrics",
        "Child Health: Hospital-based Paediatrics": "Child Health: Hospital-based Paediatrics",
        "Child Health: School Nurse": "Child Health: School Nurse",
        "Community Mental Health Team (Adult Mental Health)": "Community Mental Health Team (Adult Mental Health)",
        "Employer": "Employer",
        "Employer: Occupational Health": "Employer: Occupational Health",
        "Family Support Worker": "Family Support Worker",
        "Improving Access to Psychological Therapies Service": "Improving Access to Psychological Therapies Service",
        "Independent Sector: Low secure Inpatients": "Independent Sector: Low secure Inpatients",
        "Independent Sector: Medium secure Inpatients": "Independent Sector: Medium secure Inpatients",
        "Inpatient Service Child and Adult Mental Health": "Inpatient Service Child and Adult Mental Health",
        "Inpatient Service Learning Disabilities": "Inpatient Service Learning Disabilities",
        "Internal Referral": "Internal Referral",
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
        "Other Primary Health Care": "Other Primary Health Care",
        "Other secondary care specialty": "Other secondary care specialty",
        "Other SERVICE or agency": "Other SERVICE or agency",
        "Other: Asylum Services": "Other: Asylum Services",
        "Other: Drug Action Team / Drug Misuse Agency": "Other: Drug Action Team / Drug Misuse Agency",
        "Other: Job Centre Plus": "Other: Job Centre Plus",
        "Other: Out of Area Agency": "Other: Out of Area Agency",
        "Other: Single Point of Access Service": "Other: Single Point of Access Service",
        "Other: Urgent and Emergency Care Ambulance Service": "Other: Urgent and Emergency Care Ambulance Service",
        "Permanent Transfer from Another Mental Health Trust": "Permanent Transfer from Another Mental Health Trust",
        "Primary Health Care: Health Visitor": "Primary Health Care: Health Visitor",
        "Primary Health Care: Maternity Service": "Primary Health Care: Maternity Service",
        "Self-Referral :Self": "Self-Referral :Self",
        "Self-Referral: Carer/Relative": "Self-Referral: Carer/Relative",
        "Temporary Transfer from Another Mental Health Trust": "Temporary Transfer from Another Mental Health Trust",
        "Transfer by Graduation from CAMHS to Adult Mental Health Services": "Transfer by Graduation from CAMHS to Adult Mental Health Services",
        "Voluntary Sector": "Voluntary Sector",
        "Blank (nothing selected)": "Blank (nothing selected)"
    }


    try:
        if row in reason_map:
            if reason_map[row] is not None:
                df_filtered = df[df['source'] == reason_map[row]]
            elif row == "Blank (nothing selected)":
                df_filtered = df[df['source'].isna()]
        else:
            print("Row not recognised by filters: " + row)
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

        return df_filtered

    except Exception as e:
        print(f"Error in source_of_referral_filter with row {row}: {e} . current df is {dfname}")
        return pd.DataFrame()  # Return empty DataFrame in case of error


def reason_for_referral_filter(df, row, dfname="empty"):
    reason_map = {
        "Adjustment to Health Issues": "Adjustment to Health Issues",
        "Anxiety": "Anxiety",
        "Attachment Difficulties": "Attachment Difficulties",
        "Behaviour Disorder": "Behaviour Disorder",
        "Behaviours that challenge due to a Learning Disability": "Behaviours that challenge due to a Learning Disability",
        "Bi-polar Disorder": "Bi-polar Disorder",
        "Community Perinatal Mental Health Partner Assessment": "Community Perinatal Mental Health Partner Assessment",
        "Conduct Disorders": "Conduct Disorders",
        "Depression": "Depression",
        "Diagnosed Autism": "Diagnosed Autism",
        "Drug and Alcohol Difficulties": "Drug and Alcohol Difficulties",
        "Eating Disorders": "Eating Disorders",
        "Gambling disorder": "Gambling disorder",
        "Gender Discomfort Issues": "Gender Discomfort Issues",
        "In Crisis": "In Crisis",
        "Isolation": "Isolation",
        "Neurodevelopmental Conditions, excluding Autism": "Neurodevelopmental Conditions, excluding Autism",
        "Obsessive Compulsive Disorder": "Obsessive Compulsive Disorder",
        "Ongoing or Recurrent Psychosis": "Ongoing or Recurrent Psychosis",
        "Organic Brain Disorder": "Organic Brain Disorder",
        "Other": "Other",
        "Panic Attacks": "Panic Attacks",
        "Perinatal Mental Health Issues": "Perinatal Mental Health Issues",
        "Personality Disorders": "Personality Disorders",
        "Phobias": "Phobias",
        "Post-Traumatic Stress Disorder": "Post-Traumatic Stress Disorder",
        "Preconception Perinatal Mental Health Concern": "Preconception Perinatal Mental Health Concern",
        "Relationship Difficulties": "Relationship Difficulties",
        "Self-Care Issues": "Self-Care Issues",
        "Self-Harm Behaviours": "Self-Harm Behaviours",
        "Suspected Autism": "Suspected Autism",
        "(Suspected) First Episode Psychosis": "(Suspected) First Episode Psychosis",
        "Unexplained Physical Symptoms": "Unexplained Physical Symptoms",
        "Blank (nothing selected)": "Blank (nothing selected)"
    }

    try:
        if row in reason_map:
            if reason_map[row] is not None:
                df_filtered = df[df['reason'] == reason_map[row]]
            elif row == "Blank (nothing selected)":
                df_filtered = df[df['reason'].isna()]
        else:
            print("Row not recognised by filters: " + row)
            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

        return df_filtered

    except Exception as e:
        print(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        return pd.DataFrame()  # Return empty DataFrame in case of error


def other_reason_for_referral_filter(df, row, dfname="empty"):
    reason_map = {
        "Anti-Social Behaviour": "Anti-Social Behaviour",
        "At risk of CSE": "At risk of CSE",
        "Bereavement": "Bereavement",
        "Bullying": "Bullying",
        "Community Involvement/Participation": "Community Involvement/Participation",
        "Covid 19": "Covid 19",
        "Criminal offending behaviour/or at risk of": "Criminal offending behaviour/or at risk of",
        "Dementia": "Dementia",
        "Discrimination": "Discrimination",
        "Domestic Abuse": "Domestic Abuse",
        "Early Help": "Early Help",
        "Education Support": "Education Support",
        "Emotional Support": "Emotional Support",
        "Employability": "Employability",
        "Family Problems/Home Life": "Family Problems/Home Life",
        "Family Support": "Family Support",
        "Financial Support": "Financial Support",
        "Historic Domestic Abuse": "Historic Domestic Abuse",
        "Homelessness": "Homelessness",
        "Housing": "Housing",
        "In Crisis": "In Crisis",
        "LGBTQIA+ support": "LGBTQIA+ support",
        "Mental Health Support": "Mental Health Support",
        "Personal Safety": "Personal Safety",
        "Physical Health": "Physical Health",
        "Sexual Health": "Sexual Health",
        "Sexualised Abuse": "Sexualised Abuse",
        "Sleep Hygiene": "Sleep Hygiene",
        "Social Isolation and Loneliness": "Social Isolation and Loneliness",
        "Victim of CSE": "Victim of CSE",
        "Wellness Health Education, Guidance and Counselling": "Wellness Health Education, Guidance and Counselling",
        "Young Carer/Adult Carer": "Young Carer/Adult Carer",
        "Blank (nothing selected)": "Blank (nothing selected)"
    }

    try:
        if row in reason_map:
            if reason_map[row] is not None:
                df_filtered = df[df['reason_other'] == reason_map[row]]
            elif row == "Blank (nothing selected)":
                df_filtered = df[df['reason_other'].isna()]
        else:
            print("Row not recognised by filters: " + row)
            raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")

            return pd.DataFrame()  # Return empty DataFrame for unrecognized rows

        return df_filtered

    except Exception as e:
        print(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")
        raise Exception(f"Error in reason_for_referral_filter with row {row}: {e} . current df is {dfname}")

        return pd.DataFrame()  # Return empty DataFrame in case of error


def gender_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def ethnicity_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def disability_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def sexual_orientation_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def asylum_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def spec_ed_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def ed_hcp_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def are_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def leaving_care_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def lac_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def cpp_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def cinp_filter_end(df, row, dfname="empty"):
    return "mymupURL"

def young_carer_filter_end(df, row, dfname="empty"):
    return "mymupURL"

filter_function_map = {
    "service_info_config": SI_row_filter,
    "yp_gender_config": gender_category_filter,
    "yp_ethnicity_config": ethnic_category_filter,
    "yp_disability_config": disability_category_filter,
    "yp_sexual_orientation_config": sexual_orientation_filter,
    "yp_age_config": age_category_filter,
    "yp_area_config": area_category_filter,
    "yp_asylum_status_config": asylum_status_filter,
    "yp_special_ed_needs_config": sen_category_filter,
    "yp_ed_health_care_plan_config": ehcp_category_filter,
    "yp_at_risk_exploitation_config": at_risk_exploitation_filter,
    "yp_leaving_care_config": leaving_care_filter,
    "yp_looked_after_child_config": lac_category_filter,
    "yp_child_protection_plan_config": cpp_category_filter,
    "yp_child_in_need_plan_config": cinp_category_filter,
    "yp_young_carer_config": young_carer_category_filter,
    "total_attended_contacts_config": attended_contacts_filter,
    "goals_based_outcomes_config": goals_based_outcomes_filter,
    "average_goals_based_outcomes_config": average_goals_based_outcomes_filter,
    "goal_themes_goals_based_outcomes_config": goal_themes_filter,
    "dss_goals_based_outcomes_config": dss_goal_filter,
    "contacts_by_theme_config": contact_by_theme_filter,
    "source_of_referral_config": source_of_referral_filter,
    "reason_for_referral_config": reason_for_referral_filter,
    "other_reason_for_referral_config": other_reason_for_referral_filter,
    "gender_config": gender_filter_end,
    "ethnicity_config": ethnicity_filter_end,
    "disability_config": disability_filter_end,
    "sexual_orientation_config": sexual_orientation_filter_end,
    "asylum_seeker_refugee_status_config": asylum_filter_end,
    "special_educational_needs_config": spec_ed_filter_end,
    "education_health_care_plan_config": ed_hcp_filter_end,
    "at_risk_of_exploitation_config": are_filter_end,
    "leaving_care_config": leaving_care_filter_end,
    "looked_after_child_config": lac_filter_end,
    "child_protection_plan_config": cpp_filter_end,
    "child_in_need_plan_config": cinp_filter_end,
    "young_carer_config": young_carer_filter_end,
}