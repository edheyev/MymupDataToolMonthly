# Define your franchise lists for each CSV
yim_providers = [
    "Barnardos WRAP",
    "Bradford Youth Service",
    "Brathay", #magic service type only to do
    "Inspired Neighbourhoods", #todo check this one
    "Mind in Bradford",
    "Selfa"
]

other_vcse = [
    "All Star Youth Entertainment",
    "Bradford Counselling Service",
    "Bradford Bereavement Support",
    "Family Action Bradford",
    "Roshnighar",
    "STEP2 Young People&#039;s Health",# check this one
    "The Cellar Trust"
]

file_info = {
    "CYPMH_Clients_All": {
        "filename": "cypmh_clients_all",
        "columns": [],
    },
    "CYPMH_Contacts_All": {
        "filename": "cypmh_contacts_all",
        "columns": [],
    },
    "CYPMH_File_Closures_All": {
        "filename": "cypmh_file_closures_all",
        "columns": [],
    },
    "CYPMH_Goal_Themes_All": {
        "filename": "cypmh_goal_themes_all",
        "columns": [],
    },
    "CYPMH_Plans_And_Goals_All": {
        "filename": "cypmh_plans_and_goals_all",
        "columns": [],
    },
    "CYPMH_Referral_Rejections_All": {
        "filename": "cypmh_referral_rejections_all",
        "columns": [],
    },
    "CYPMH_Referrals": {
        "filename": "cypmh_referrals",
        "columns": [],
    },
    "CYPMH_Referrals_MIB": {
        "filename": "cypmh_referrals_mib",
        "columns": [],
    },
    "CYPMH_Two_Contacts": {
        "filename": "cypmh_two_contacts",
        "columns": [],
    },
    "CYPMH_Two_Contacts_MIB": {
        "filename": "cypmh_two_contacts_mib",
        "columns": [],
    },
}

Overall_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "Overall_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

CIC_CLA_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "CIC_CLA_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

SEN_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "SEN_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

EHCP_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "EHCP_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

CRAVEN_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "CRAVEN_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

BRADFORD_DISTRICT_caseload_and_referrals = {
    "sheet_name": "Case_Status_Split",
    "table_name": "BRADFORD_DISTRICT_caseload_and_referrals",
    "row_names": [
        "Number referrals",
        "Number unique referrals",
        "Referrals accepted",
        "Referrals refused",
        "Number open cases",
        "Number closed cases",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

All_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "All_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

All_CIC_CLA_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "All_CIC_CLA_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
    },    
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

All_SEN_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "All_SEN_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

All_EHCP_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "All_EHCP_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

All_CRAVEN_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "All_CRAVEN_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

BRADFORD_DISTRICT_Referrals_by_demographics = {
    "sheet_name": "Demographic_split ",
    "table_name": "BRADFORD_DISTRICT_Referrals_by_demographics",
    "row_names": [
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
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Other (not listed)",
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
        "White and Black Carribean",
        "White British",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Unknown Ethnicity",
    ],
    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

referrals_row_names = [
    "GP services",
    "Other Primary Health Care",
    "Primary care",
    "Self Referral",
    "Self",
    "Carer",
    "Social Services",
    "Education Service",
    "Housing Service",
    "Police",
    "Youth Offending Service",
    "School Nurse",
    "Hospital-based Paediatrics",
    "Community-based Paediatrics",
    "Voluntary Sector",
    "Accident And Emergency Department",
    "Other secondary care specialty",
    "Out of Area Agency",
    "Drug Action Team / Drug Misuse Agency",
    "Other service or agency",
    "Single Point of Access Service",
    "Internal Referral",
    "CAMHS Core/Step down",
    "CAMHS Waiting List",
    "CAMHS Crisis",
    "Transfer by graduation from Child Adolescent Mental Health Services to Adult",
    "VCS",
    "Unknown",
    "Community Mental Health Team (Adult Mental Health)",
    "Employer",
    "Employer: Occupational Health",
    "Family Support Worker",
    "Improving Access to Psychological Therapies Service",
    "Independent Sector: Low secure Inpatients",
    "Independent Sector: Medium secure Inpatients",
    "Inpatient Service Child and Adult Mental Health",
    "Inpatient Service Learning Disabilities",
    "Justice System: Court Liaison and Diversion Service",
    "Justice System: Courts",
    "Justice System: Police",
    "Justice System: Prison",
    "Justice System: Probation",
    "Justice System: Youth Offending Team",
    "Local Authority and Other Public Services: Education Service / Educational Establishment",
    "Local Authority and Other Public Services: Housing Service",
    "Local Authority and Other Public Services: Social Services",
    "Mental Health Drop In Service",
    "Not Known",
    "Other Independent Sector Mental Health Services",
    "Other: Asylum Services",
    "Other: Job Centre Plus",
    "Other: Single Point of Access Service",
    "Other: Urgent and Emergency Care Ambulance Service",
    "Permanent Transfer from Another Mental Health Trust",
    "Primary Health Care: Health Visitor",
    "Primary Health Care: Maternity Service",
    "Temporary Transfer from Another Mental Health Trust",
    "Blank (nothing selected)"
    ],

Source_of_All_Referrals = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_All_Referrals",
    "row_names": referrals_row_names[0],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPHM_",
    "row_db_default": "CYPMH_Referrals",
}

Source_of_Referrals___CIC_CLA = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_Referrals_CIC_CLA",
    "row_names": referrals_row_names[0],
    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Referrals",
}

