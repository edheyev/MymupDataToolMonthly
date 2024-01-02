# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:58:58 2023

@author: Edloc
"""

import pandas as pd



def column_filter(df, column, dfname="empty"):
    try:
        if column == "Q1_Totals":
            # Apply all filters and then concatenate the results
            filters = [
                df["franchise"] == "Barnardos WRAP",
                df["franchise"] == "Bradford Youth Service",
                (df["franchise"] == "Brathay") & (df["contact_service_type"] == "MAGIC"),
                (df["franchise"] == "Inspired Neighbourhoods") & (df["contact_service_type"] == "CYP"),
                df["contact_service_type"] == "Know Your Mind",
                df["contact_service_type"] == "Know Your Mind Plus",
                df["contact_service_type"] == "Hospital Buddies AGH",
                df["contact_service_type"] == "Hospital Buddies BRI",
                (df["franchise"] == "Selfa") & (df["contact_service_type"] == "Mighty Minds")
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
                (df["franchise"] == "Brathay") & (df["contact_service_type"] == "MAGIC")
            ]
        elif column == "INCIC (CYP)":
            return df[
                (df["franchise"] == "Inspired Neighbourhoods")
                & (df["contact_service_type"] == "CYP")
            ]
        elif column == "MIB Know Your Mind":
            return df[df["contact_service_type"] == "Know Your Mind"]
        elif column == "MIB Know Your Mind +":
            return df[df["contact_service_type"] == "Know Your Mind Plus"]
        elif column == "MIB Hospital Buddys Airedale General":
            return df[df["contact_service_type"] == "Hospital Buddies AGH"]
        elif column == "MIB Hospital Buddys BRI":
            return df[df["contact_service_type"] == "Hospital Buddies BRI"]
        elif column == "SELFA (Mighty Minds)":
            return df[
                (df["franchise"] == "Selfa")
                & (df["contact_service_type"] == "Mighty Minds")
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
    try:
        # Extract age number from row name
        if row.startswith("Age "):
            age = int(row.split(" ")[1])
            # Apply filter logic based on extracted age
            filtered_df = df[
                df["age"] == age
            ]  # Assuming 'age' is the column name for age in the DataFrame
            # Further processing logic here
            pass
        elif row == "Out of age Range":
            # Logic for handling out of age range
            filtered_df = df[
                df["age"] > 25
            ]  # Adjust the condition based on your age range criteria
            # Further processing logic here
            pass
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

    except Exception as e:
        print(
            f"Error in age_category_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Or return some other result based on the processing logic


def area_category_filter(df, row, dfname="empty"):
    try:
        if row == "BAILDON":
            filtered_df = df[df["area"] == "BAILDON"]
        elif row == "Bentham":
            filtered_df = df[df["area"] == "Bentham"]
        elif row == "BINGLEY":
            filtered_df = df[df["area"] == "BINGLEY"]
        elif row == "BINGLEY RURAL":
            filtered_df = df[df["area"] == "BINGLEY RURAL"]
        elif row == "BOLTON & UNDERCLIFFE":
            filtered_df = df[df["area"] == "BOLTON & UNDERCLIFFE"]
        elif row == "BOWLING & BARKEREND":
            filtered_df = df[df["area"] == "BOWLING & BARKEREND"]
        elif row == "BRADFORD MOOR":
            filtered_df = df[df["area"] == "BRADFORD MOOR"]
        elif row == "CITY":
            filtered_df = df[df["area"] == "CITY"]
        elif row == "CLAYTON & FAIRWEATHER GREEN":
            filtered_df = df[df["area"] == "CLAYTON & FAIRWEATHER GREEN"]
        elif row == "CRAVEN":
            filtered_df = df[df["area"] == "CRAVEN"]
        # ... Add similar conditions for all other areas ...
        elif row == "KEIGHLEY WEST":
            filtered_df = df[df["area"] == "KEIGHLEY WEST"]
        elif row == "LITTLE HORTON":
            filtered_df = df[df["area"] == "LITTLE HORTON"]
        elif row == "MANNINGHAM":
            filtered_df = df[df["area"] == "MANNINGHAM"]
        elif row == "OUT OF AREA":
            filtered_df = df[df["area"] == "OUT OF AREA"]
        elif row == "QUEENSBURY":
            filtered_df = df[df["area"] == "QUEENSBURY"]
        elif row == "ROYDS":
            filtered_df = df[df["area"] == "ROYDS"]
        elif row == "SHIPLEY":
            filtered_df = df[df["area"] == "SHIPLEY"]
        elif row == "THORNTON & ALLERTON":
            filtered_df = df[df["area"] == "THORNTON & ALLERTON"]
        elif row == "TOLLER":
            filtered_df = df[df["area"] == "TOLLER"]
        elif row == "TONG":
            filtered_df = df[df["area"] == "TONG"]
        elif row == "WHARFEDALE":
            filtered_df = df[df["area"] == "WHARFEDALE"]
        elif row == "WIBSEY":
            filtered_df = df[df["area"] == "WIBSEY"]
        elif row == "WINDHILL & WROSE":
            filtered_df = df[df["area"] == "WINDHILL & WROSE"]
        elif row == "WORTH VALLEY":
            filtered_df = df[df["area"] == "WORTH VALLEY"]
        elif row == "WYKE":
            filtered_df = df[df["area"] == "WYKE"]
        elif row == "Blank (nothing selected )":
            filtered_df = df[
                df["area"].isna()
            ]  # Adjust this condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        # Example: pass
        pass

    except Exception as e:
        print(
            f"Error in area_category_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Or return some other result based on the processing logic


def asylum_status_filter(df, row, dfname="empty"):
    try:
        # Filter logic based on asylum seeker/refugee status
        if row == "Yes":
            filtered_df = df[df["asylum_status"] == "Yes"]
        elif row == "No":
            filtered_df = df[df["asylum_status"] == "No"]
        elif row == "Not known":
            filtered_df = df[df["asylum_status"] == "Not known"]
        elif row == "Blank (nothing selected )":
            filtered_df = df[
                df["asylum_status"].isna()
            ]  # Adjust this condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        pass

    except Exception as e:
        print(
            f"Error in asylum_status_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Or return some other result based on the processing logic


def special_ed_needs_filter(df, row, dfname="empty"):
    try:
        # Filter logic based on special educational needs status
        if row == "No":
            filtered_df = df[df["special_ed_needs"] == "No"]
        elif row == "Not known":
            filtered_df = df[df["special_ed_needs"] == "Not known"]
        elif row == "Yes":
            filtered_df = df[df["special_ed_needs"] == "Yes"]
        elif row == "Not applicable":
            filtered_df = df[df["special_ed_needs"] == "Not applicable"]
        elif row == "Blank (nothing selected )":
            filtered_df = df[
                df["special_ed_needs"].isna()
            ]  # Adjust this condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        pass

    except Exception as e:
        print(
            f"Error in special_ed_needs_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Or return some other result based on the processing logic


def ed_health_care_plan_filter(df, row, dfname="empty"):
    try:
        # Filter logic based on education, health and care plan status
        if row == "Yes":
            filtered_df = df[df["ed_health_care_plan"] == "Yes"]
        elif row == "No":
            filtered_df = df[df["ed_health_care_plan"] == "No"]
        elif row == "Not known":
            filtered_df = df[df["ed_health_care_plan"] == "Not known"]
        elif row == "Not applicable":
            filtered_df = df[df["ed_health_care_plan"] == "Not applicable"]
        elif row == "Blank (nothing selected )":
            filtered_df = df[
                df["ed_health_care_plan"].isna()
            ]  # Adjust this condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        pass

    except Exception as e:
        print(
            f"Error in ed_health_care_plan_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Or return some other result based on the processing logic


def at_risk_exploitation_filter(df, row, dfname="empty"):
    try:
        if row == "Yes":
            filtered_df = df[df["at_risk_exploitation"] == "Yes"]
        elif row == "No":
            filtered_df = df[df["at_risk_exploitation"] == "No"]
        elif row == "Not known":
            filtered_df = df[df["at_risk_exploitation"] == "Not known"]
        elif row == "Blank (nothing selected )":
            filtered_df = df[
                df["at_risk_exploitation"].isna()
            ]  # or use appropriate condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Here, you can add further processing logic for the filtered data
        pass

    except Exception as e:
        print(
            f"Error in at_risk_exploitation_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Return the filtered DataFrame or some other result based on processing logic


def leaving_care_filter(df, row, dfname="empty"):
    try:
        if row == "Yes":
            filtered_df = df[df["leaving_care"] == "Yes"]
        elif row == "No":
            filtered_df = df[df["leaving_care"] == "No"]
        elif row == "Not Known":
            filtered_df = df[df["leaving_care"] == "Not Known"]
        elif row == "Blank (nothing selected)":
            filtered_df = df[
                df["leaving_care"].isna()
            ]  # or use appropriate condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Here, you can add further processing logic for the filtered data
        pass

    except Exception as e:
        print(
            f"Error in leaving_care_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Return the filtered DataFrame or some other result based on processing logic


def looked_after_child_filter(df, row, dfname="empty"):
    try:
        if row == "Yes":
            filtered_df = df[df["looked_after_child"] == "Yes"]
        elif row == "No":
            filtered_df = df[df["looked_after_child"] == "No"]
        elif row == "Not known":
            filtered_df = df[df["looked_after_child"] == "Not known"]
        elif row == "Blank (nothing selected)":
            filtered_df = df[
                df["looked_after_child"].isna()
            ]  # or use appropriate condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        pass

    except Exception as e:
        print(
            f"Error in looked_after_child_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Return the filtered DataFrame or some other result based on processing logic


def child_protection_plan_filter(df, row, dfname="empty"):
    try:
        if row == "No":
            filtered_df = df[df["child_protection_plan"] == "No"]
        elif row == "Has never been subject to a plan":
            filtered_df = df[
                df["child_protection_plan"] == "Has never been subject to a plan"
            ]
        elif row == "Not known":
            filtered_df = df[df["child_protection_plan"] == "Not known"]
        elif row == "Has been previously subject to a plan":
            filtered_df = df[
                df["child_protection_plan"] == "Has been previously subject to a plan"
            ]
        elif row == "Is currently subject to a plan":
            filtered_df = df[
                df["child_protection_plan"] == "Is currently subject to a plan"
            ]
        elif row == "Under assessment":
            filtered_df = df[df["child_protection_plan"] == "Under assessment"]
        elif row == "Blank (nothing selected)":
            filtered_df = df[
                df["child_protection_plan"].isna()
            ]  # or use appropriate condition for blank entries
        else:
            print("Row not recognised by filters")
            return pd.DataFrame()

        # Further processing logic here
        pass

    except Exception as e:
        print(
            f"Error in child_protection_plan_filter with row {row}: {e} . current df is {dfname}"
        )
        return "error"

    return filtered_df  # Return the filtered DataFrame or some other result based on processing logic





filter_function_map = {
    "service_info_config": SI_row_filter,
    "yp_gender_config": gender_category_filter,
    "yp_ethnicity_config": ethnic_category_filter,
    "yp_disability_config": disability_category_filter,
    "yp_sexual_orientation_config": sexual_orientation_filter,
    "yp_age_config": age_category_filter,
    "yp_area_config": area_category_filter,
    "yp_asylum_status_config": asylum_status_filter,
    "yp_special_ed_needs_config": special_ed_needs_filter,
    "yp_ed_health_care_plan_config": ed_health_care_plan_filter,
    "yp_at_risk_exploitation_config": at_risk_exploitation_filter,
    "yp_leaving_care_config": leaving_care_filter,
    "yp_looked_after_child_config": looked_after_child_filter,
    "yp_child_protection_plan_config": child_protection_plan_filter,
}