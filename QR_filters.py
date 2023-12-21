# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:58:58 2023

@author: Edloc
"""

import pandas as pd

def column_filter(df, column, dfname="empty"):
    try:

        if column == "Q1_Totals":
            return df
        elif column == "Barnardos (Wrap)":
            return df[df['franchise'] == "Barnardos WRAP"]
        elif column == "BYS All":
            return df[df['franchise'] == "Bradford Youth Service"]
        elif column == "Brathay Magic":
            return df[(df['franchise'] == "Brathay") & (df['contact_service_type'] == "MAGIC")]
        elif column == "INCIC (CYP)":
            return df[(df['franchise'] == "Inspired Neighbourhoods") & (df['contact_service_type'] == "CYP")]
        elif column == "MIB Know Your Mind":
            return df[df['contact_service_type'] == "Know Your Mind"]
        elif column == "MIB Know Your Mind +":
            return df[df['contact_service_type'] == "Know Your Mind Plus"]
        elif column == "MIB Hospital Buddys Airedale General":
            return df[df['contact_service_type'] == "Hospital Buddies AGH"]
        elif column == "MIB Hospital Buddys BRI":
            return df[df['contact_service_type'] == "Hospital Buddies BRI"]
        elif column == "SELFA (Mighty Minds)":
            return df[(df['franchise'] == "Selfa") & (df['contact_service_type'] == "Mighty Minds")]
        else:
            print("column not recognised by filters")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error in col_filter with column {column}: {e} . current df is {dfname}")
        return pd.DataFrame({'error': [True]})  # Return DataFrame with an error flag

def SI_row_filter(df, row, dfname="empty"):
    try:
        
        # mib = True if dfname.startswith("MIB") else False
            
        #print("Row Filter: "+ row)
        if row == "Number of unique people supported (old rule)":
            return "MYMUP"
        elif row == "Number of unique people supported":
            # if not mib: 
                #exclude admin contacts
            df = df[df['contact_themes'] != "Administrative"]
            
            # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches). 
            contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video consultation", "Instant Messaging (Synchronous)"]
            df = df[df['contact_approach'].isin(contact_approaches)]            
            
            # Count of unique clients
            return df['client_id'].count() 
            # else:
                # exclude admin contacts
                # df = df[df['contact_themes'] != "Administrative"]
                
                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches). 
                # contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video consultation", "Instant Messaging (Synchronous)"]
                # df = df[df['contact_approach'].isin(contact_approaches)]  
                
                # filter session typesonly with type of session support session/ or 24 hr call back with attendance status attended (exclude all other approaches).
        
        elif row == "How many unique referrals":
            return "MYMUP"
        elif row == "How many new people referred":
            return "MYMUP"
        
        elif row == "How many were declined by the service?":
            return df['client_id'].count() 
        
        elif row == "How many young people disengaged, couldn’t be contacted or rejected a referral?":
            # Filter by specific file closure reasons and count unique clients
            closure_reasons = ["client did not attend", "client requested discharge", "client disengages", "refused to be seen", "client rejects referral", "client not available for pre-arranged appointments", "organisation cannot contact client prior to assessment", "client declined a service prior or during assessment", "client not available for assessment"]
            df_filtered = df[df['file_closure_reason'].isin(closure_reasons)]
            return df_filtered['client_id'].nunique()
            
        elif row == "Active cases":
            # Count clients with no file closure date and status active, pending, processing, or waiting list
            active_statuses = ["active", "pending", "processing", "waiting list"]
            df_active = df[df['client_status'].isin(active_statuses) & df['file_closure_date'].isna()]
            return df_active['client_id'].nunique()
        
        elif row == "How many people have moved on":
            # Filter by specific file closure reasons for moving on and count unique clients
            move_on_reasons = ["planned ending", "treatment complete", "decision made at review", "no further treatment required", "single episode"]
            df_moved_on = df[df['file_closure_reason'].isin(move_on_reasons)]
            return df_moved_on['client_id'].nunique()
        
        elif row == "% clients with initial contact 5 days after referral (new rule)":
            return "MYMUP"
        elif row == "% clients with initial contact within 7 days of referral (old rule not including admin contacts)":
            return "MYMUP"
        elif row == "% clients who had the first support session offered within 21 days of referral":
            return "MYMUP"
        elif row == "% clients attended the first contact by video/face to face/telephone within 21 days of referral":
            return "MYMUP"
        else:
            print("Row not recognised by filters")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in row_filter with row {row}: {e} . current df is {dfname}")
    return "error"