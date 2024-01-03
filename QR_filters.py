# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:58:58 2023

@author: Edloc
"""

import pandas as pd



def column_filter(df, column, dfname="empty"):
    
    if dfname == "File_Closures_And_Goals_Within_Reporting_Period" or dfname == "MIB_File_Closures_And_Goals_Within_Reporting_Period":
        contact_service = "file_closure_service_type"
    else:
        contact_service = "contact_service_type"
    
    
    try:
        if column == "Q1_Totals":
        # ACTUALLY THIS initial FILTER IS DEPRECATED AND IS BEING TOTALLED IN THE REPORTING SCRIPT
            filters = [
                df["franchise"] == "Barnardos WRAP",
                df["franchise"] == "Bradford Youth Service",
                (df["franchise"] == "Brathay") & (df[contact_service] == "MAGIC"),
                (df["franchise"] == "Inspired Neighbourhoods") & (df[contact_service] == "CYP"),
                df[contact_service] == "Know Your Mind",
                df[contact_service] == "Know Your Mind Plus",
                df[contact_service] == "Hospital Buddies AGH",
                df[contact_service] == "Hospital Buddies BRI",
                (df["franchise"] == "Selfa") & (df[contact_service] == "Mighty Minds")
            ]
            filtered_dfs = [df[filter_condition] for filter_condition in filters]
            total_df = pd.concat(filtered_dfs)
            return total_df.drop_duplicates()
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
            return pd.DataFrame()
    except Exception as e:
        print(f"Error in col_filter with column {column}: {e} . current df is {dfname}")
        return pd.DataFrame({"error": [True]})  # Return DataFrame with an error flag

def SI_row_filter(df, row, dfname="empty"):
    try:
        mib = True if dfname.startswith("MIB") else False

        # print("Row Filter: "+ row)
        if row == "Number of unique people supported":
            if not mib:
                # exclude admin contacts
                df = df[df["contact_themes"] != "Administrative"]

                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches).
                contact_approaches = [
                    "Face to Face",
                    "Telephone",
                    "Type talk",
                    "Video consultation",
                    "Instant Messaging (Synchronous)",
                ]
                df = df[df["contact_approach"].isin(contact_approaches)]

                # Count of unique clients
                return df["client_id"].count()
            else:
                # exclude admin contacts
                df = df[df["contact_themes"] != "Administrative"]

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

                # Count of unique clients
                return df["client_id"].count()

        elif row == "How many were declined by the service?":
            return df["client_id"].count()

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
            return df_filtered["client_id"].nunique()

        elif row == "Active cases":
            # Count clients with no file closure date and status active, pending, processing, or waiting list
            active_statuses = ["active", "pending", "processing", "waiting list"]
            # df_active = df[df['client_status'].isin(active_statuses) & df['file_closure_date'].isna()]
            # df_active = df[df['client_status'].isin(active_statuses) & df['file_closure_date'].isna()]
            return df["client_id"].nunique()

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
            return df_moved_on["client_id"].nunique()
        else:
            print("Row not recognised by filters")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in row_filter with row {row}: {e} . current df is {dfname}")
    return "error"

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
        "Blank (nothing selected)": None  # Special handling for blank entries
    }

    try:
        if row in gender_map:
            if gender_map[row] is not None:
                return df[df['client_gender'] == gender_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                # Counting rows where 'client_gender' is NaN
                return df[df['client_gender'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in gender_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return 0

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
        "Blank (nothing selected)": None  # Special handling for blank entries
    }

    try:
        if row in ethnic_map:
            if ethnic_map[row] is not None:
                return df[df['client_ethnicity'] == ethnic_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                # Counting rows where 'client ethnicity' is NaN
                return df[df['client_ethnicity'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in ethnic_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "Some result or DataFrame"

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
        "Personal, Self-Care and Continence": "Personal, Self-Care and Continence",  # Not found in the data
        "Progressive Conditions and Physical Health (such as HIV, Cancer, Multiple Sclerosis, Fits)": "Progressive Conditions and Physical Health (such as HIV, cancer, multiple sclerosis, fits etc)", 
        "Sight": "Sight",
        "Speech": "Speech",
        "Yes": "Yes",
        "Blank (nothing selected)": None  # Special handling for blank entries
    }

    try:
        if row in disability_map:
            if disability_map[row] is not None:
                return df[df['client_disability'] == disability_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                # Counting rows where 'client disability' is NaN
                return df[df['client_disability'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in disability_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "Some result or DataFrame"

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
        "Blank (nothing selected)": None  # Special handling for blank entries
    }

    try:
        if row in sexuality_map:
            if sexuality_map[row] is not None:
                return df[df['client_sexuality'] == sexuality_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                # Counting rows where 'client sexuality' is NaN
                return df[df['client_sexuality'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in sexuality_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "Some result or DataFrame"

def age_category_filter(df, row, dfname="empty"):
    age_groups = {
        "Age 4": 4, "Age 5": 5, "Age 6": 6, "Age 7": 7, "Age 8": 8, "Age 9": 9,
        "Age 10": 10, "Age 11": 11, "Age 12": 12, "Age 13": 13, "Age 14": 14,
        "Age 15": 15, "Age 16": 16, "Age 17": 17, "Age 18": 18, "Age 19": 19,
        "Age 20": 20, "Age 21": 21, "Age 22": 22, "Age 23": 23, "Age 24": 24,
        "Age 25": 25, "Out of age Range": None
    }

    try:
        if row in age_groups:
            if age_groups[row] is not None:
                age = age_groups[row]
                return df[df['client_age'] == age]['client_id'].nunique()
            else:
                # Handling "Out of age Range" by filtering ages not in the specified range
                specified_ages = list(age_groups.values())
                specified_ages.remove(None)
                return df[~df['client_age'].isin(specified_ages)]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in age_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return 0

def area_category_filter(df, row, dfname="empty"):
    area_map = {
        "BAILDON": "BAILDON",
        "Bentham": "Bentham",  # Not found in the data
        "BINGLEY": "BINGLEY",
        "BINGLEY RURAL": "BINGLEY RURAL",
        "BOLTON & UNDERCLIFFE": "BOLTON & UNDERCLIFFE",
        "BOWLING & BARKEREND": "BOWLING & BARKEREND",
        "BRADFORD MOOR": "BRADFORD MOOR",
        "CITY": "CITY",
        "CLAYTON & FAIRWEATHER GREEN": "CLAYTON & FAIRWEATHER GREEN",
        "CRAVEN": "CRAVEN",
        "Craven Ward  -Skipton North": "Craven Ward -  Skipton North",
        "Craven Ward  -Skipton West": "Craven Ward -  Skipton West",
        "Craven Ward -Settle Ribblebanks": "Craven Ward - Settle Ribblebanks",  # Not found in the data
        "Craven Ward -Sutton in Craven": "Craven Ward -  Sutton-in-Craven",
        "Carven ward -Skipton South": "Craven Ward -  Skipton South",
        "Craven Ward -Hellifield and Long Preston": "Craven Ward - Hellifield and Long Preston",  # Not found in the data
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

    try:
        if row in area_map:
            if area_map[row] is not None:
                return df[df['client_area'] == area_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected )":
                # Counting rows where 'client area' is NaN
                return df[df['client_area'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in area_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def asylum_status_filter(df, row, dfname="empty"):
    asylum_seeker_map = {
        "Yes": "Yes",
        "No": "No",
        "Not known": "Unknown",  
        "Blank (nothing selected )": None  
    }

    try:
        if row in asylum_seeker_map:
            if asylum_seeker_map[row] is not None:
                return df[df['client_asylum_seeker'] == asylum_seeker_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected )":
                # Counting rows where 'client asylum seeker' is NaN
                return df[df['client_asylum_seeker'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in asylum_seeker_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def sen_category_filter(df, row, dfname="empty"):
    sen_map = {
        "No": "No",
        "Not known": "Not known",
        "Yes": "Yes",
        "Not applicable": "Not applicable",
        "Blank (nothing selected )": None
    }

    try:
        if row in sen_map:
            if sen_map[row] is not None:
                return df[df['client_sen'] == sen_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected )":
                return df[df['client_sen'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in sen_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def ehcp_category_filter(df, row, dfname="empty"):
    ehcp_map = {
        "No": "No",
        "Not known": "Not known",
        "Yes": "Yes",
        "Not applicable": "Not applicable",
        "Blank (nothing selected )": None
    }

    try:
        if row in ehcp_map:
            if ehcp_map[row] is not None:
                return df[df['client_ehcp'] == ehcp_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected )":
                return df[df['client_ehcp'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in ehcp_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def at_risk_exploitation_filter(df, row, dfname="empty"):
    are_map = {
        "No": "No",
        "Not known": "Unknown",
        "Yes": "Yes",
        "Blank (nothing selected )": None
    }

    try:
        if row in are_map:
            if are_map[row] is not None:
                return df[df['client_exploitation_risk'] == are_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected )":
                return df[df['client_exploitation_risk'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in at_risk_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def leaving_care_filter(df, row, dfname="empty"):
    lc_map = {
        "Yes": "Yes",
        "No": "No",
        "Not Known": "Unknown",  # Adjusted to match the row name
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    try:
        if row in lc_map:
            if lc_map[row] is not None:
                return df[df['client_leaving_care'] == lc_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                return df[df['client_leaving_care'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in leaving_care_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def lac_category_filter(df, row, dfname="empty"):
    lac_map = {
        "Yes": "Yes (Is a child looked after)",
        "No": "No (Is not a child looked after)",
        "Not known": "Not Known",
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    try:
        if row in lac_map:
            if lac_map[row] is not None:
                return df[df['client_lac'] == lac_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                return df[df['client_lac'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in lac_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

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

    try:
        if row in cpp_map:
            if cpp_map[row] is not None:
                return df[df['client_cpp'] == cpp_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                return df[df['client_cpp'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in cpp_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def cinp_category_filter(df, row, dfname="empty"):
    cinp_map = {
        "Is currently subject to a Child in need plan": "Is currently subject to a Children In Need Plan",
        "No": "No",
        "Has never been subject to a Child in need plan": "Has never been subject to a Children In Need Plan",
        "Not known": "Not known",
        "Has previously been subject to a Child in need plan": "Has previously been subject to a Children In Need Plan",
        "Under assessment": "Under assessment",  # Not found in your dataset
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    try:
        if row in cinp_map:
            if cinp_map[row] is not None:
                return df[df['client_cinp'] == cinp_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                return df[df['client_cinp'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in cinp_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def young_carer_category_filter(df, row, dfname="empty"):
    young_carer_map = {
        "Yes": "Yes - child or young PERSON has a caring role for an ill or disabled parent, carer or sibling",
        "No": "No - child or young PERSON does not have a caring role for an ill or disabled parent, carer or sibling",
        "Not known": "Not Known",
        "Not stated": "Not Stated (Person asked but declined to provide a response)",
        "Blank (nothing selected)": None  # Handling for blank entries
    }

    try:
        if row in young_carer_map:
            if young_carer_map[row] is not None:
                return df[df['client_young_carer'] == young_carer_map[row]]['client_id'].nunique()
            elif row == "Blank (nothing selected)":
                return df[df['client_young_carer'].isna()]['client_id'].nunique()
        else:
            print("Row not recognised by filters: " + row)
            return "error"

    except Exception as e:
        print(f"Error in young_carer_category_filter with row {row}: {e} . current df is {dfname}")
        return "error"

    return "row or dataframe error"

def attended_contacts_filter(df, row, dfname="empty"):

    is_mib = dfname.startswith("MIB")
    
    
    if row == "Total Number of Attended Contacts":
        initial_filtering = total_attended_contacts(df, is_mib)
        return initial_filtering['client_id'].nunique()

    elif row == "One to One Contacts":
        initial_filtering = total_attended_contacts(df, is_mib)
        #  activity details client therapy mode individual patient
        if is_mib:
            session_types = ["1 to 1", "2 to 1"]
            dfout = initial_filtering[initial_filtering['contact_session_type'].isin(session_types)]
        else:
            dfout = initial_filtering[initial_filtering['contact_therapy_mode'] == 'Individual patient']
        
        return dfout['client_id'].nunique()  # Count unique client_ids

    elif row == "Group Contacts":
        initial_filtering = total_attended_contacts(df, is_mib)
        # Filtering for 'Group' session type and 'group therapy' mode
        if is_mib:
            # If MIB specific logic is needed, include it here
            dfout = initial_filtering[(initial_filtering['contact_session_type'] == 'Group') ]
        else:
            dfout = initial_filtering[(initial_filtering['contact_therapy_mode'] == 'group therapy')]
        

        # Count the number of rows
        return len(dfout)


    elif row == "Indirect Activities":
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        df = df[df['contact_attendance'] == 'Attended']
        # Filter for rows where 'indirect service type' is not empty or NA
        indirect_approaches = ["Email", "Text Message (Asynchronous)"]
        dfout = df[df['contact_approach'].isin(indirect_approaches)]

        return len(dfout)

    elif row == "Other (email and text)":
        if is_mib:
            df = df[~df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            df = df[~df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        df = df[df['contact_attendance'] == 'Attended']
        other_approachs = ["Email", "Text Message (Asynchronous)", "Chat Room (Asynchronous)","Message Board (Asynchronous)" "Chat Room (Asynchronous)", "Instant Messaging (Asynchronous)", "Other (not listed)"]
        dfout = df[df['contact_approach'].isin(other_approachs)]
        return len(dfout)
        
        
    elif row == "Admin Contacts":
        if is_mib:
            dfout = df[df['contact_session_option'].str.contains("Administrative", case=False, na=False)]
        else:
            dfout = df[df['contact_themes'].str.contains("Administrative", case=False, na=False)]
        
        return len(dfout)

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
        
        return len(dfout)



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
            return 0
        else:
            return round(len(dfdna)/len(dftotal)*100, 2)

    else:
        print(f"Row not recognised: {row}")
        return "error"

    return "FILTERING FAILED"

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
    # Additional filters may be required based on the dataset and requirements
    print(f"Row: {row}")
    print(f"dfname: {dfname}")
    print(f"df: {df}")
    if row == "% of closed cases with initial outcomes measure completed":
        # Logic to calculate this percentage
        pass

    elif row == "% of closed cases with follow-up/final outcomes measure completed":
        # Logic to calculate this percentage
        pass

    elif row == "% of GBOs demonstrating reliable change":
        # Logic to calculate this percentage
        pass
    
    else:
        print(f"Row not recognised: {row}")
        return "error"

    return "result after filtering"

def average_goals_based_outcomes_filter(df, row, dfname="empty"):
    
    is_mib = dfname.startswith("MIB")
    

    df_copy = df.copy()

    # Convert dates to datetime
    df_copy['referral_date'] = pd.to_datetime(df_copy['referral_date'], errors='coerce')
    df_copy['file_closure_date'] = pd.to_datetime(df_copy['file_closure_date'], errors='coerce')
    df_copy['goal_score_date'] = pd.to_datetime(df_copy['goal_score_date'], errors='coerce')

    # Filter for Initial and Follow-Up/Final GBOs
    df_initial = df_copy[df_copy['initial_/_followup_/_final'].str.contains("Initial", case=False, na=False)]
    df_followup_final = df_copy[df_copy['initial_/_followup_/_final'].isin(["Follow up", "Final"])]

    # Ensure that 'goal_score_date' is uniquely named in df_followup_final
    df_followup_final = df_followup_final.rename(columns={'goal_score_date': 'goal_score_date_fu_f'})

    # Merge on 'goal_id'
    merged_df = pd.merge(df_initial[['goal_id', 'referral_date', 'file_closure_date', 'score_1', 'score_2', 'score_3']], 
                        df_followup_final[['goal_id', 'goal_score_date_fu_f']], 
                        on='goal_id', 
                        how='inner')

    # Apply the criteria for paired GBOs
    paired_gbo_df = merged_df[(merged_df['goal_score_date_fu_f'] > merged_df['referral_date']) & 
                            (merged_df['goal_score_date_fu_f'] < merged_df['file_closure_date'])]

    # Count the paired GBOs
        
    if row == "% of closed case that have an initial and follow up/final paired GBO":
        
        if len(df_initial) == 0:
            return str(0) + "%"
        else:
            return str(round(len(paired_gbo_df) / len(df_initial) * 100, 2)) + "%"

    elif row == "% of closed cases with reliable change in paired GBO":
        return "todo"
        # Check if required columns exist
        required_columns = ['score_1', 'score_2', 'score_3']
        
        print(paired_gbo_df.columns.tolist())

        for col in required_columns:
            if col not in paired_gbo_df.columns:
                print(f"Column {col} not found in DataFrame.")
                return "error"

        # Check for NaN values in 'score_1' and 'score_2'
        if paired_gbo_df[['score_1', 'score_2']].isna().any().any():
            print("NaN values found in 'score_1' or 'score_2'.")
            return "error"
        # Ensure that only goals with at least two scores are included
        paired_gbo_with_scores = paired_gbo_df.dropna(subset=['score_1', 'score_2'])

        # Use score_3 if available, otherwise use score_2
        paired_gbo_with_scores['follow_up_score'] = paired_gbo_with_scores['score_3'].fillna(paired_gbo_with_scores['score_2'])

        # Calculate score change
        paired_gbo_with_scores['score_change'] = paired_gbo_with_scores['follow_up_score'] - paired_gbo_with_scores['score_1']

        # Determine goals with reliable change (+3 or more)
        reliable_change_count = (paired_gbo_with_scores['score_change'] >= 3).sum()

        # Calculate the percentage of goals showing reliable change
        total_goals_count = len(paired_gbo_with_scores)
        percentage_reliable_change = (reliable_change_count / total_goals_count) * 100 if total_goals_count > 0 else 0

        return percentage_reliable_change


    elif row == "Average impact score of all paired goals":
        return "todo"

    else:
        print(f"Row not recognised: {row}")
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
            return "error"
        
        if len(df) == 0:
            return str(0) + "$"
        else:
            return str(round(len(this_theme_df) / len(df) * 100, 2)) + "%"

    except Exception as e:
        print(f"Error in area_category_filter with row {row}: {e} . current df is {dfname}")
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
    "Hearing Voices":"Hearing Voices",# not found in data
    "Homelessness":"Homelessness",# not found in data
    "Identity issues":"Identity issues",
    "Ill Health":"Ill Health",# not found in data
    "In Crisis/De-escalation":"In Crisis/De-escalation",
    "Issues with medication":"Issues with medication",
    "Loss Job/house":"Loss Job/house",# not found in data
    "Loneliness / isolation":"Loneliness / isolation",
    "Low confidence / self-worth":"Low confidence / self-worth", # not found in data
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
    "Self-Care":"Self-Care",# not found in data
    "Self-Harm":"Self-Harm",# not found in data
    "Sexual Violence":"Sexual Violence",# not found in data
    "Sleep problems":"Sleep problems",
    "Substance Misuse":"Substance Misuse",
    "Suicidal Ideation":"Suicidal Ideation",
    "Transition":"Transition",
    "Trauma":"Trauma",
    }
  
    try:
        if row in theme_map:
            if theme_map[row] is not None:
                # Split the row into multiple themes based on comma separation
                themes = theme_map[row].split(', ')
                # Fill NaN values in 'contact_themes' with an empty string using .loc[]
                df.loc[df['contact_themes'].isna(), 'contact_themes'] = ''
                # Check if any of the themes exist in the 'contact_themes' column
                this_theme_df = df[df['contact_themes'].str.contains('|'.join(themes))]
            elif row == "Blank (nothing selected )":
                # Count rows where 'client area' is NaN
                this_theme_df = df[df['contact_themes'].isna()]
        else:
            print("Row not recognized by filters: " + row)
            return "error"
        
        return len(this_theme_df)
    except Exception as e:
        print("An error occurred:", str(e))
        return "error"



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
    "contacts_by_theme_config": contact_by_theme_filter
}