Source_of_Referrals___SEN = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_Referrals_SEN",
    "row_names": referrals_row_names[0],

    "placeholder_text": {
       
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Referrals",
}

Source_of_Referrals___EHCP = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_Referrals_EHCP",
    "row_names": referrals_row_names[0],

    "placeholder_text": {
       
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Referrals",
}

Source_of_Referrals___CRAVEN = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_Referrals_CRAVEN",
    "row_names": referrals_row_names[0],

    "placeholder_text": {
        
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Referrals",
}

Source_of_Referrals___BRADFORD_DISTRICT = {
    "sheet_name": "Referral_Source",
    "table_name": "Source_of_Referrals_BRADFORD_DISTRICT",
    "row_names": referrals_row_names[0],

    "placeholder_text": {
       
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Referrals",
}

No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_ = {
    "sheet_name": "Two_attended_contacts_data",
    "table_name": "No_of_CYP_receiving_a_second_attended_contact_with_mental_health_services",
    "row_names": ["All", "CIC/CLA", "SEN", "EHCP", "CRAVEN", "BRADFORD DISTRICT"],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts",
    "row_db_default": "CYPMH_Two_Contacts",
}


DNAs_and_cancellations = {
    "sheet_name": "DNA",
    "table_name": "DNAs_and_cancellations",
    "row_names": [
        "All DNA Appointments",
        "All Cancelled by patient",
        "All Cancelled by Provider",
        "CIC/CLA DNA Appointments",
        "CIC/CLA Cancelled by patient",
        "CIC/CLA Cancelled by Provider",
        "SEN DNA Appointments",
        "SEN Cancelled by patient",
        "SEN Cancelled by Provider",
        "EHCP DNA Appointments",
        "EHCP Cancelled by patient",
        "EHCP Cancelled by Provider",
        "CRAVEN DNA Appointments",
        "CRAVEN Cancelled by patient",
        "CRAVEN Cancelled by Provider",
        "BRADFORD DISTRICT DNA Appointments",
        "BRADFORD DISTRICT Cancelled by patient",
        "BRADFORD DISTRICT Cancelled by Provider",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Contacts_All",
}

Goals_Based_Outcomes = {
    "sheet_name": "Outcome_Data",
    "table_name": "Goals_Based_Outcomes",
    "row_names": [
        "Number All Initials completed",
        "Number All Follow ups completed",
        "Average Initial score",
        "Average Follow up score",
        "Number CIC/CLA Initials completed",
        "Number CIC/CLA Follow ups completed",
        "Average CIC/CLA Initial score",
        "Average CIC/CLA Follow up score",
        "Number SEN Initials completed",
        "Number SEN Follow ups completed",
        "Average SEN Initial score",
        "Average SEN Follow up score",
        "Number EHCP Initials completed",
        "Number EHCP Follow ups completed",
        "Average EHCP Initial score",
        "Average EHCP Follow up score",
        "Number CRAVEN Initials completed",
        "Number CRAVEN Follow ups completed",
        "Average CRAVEN Initial score",
        "Average CRAVEN Follow up score",
        "Number BRADFORD DISTRICT Initials completed",
        "Number BRADFORD DISTRICT Follow ups completed",
        "Average BRADFORD DISTRICT Initial score",
        "Average BRADFORD DISTRICT Follow up score",
    ],
    "placeholder_text": {
        # "Number All Initials completed": "todo",
        # "Number All Follow ups completed": "todo",
        # "Average Initial score": "todo",
        # "Average Follow up score": "todo",
        # "Number CIC/CLA Initials completed": "todo",
        # "Number CIC/CLA Follow ups completed": "todo",
        # "Average CIC/CLA Initial score": "todo",
        # "Average CIC/CLA Follow up score": "todo",
        # "Number SEN Initials completed": "todo",
        # "Number SEN Follow ups completed": "todo",
        # "Average SEN Initial score": "todo",
        # "Average SEN Follow up score": "todo",
        # "Number EHCP Initials completed": "todo",
        # "Number EHCP Follow ups completed": "todo",
        # "Average EHCP Initial score": "todo",
        # "Average EHCP Follow up score": "todo",
        # "Number CRAVEN Initials completed": "todo",
        # "Number CRAVEN Follow ups completed": "todo",
        # "Average CRAVEN Initial score": "todo",
        # "Average CRAVEN Follow up score": "todo",
        # "Number BRADFORD DISTRICT Initials completed": "todo",
        # "Number BRADFORD DISTRICT Follow ups completed": "todo",
        # "Average BRADFORD DISTRICT Initial score": "todo",
        # "Average BRADFORD DISTRICT Follow up score": "todo",
    },
    "mib_row_db_default": "CYPMH_Plans_And_Goals_All",
    "row_db_default": "CYPMH_Plans_And_Goals_All",
}

All_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "All_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

CIC_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "CIC_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

SEN_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "SEN_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

EHCP_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "EHCP_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

CRAVEN_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "CRAVEN_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

Bradford_District_Goal_Themes = {
    "sheet_name": "Goal_Themes",
    "table_name": "Bradford_District_Goal_Themes",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
        "TOTAL",
    ],
    "placeholder_text": {
        # "Being able to maintain and build positive relationships": "todo",
        # "Being able to support others": "todo",
        # "Being better at managing my emotional wellbeing": "todo",
        # "Being better at managing risks and feeling safer": "todo",
        # "Covid-19 Support": "todo",
        # "Improving my confidence and self esteem": "todo",
        # "Improving my physical wellbeing": "todo",
        # "Reducing my isolation": "todo",
        # "Understanding who I am": "todo",
        # "TOTAL": "todo",
    },
    "mib_row_db_default": "CYPMH_Goal_Themes_All",
    "row_db_default": "CYPMH_Goal_Themes_All",
}

Overall_Discharges = {
    "sheet_name": "Discharge_Data",
    "table_name": "Overall_Discharges",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
        "Not Disclosed",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Discharges_CIC_CLA = {
    "sheet_name": "Discharge_Data",
    "table_name": "Discharges_CIC_CLA",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
        "Not Disclosed",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Discharges_SEN = {
    "sheet_name": "Discharge_Data",
    "table_name": "Discharges_SEN",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
        "Not Disclosed",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Discharges_EHCP = {
    "sheet_name": "Discharge_Data",
    "table_name": "Discharges_EHCP",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
    ],
    "placeholder_text": {
        },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Discharges_CRAVEN = {
    "sheet_name": "Discharge_Data",
    "table_name": "Discharges_CRAVEN",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Discharges_BRADFORD_DISTRICT = {
    "sheet_name": "Discharge_Data",
    "table_name": "Discharges_BRADFORD_DISTRICT",
    "row_names": [
        "Number completed treatment",
        "Number inappropriate referrals",
        "Number who could not be contacted",
        "Number disengaged",
        "Number signposted to another CCG provider",
        "Not Disclosed",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_File_Closures_All",
    "row_db_default": "CYPMH_File_Closures_All",
}

Overall_Number_on_Waiting_list = {
    "sheet_name": "Wait_List_Data",
    "table_name": "Overall_Number_on_Waiting_list",
    "row_names": ["All", "CIC/CLA", "SEN", "EHCP", "CRAVEN", "BRADFORD DISTRICT"],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Referrals",
    "row_db_default": "CYPMH_Referrals",
}

Overall_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "Overall_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts",
    "row_db_default": "CYPMH_Two_Contacts",
}

CIC_CLA_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "CIC_CLA_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts_MIB",
    "row_db_default": "CYPMH_Two_Contacts_MIB",
}

SEN_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "SEN_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts_MIB",
    "row_db_default": "CYPMH_Two_Contacts_MIB",
}

EHCP_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "EHCP_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts_MIB",
    "row_db_default": "CYPMH_Two_Contacts_MIB",
}

CRAVEN_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "CRAVEN_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts_MIB",
    "row_db_default": "CYPMH_Two_Contacts_MIB",
}

BRADFORD_DISTRICT_Wait_Times = {
    "sheet_name": "Wait_Times",
    "table_name": "BRADFORD_DISTRICT_Wait_Times",
    "row_names": [
        "Average Weeks from referral to 1st attended contact/indirect",
        "Average Weeks from referral to 2nd attended contact/indirect",
        "Average Weeks between 1st Attended contact/Indirect & 2nd attended contact/indirect",
    ],
    "placeholder_text": {
    },
    "mib_row_db_default": "CYPMH_Two_Contacts_MIB",
    "row_db_default": "CYPMH_Two_Contacts_MIB",
}

Yim_Live = {
    "sheet_name": "YIM_LIVE_&_KCU_Delivery",
    "table_name": "Yim_Live",
    "row_names": ["Number Sessions", "Number Participants"],
    "placeholder_text": {"Number Sessions": "todo", "Number Participants": "todo"},
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

KCU = {
    "sheet_name": "YIM_LIVE_&_KCU_Delivery",
    "table_name": "KCU",
    "row_names": ["Number Schools/Youth Settings", "Number Participants"],
    "placeholder_text": {
        "Number Schools/Youth Settings": "todo",
        "Number Participants": "todo",
    },
    "mib_row_db_default": "CYPMH_Clients_All",
    "row_db_default": "CYPMH_Clients_All",
}

table_configs = [
    Overall_caseload_and_referrals,
    CIC_CLA_caseload_and_referrals,
    SEN_caseload_and_referrals,
    EHCP_caseload_and_referrals,
    CRAVEN_caseload_and_referrals,
    BRADFORD_DISTRICT_caseload_and_referrals,
    All_Referrals_by_demographics,
    All_CIC_CLA_Referrals_by_demographics,
    All_SEN_Referrals_by_demographics,
    All_EHCP_Referrals_by_demographics,
    All_CRAVEN_Referrals_by_demographics,
    BRADFORD_DISTRICT_Referrals_by_demographics,
    Source_of_All_Referrals,
    Source_of_Referrals___CIC_CLA,
    Source_of_Referrals___SEN,
    Source_of_Referrals___EHCP,
    Source_of_Referrals___CRAVEN,
    Source_of_Referrals___BRADFORD_DISTRICT,
    No__of_CYP_receiving_a_second_attended_contact_with_mental_health_services_,
    DNAs_and_cancellations,
    Goals_Based_Outcomes,
    All_Goal_Themes,
    CIC_Goal_Themes,
    SEN_Goal_Themes,
    EHCP_Goal_Themes,
    CRAVEN_Goal_Themes,
    Bradford_District_Goal_Themes,
    Overall_Discharges,
    Discharges_CIC_CLA,
    Discharges_SEN,
    Discharges_EHCP,
    Discharges_CRAVEN,
    Discharges_BRADFORD_DISTRICT,
    Overall_Number_on_Waiting_list,
    Overall_Wait_Times,
    CIC_CLA_Wait_Times,
    SEN_Wait_Times,
    EHCP_Wait_Times,
    CRAVEN_Wait_Times,
    BRADFORD_DISTRICT_Wait_Times,
    Yim_Live,
    KCU,
]
