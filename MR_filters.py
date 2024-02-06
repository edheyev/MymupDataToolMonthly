# -*- coding: utf-8 -*-
"""
Created on Tues Feb 06 15:58:58 2023

@author: Ed Heywood-Everett
"""
import pandas as pd

def OCR_filter(df, row, dfname="empty"):
    try:
        if row == "Number referrals":
            return df
        return "row not caught"
    except Exception as e:
        print(
            f"Error in common_demographic_filter with row : {e}. Current df: {dfname}"
        )
        raise Exception(
            f"Error in common_demographic_filter with row : {e} . current df is {dfname}"
        )
        
        
def CIC_CLA_caseload_and_referrals_filter(df, row, dfname="empty"):

    return "not yet implemented"



filter_function_map = {
    "Overall_caseload_and_referrals":OCR_filter,
    "CIC_CLA_caseload_and_referrals":CIC_CLA_caseload_and_referrals_filter,
    # "SEN_caseload_and_referrals":,
    # "EHCP_caseload_and_referrals":,
    # "CRAVEN_caseload_and_referrals":,
    # "BRADFORD_DISTRICT_caseload_and_referrals":,
    # "All_Referrals_by_demographics":,
    # "All_CIC_CLA_Referrals_by_demographics":,
    # "All_SEN_Referrals_by_demographics":,
    # "All_EHCP_Referrals_by_demographics":,
    # "All_CRAVEN_Referrals_by_demographics":,
    # "BRADFORD_DISTRICT_Referrals_by_demographics":,
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
