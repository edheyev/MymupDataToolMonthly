# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:58:58 2023

@author: Edloc
"""

import pandas as pd

def column_filter(df, column):
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
            return df[df['service_type'] == "Know Your Mind"]
        elif column == "MIB Know Your Mind +":
            return df[df['service_type'] == "Know Your Mind Plus"]
        elif column == "MIB Hospital Buddys Airedale General":
            return df[df['service_type'] == "Hospital Buddies AGH"]
        elif column == "MIB Hospital Buddys BRI":
            return df[df['service_type'] == "Hospital Buddies BRI"]
        elif column == "SELFA (Mighty Minds)":
            return df[(df['franchise'] == "Selfa") & (df['contact_service_type'] == "Mighty Minds")]
        else:
            print("column not recognised by filters")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error in row_filter with row {column}: {e}")
        return pd.DataFrame({'error': [True]})  # Return DataFrame with an error flag

def row_filter(df, row):
    try:
        #print("Row Filter: "+ row)
        if row == "Number of unique people supported (old rule)":
            return "MYMUP"
        elif row == "Number of unique people supported":
            return df['client_id'].count() 
        elif row == "How many unique referrals":
            return "MYMUP"
        elif row == "How many new people referred":
            return "MYMUP"
        elif row == "How many were declined by the service?":
            return df['client_id'].count() 
        elif row == "How many young people disengaged, couldn’t be contacted or rejected a referral?":
            return pd.DataFrame()
        elif row == "Active cases":
            return pd.DataFrame()
        elif row == "How many people have moved on":
            return pd.DataFrame()
        elif row == "% clients with initial contact 5 days after referral (new rule)":
            return pd.DataFrame()
        elif row == "% clients with initial contact within 7 days of referral (old rule not including admin contacts)":
            return pd.DataFrame()
        elif row == "% clients who had the first support session offered within 21 days of referral":
            return pd.DataFrame()
        elif row == "% clients attended the first contact by video/face to face/telephone within 21 days of referral":
            return pd.DataFrame()
        else:
            print("Row not recognised by filters")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in row_filter with row {row}: {e}")
    return "error"