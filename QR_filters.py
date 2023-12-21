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
        
        mib = True if dfname.startswith("MIB") else False
            
        #print("Row Filter: "+ row)
        if row == "Number of unique people supported (old rule)":
            return "MYMUP"
        elif row == "Number of unique people supported":
            if not mib: 
                #exclude admin contacts
                df = df[df['contact_themes'] != "Administrative"]
                
                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches). 
                contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video consultation", "Instant Messaging (Synchronous)"]
                df = df[df['contact_approach'].isin(contact_approaches)]            
                
                # Count of unique clients
                return df['client_id'].count() 
            else:
                #exclude admin contacts
                df = df[df['contact_themes'] != "Administrative"]
                
                # contact approach face to face/ telephone/ type talk/ video/ instant messaging (synchronous) only with attendance status attended (exclude all other approaches). 
                contact_approaches = ["Face to Face", "Telephone", "Type talk", "Video consultation", "Instant Messaging (Synchronous)"]
                df = df[df['contact_approach'].isin(contact_approaches)]            
                
                # contact session option must be either 'Support Session' or '24 hr call back'
                df = df[df['contact_session_option'].isin(["Support Session", "24 hour call back"])]
                
                # Count of unique clients
                return df['client_id'].count() 
        
        elif row == "How many unique referrals":
            return "MYMUP"
        elif row == "How many new people referred":
            return "MYMUP"
        
        elif row == "How many were declined by the service?":
            return df['client_id'].count() 
        
    
        elif row == "How many young people disengaged, couldn’t be contacted or rejected a referral?":
            # Filter by specific file closure reasons and count unique clients
            closure_reasons = ["Client did not attend", "Client requested discharge", "Client disengages", "Refused to be seen", "Client rejects referral", "Client not available for pre-arranged appointments", "Organisation cannot contact Client prior to assessment", "Client declined a service prior or during assessment"]
            df_filtered = df[df['reason'].isin(closure_reasons)]
            return df_filtered['client_id'].nunique()
        # ---------------------------------------------------------------------
            
        elif row == "Active cases":
            # Count clients with no file closure date and status active, pending, processing, or waiting list
            active_statuses = ["active", "pending", "processing", "waiting list"]
            # df_active = df[df['client_status'].isin(active_statuses) & df['file_closure_date'].isna()]
            # df_active = df[df['client_status'].isin(active_statuses) & df['file_closure_date'].isna()]
            return df['client_id'].nunique()
        
        elif row == "How many people have moved on":
            # Filter by specific file closure reasons for moving on and count unique clients
            move_on_reasons = ["Planned ending met outcomes at Assessment Point", "Planned ending without review", "Treatment completed", "Decision made at review", "No further treatment required", "Single episode"]
            df_moved_on = df[df['reason'].isin(move_on_reasons)]
            return df_moved_on['client_id'].nunique()
        
        
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