file_info = {
    "Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "contacts_or_indirects_within_reporting_period.csv",
        "columns": ["client_id", 
                    "franchise", 
                    "contact_service_type", 
                    "contact_themes", 
                    "contact_approach", 
                    "client_gender",
                    "client_ethnicity",
                    "client_disability",
                    "client_sexuality",
                    "client_age",
                    "client_area",
                    "client_asylum_seeker",
                    "client_sen",
                    "client_ehcp",
                    "client_exploitation_risk",
                    "client_leaving_care",
                    "client_lac",
                    "client_cpp",
                    "client_cinp",
                    "client_young_carer",
                    "contact_attendance",
                    "contact_themes",
                    ],
    },
    "MIB_Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "mib_contacts_or_indirects_within_reporting_period.csv",
        "columns": ["client_id", 
                    "franchise", 
                    "contact_service_type", 
                    "contact_themes", 
                    "contact_approach", 
                    "client_gender",
                    "client_ethnicity",
                    "client_disability",
                    "client_sexuality",
                    "client_age",
                    "client_area",
                    "client_asylum_seeker",
                    "client_sen",
                    "client_ehcp",
                    "client_exploitation_risk",
                    "client_leaving_care",
                    "client_lac",
                    "client_cpp",
                    "client_cinp",
                    "client_young_carer",
                    "contact_attendance",
                    "contact_session_option",
                    "contact_themes",
                    ],
    },
    "File_Closures_And_Goals_Within_Reporting_Period": {
        "filename": "file_closures_and_goals_within_reporting_period.csv",
        "columns": ["client_id", 'referral_date', 'reason', 'goal_score_date', 'file_closure_date','initial_/_followup_/_final'],
    },
    "MIB_File_Closures_And_Goals_Within_Reporting_Period": {
        "filename": "mib_file_closures_and_goals_within_reporting_period.csv",
        "columns": ["client_id", 'referral_date', 'reason', 'goal_score_date', 'file_closure_date','initial_/_followup_/_final'],

    },
    "File_Closures_Within_Reporting_Period": {
        "filename": "file_closures_within_reporting_period.csv",
        "columns": ["client_id","reason"],
    },
    "Initial_Goals_Within_Reporting_Period": {
        "filename": "initial_goals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "Referrals_Within_Reporting_Period": {
        "filename": "referrals_within_reporting_period.csv",
        "columns": ["client_id","source","reason","reason_other"],
    },
    "MIB_Referrals_Within_Reporting_Period": {
        "filename": "mib_referrals_within_reporting_period.csv",
        "columns": ["client_id","source","reason","reason_other"],
    },
    "Referrals_Before_End_Reporting_Period": {
        "filename": "referrals_before_end_reporting_period.csv",
        "columns": ["client_id","client_status"],
    },
    "MIB_Referrals_Before_End_Reporting_Period": {
        "filename": "mib_referrals_before_end_of_reporting_period.csv",
        "columns": ["client_id","client_status"],
    },
    "Contacts_Within_Seven_Days": {
        "filename": "contacts_within_seven_days.csv",
        "columns": ["client_id", "file_closure_service_type",'referral_date', 'file_closure_date', 'contact_/_indirect_date'],
    },
    "MIB_Contacts_Within_Seven_Days": {
        "filename": "mib_contacts_within_seven_days.csv",
        "columns": ["client_id", "file_closure_service_type",'referral_date', 'file_closure_date', 'contact_/_indirect_date'],
    },
    "Contacts_Within_Twenty_One_Days": {
        "filename": "contacts_within_twenty_one_days.csv",
        "columns": ["client_id", "file_closure_service_type",'referral_date', 'file_closure_date', 'contact_/_indirect_date'],
    },
    "MIB_Contacts_Within_Twenty_One_Days": {
        "filename": "mib_contacts_within_twenty_one_days.csv",
        "columns": ["client_id", "file_closure_service_type",'referral_date', 'file_closure_date', 'contact_/_indirect_date'],
    },
    # "Attended_Contacts_Within_Twenty_One_Days": {
    #     "filename": "attended_contacts_within_twenty_one_days.csv",
    #     "columns": ["client_id"],
    # },
    # "MIB_Attended_Contacts_Within_Twenty_One_Days": {
    #     "filename": "mib_attended_contacts_within_twenty_one_days.csv",
    #     "columns": ["client_id"],
    # },
    # "Contacts_After_Referrals": {
    #     "filename": "contacts_after_referrals.csv",
    #     "columns": ["client_id"],
    # },
    # "MIB_Contacts_After_Referrals": {
    #     "filename": "mib_contacts_after_referrals.csv",
    #     "columns": ["client_id"],
    # },
    # Add more file information as needed
}

# yim_providers = [
#     "Barnardos",
#     "Bradford Youth Service (BYS)",
#     "Brathay -MAGIC service type only",
#     "INCIC -service type CYP only",
#     "Mind in Bradford (MiB) service type Know Your Mind, Know Your Mind plus, Hospital Buddies BRI and Hospital Buddies  AGH only",
#     "SELFA",
# ]

# Other_VCSE = [
#     "All Star Youth Entertainment",
#     "Bradford Counselling Service",
#     "Bradford Bereavement Support",
#     "Family Action Bradford",
#     "Roshnighar",
#     "STEP 2",
#     "The Cellar Trust",
# ]

service_info_config = {
    "table_name": "service_info_config",
    "row_names": [
        "Number of unique people supported (old rule)",
        "Number of unique people supported",
        "How many unique referrals",
        "How many new people referred",
        "How many were declined by the service?",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?",
        "Active cases",
        "How many people have moved on",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)",
        "% clients who had the first support session offered within 21 days of referral",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Number of unique people supported (old rule)": "MYMUP_URL",
        "How many unique referrals": "DO THIS!!!",
        "How many new people referred": "MYMUP_URL",
        "How many were declined by the service?": "CHECK THIS",
        #"% clients with initial contact within 7 days of referral (old rule not including admin contacts)": "to do?",
        # "% clients who had the first support session offered within 21 days of referral": "to do?",
        #"% clients attended the first contact by video/face to face/telephone within 21 days of referral": "to do?",
    },
    "row_db_logic": {
        "How many were declined by the service?": "File_Closures_Within_Reporting_Period",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?": "File_Closures_Within_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "Active cases": "Referrals_Before_End_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)":"Contacts_Within_Seven_Days",
        "% clients who had the first support session offered within 21 days of referral":"Contacts_Within_Twenty_One_Days",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral":"Contacts_Within_Twenty_One_Days",
    },
    "mib_row_db_logic": {
        "How many were declined by the service?": "File_Closures_Within_Reporting_Period",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?": "File_Closures_Within_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "Active cases": "MIB_Referrals_Before_End_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)":"MIB_Contacts_Within_Seven_Days",
        "% clients who had the first support session offered within 21 days of referral":"MIB_Contacts_Within_Twenty_One_Days",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral":"MIB_Contacts_Within_Twenty_One_Days",
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

yp_gender_config = {
    "table_name": "yp_gender_config",
    "row_names": [
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Prefer not to say",
        "Transgendered",
        "Other (not listed)",
        "Blank (nothing selected)",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Female (including Transgender Woman)": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Male (including Transgender Man)": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Non-Binary": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known (Person stated Gender Code not recorded)": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No Stated (patient asked but declined to provide a response)": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Prefer not to say": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Transgendered": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Other (not listed)": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Female (including Transgender Woman)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Male (including Transgender Man)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Non-Binary": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known (Person stated Gender Code not recorded)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No Stated (patient asked but declined to provide a response)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Prefer not to say": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Transgendered": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Other (not listed)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'mib_row_db_default:': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default:': 'Contacts_Or_Indirects_Within_Reporting_Period',
    
}

yp_ethnicity_config = {
    "table_name": "yp_ethnicity_config",
    "row_names": [
        "African",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Arab",
        "Bangladeshi",
        "British",
        "Caribbean",
        "Central and Eastern European",
        "Chinese",
        "Gypsy/Roma/Traveller",
        "Indian",
        "Irish",
        "Latin America",
        "Not known",
        "Not stated",
        "Pakistani",
        "White and Asian",
        "White and Black African",
        "White and Black Caribbean",
        "Blank (nothing selected)",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # row: "Contacts_Or_Indirects_Within_Reporting_Period" for row in row_names
    },
    "mib_row_db_logic": {
        # row: "MIB_Contacts_Or_Indirects_Within_Reporting_Period" for row in row_names
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',  # Removed colon
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',  # Removed colon
}

yp_disabilty_config = {
    "table_name": "yp_disability_config",
    "row_names": [
        "Autism or other Neurological condition",
        "Behaviour and Emotional",
        "Hearing",
        "Manual Dexterity",
        "Memory or ability to concentrate, learn or understand (Learning Disability)",
        "Mobility and Gross Motor",
        "No disability",
        "Not Known",
        "Not stated (Person asked but declined to provide a response)",
        "Other",
        "Perception of Physical Danger",
        "Personal, Self-Care and Continence",
        "Progressive Conditions and Physical Health (such as HIV, Cancer, Multiple Sclerosis, Fits)",
        "Sight",
        "Speech",
        "Yes",
        "Blank (nothing selected)",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # row: "Contacts_Or_Indirects_Within_Reporting_Period" for row in row_names
    },
    "mib_row_db_logic": {
        # row: "MIB_Contacts_Or_Indirects_Within_Reporting_Period" for row in row_names
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',  # Removed colon
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',  # Removed colon
}

yp_sexual_orientation_config = {
    "table_name": "yp_sexual_orientation_config",
    "row_names": [
        "Asexual",
        "Bisexual",
        "Gay",
        "Heterosexual or Straight",
        "Lesbian",
        "Not asked/Unknown",
        "Not stated (Person asked but declined to provide a response)",
        "Other",
        "Pansexual",
        "Person asked and did not know/is unsure or undecided",
        "Blank (nothing selected)",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Asexual": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Bisexual": "Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each row name)
    },
    "mib_row_db_logic": {
        "Asexual": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Bisexual": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each row name)
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',  
    
}

yp_age_config = {
    "table_name": "yp_age_config",
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
        "Out of age Range",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Map each age to its corresponding logic
        "Age 3": "Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each age)
    },
    "mib_row_db_logic": {
        # Map each age to its corresponding MIB logic
        "Age 3": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each age)
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_area_config = {
    "table_name": "yp_area_config",
    "row_names": [
    "BAILDON",
    "Bentham",
    "BINGLEY",
    "BINGLEY RURAL",
    "BOLTON & UNDERCLIFFE",
    "BOWLING & BARKEREND",
    "BRADFORD MOOR",
    "CITY",
    "CLAYTON & FAIRWEATHER GREEN",
    "CRAVEN",
    "Craven Ward - Aire Valley-with-Lothersdale",
    "Craven Ward - Barden Fell",
    "Craven Ward - Cowling",
    "Craven Ward - Embsay-with-Eastby",
    "Craven Ward - Gargrave and Malhamdale",
    "Craven Ward - Glusburn",
    "Craven Ward - Grassington",
    "Craven Ward - Hellifield and Long Preston",
    "Craven Ward - Penyghent",
    "Craven Ward - Settle and Ribblebanks",
    "Craven Ward - Skipton East",
    "Craven Ward - Skipton North",
    "Craven Ward - Skipton South",
    "Craven Ward - Skipton West",
    "Craven Ward - Sutton-in-Craven",
    "Craven Ward - Upper Wharfedale",
    "Craven Ward - West Craven",
    "ECCLESHILL",
    "GREAT HORTON",
    "HEATON",
    "IDLE & THACKLEY",
    "ILKLEY",
    "KEIGHLEY CENTRAL",
    "KEIGHLEY EAST",
    "KEIGHLEY WEST",
    "LITTLE HORTON",
    "MANNINGHAM",
    "OUT OF AREA",
    "QUEENSBURY",
    "ROYDS",
    "SHIPLEY",
    "THORNTON & ALLERTON",
    "TOLLER",
    "TONG",
    "WHARFEDALE",
    "WIBSEY",
    "WINDHILL & WROSE",
    "WORTH VALLEY",
    "WYKE",
    "Blank (nothing selected )"
]
,
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Map each area to its corresponding logic
        "BAILDON": "Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each area)
    },
    "mib_row_db_logic": {
        # Map each area to its corresponding MIB logic
        "BAILDON": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        # ... (and so on for each area)
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_asylum_status_config = {
    "table_name": "yp_asylum_status_config",
    "row_names": ["Yes", "No", "Not known", "Blank (nothing selected )"],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Yes": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Yes": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_special_ed_needs_config = {
    "table_name": "yp_special_ed_needs_config",
    "row_names": [
        "No",
        "Not known",
        "Yes",
        "Not applicable",
        "Blank (nothing selected )",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
    },
    "mib_row_db_logic": {
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_ed_health_care_plan_config = {
    "table_name": "yp_ed_health_care_plan_config",
    "row_names": [
        "Yes",
        "No",
        "Not known",
        "Not applicable",
        "Blank (nothing selected )",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Yes": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not applicable": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Yes": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not applicable": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_at_risk_exploitation_config = {
    "table_name": "yp_at_risk_exploitation_config",
    "row_names": ["Yes", "No", "Not known", "Blank (nothing selected )"],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Yes": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Yes": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected )": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_leaving_care_config = {
    "table_name": "yp_leaving_care_config",
    "row_names": ["Yes", "No", "Not Known", "Blank (nothing selected)"],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Yes": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not Known": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Yes": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not Known": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_looked_after_child_config = {
    "table_name": "yp_looked_after_child_config",
    "row_names": ["Yes", "No", "Not known", "Blank (nothing selected)"],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        "Yes": "Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "Contacts_Or_Indirects_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Yes": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "No": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Not known": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "Blank (nothing selected)": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
    },
    'row_db_default:': 'Contacts_Or_Indirects_Within_Reporting_Period',
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 

}

yp_child_protection_plan_config = {
    "table_name": "yp_child_protection_plan_config",
    "row_names": [
        "No",
        "Has never been subject to a plan",
        "Not known",
        "Has been previously subject to a plan",
        "Is currently subject to a plan",
        "Under assessment",
        "Blank (nothing selected)",
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
    
}

yp_child_in_need_plan_config = {
    "table_name": "yp_child_in_need_plan_config",
    "row_names": [
        "Is currently subject to a Child in need plan",
        "No",
        "Has never been subject to a Child in need plan",
        "Not known",
        "Has previously been subject to a Child in need plan",
        "Under assessment",  # Not found in your dataset
        "Blank (nothing selected)" # Handling for blank entries
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
}

yp_young_carer_config = {
    "table_name": "yp_young_carer_config",
    "row_names": [
        "Yes",
        "No",
        "Not known",
        "Not stated",
        "Blank (nothing selected)" # Handling for blank entries
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
}


total_attended_contacts_config = {
    "table_name": "total_attended_contacts_config",
    "row_names": [
        "Total Number of Attended Contacts",
        "One to One Contacts",
        "Group Contacts",
        "Indirect Activities",
        "Other (email and text)",
        "Admin Contacts",
        "Total number of DNA Contacts",
        "Percentage of DNA Contacts"
    ],
    "column_headings": [
        "Q1_Totals",
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each row, if needed
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each row, if needed
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period', 
}

goals_based_outcomes_config = {
    "table_name": "goals_based_outcomes_config",
    "row_names": [
        "% of closed cases with initial outcomes measure completed",
        "% of closed cases with follow-up/final outcomes measure completed",
        "% of GBOs demonstrating reliable change",
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "% of closed cases with initial outcomes measure completed":"XXX",
        "% of closed cases with follow-up/final outcomes measure completed":"XXX",
        "% of GBOs demonstrating reliable change":"XXX",
    },
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_File_Closures_And_Goals_Within_Reporting_Period',
    'row_db_default': 'File_Closures_And_Goals_Within_Reporting_Period',
}

average_goals_based_outcomes_config = {
    "table_name": "average_goals_based_outcomes_config",
    "row_names": [
        "% of closed cases that have an initial and follow-up/final paired GBO",
        "% of closed cases with reliable change in paired GBO",
        "Average impact score of all paired goals",
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {        
        #"% of closed cases with reliable change in paired GBO":"todo",
        #"Average impact score of all paired goals":"todo",
        },
    "row_db_logic": {
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_File_Closures_And_Goals_Within_Reporting_Period',
    'row_db_default': 'File_Closures_And_Goals_Within_Reporting_Period',
}

goal_themes_goals_based_outcomes_config = {
    "table_name": "goal_themes_goals_based_outcomes_config",
    "row_names": [
        "Being able to maintain and build positive relationships",
        "Being able to support others",
        "Being better at managing my emotional wellbeing",
        "Being better at managing risks and feeling safer",
        "Covid-19 Support",
        "Improving my confidence and self-esteem",
        "Improving my physical wellbeing",
        "Reducing my isolation",
        "Understanding who I am",
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'Initial_Goals_Within_Reporting_Period',
    'row_db_default': 'Initial_Goals_Within_Reporting_Period',
}

dss_goals_based_outcomes_config = {
    "table_name": "dss_goals_based_outcomes_config",
    "row_names": [
        "How many unique clients have had a distress scale score in reporting period",
        "Average change score for distress scale",
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "How many unique clients have had a distress scale score in reporting period":"MIB_MasEx",
        "Average change score for distress scale":"MIB_MasEx",
        },
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_File_Closures_And_Goals_Within_Reporting_Period',
    'row_db_default': 'File_Closures_And_Goals_Within_Reporting_Period',
}

contacts_by_theme_config = {
    "table_name": "contacts_by_theme_config",
    "row_names": [
        "Abuse / exploitation",
        "Administrative",
        "Activities / opportunities",
        "Anger",
        "Anxiety / stress",
        "Bereavement / grief / loss",
        "Boyfriend / girlfriend relationships",
        "Bullying",
        "Caring for others",
        "Covid-19 support",
        "Depression / low mood",
        "Domestic abuse",
        "Eating difficulties",
        "Family relationships / home life",
        "Finances / debt /poverty",
        "Friendships",
        "Harm to others",
        "Hearing Voices",
        "Homelessness",
        "Identity issues",
        "Ill Health",
        "In Crisis/De-escalation",
        "Issues with medication",
        "Loss Job/house",
        "Loneliness / isolation",
        "Low confidence / self-worth",
        "Low mood",
        "Neurodevelopmental issues",
        "OCD",
        "Offending behaviour",
        "Panic",
        "Phobias",
        "Physical health / illness / disability",
        "Psychosis / psychotic episodes",
        "PTSD",
        "School / college / employment",
        "Self-Care",
        "Self-Harm",
        "Sexual Violence",
        "Sleep problems",
        "Substance Misuse",
        "Suicidal Ideation",
        "Transition",
        "Trauma",
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}


source_of_referral_config = {
    "table_name": "source_of_referral_config",
   "row_names" : [
    "Primary Health Care: General Medical Practitioner Practice",
    "Accident and Emergency Department",
    "CAMHS - Core/Step Down",
    "CAMHS - Crisis Team (Hospital Urgents)",
    "CAMHS - Waiting List",
    "Child Health: Community-based Paediatrics",
    "Child Health: Hospital-based Paediatrics",
    "Child Health: School Nurse",
    "Community Mental Health Team (Adult Mental Health)",
    "Employer",
    "Employer: Occupational Health",
    "Family Support Worker",
    "Improving Access to Psychological Therapies Service",
    "Independent Sector: Low secure Inpatients",
    "Independent Sector: Medium secure Inpatients",
    "Inpatient Service Child and Adult Mental Health",
    "Inpatient Service Learning Disabilities",
    "Internal Referral",
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
    "Other Primary Health Care",
    "Other secondary care specialty",
    "Other SERVICE or agency",
    "Other: Asylum Services",
    "Other: Drug Action Team / Drug Misuse Agency",
    "Other: Job Centre Plus",
    "Other: Out of Area Agency",
    "Other: Single Point of Access Service",
    "Other: Urgent and Emergency Care Ambulance Service",
    "Permanent Transfer from Another Mental Health Trust",
    "Primary Health Care: Health Visitor",
    "Primary Health Care: Maternity Service",
    "Self-Referral :Self",
    "Self-Referral: Carer/Relative",
    "Temporary Transfer from Another Mental Health Trust",
    "Transfer by Graduation from CAMHS to Adult Mental Health Services",
    "Voluntary Sector",
    "Blank (nothing selected)"
],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Referrals_Within_Reporting_Period',
    'row_db_default': 'Referrals_Within_Reporting_Period',
}

reason_for_referral_config = {
    "table_name": "reason_for_referral_config",
    "row_names" : [
        "Adjustment to Health Issues",
        "Anxiety",
        "Attachment Difficulties",
        "Behaviour Disorder",
        "Behaviours that challenge due to a Learning Disability",
        "Bi-polar Disorder",
        "Community Perinatal Mental Health Partner Assessment",
        "Conduct Disorders",
        "Depression",
        "Diagnosed Autism",
        "Drug and Alcohol Difficulties",
        "Eating Disorders",
        "Gambling disorder",
        "Gender Discomfort Issues",
        "In Crisis",
        "Isolation",
        "Neurodevelopmental Conditions, excluding Autism",
        "Obsessive Compulsive Disorder",
        "Ongoing or Recurrent Psychosis",
        "Organic Brain Disorder",
        "Other",
        "Panic Attacks",
        "Perinatal Mental Health Issues",
        "Personality Disorders",
        "Phobias",
        "Post-Traumatic Stress Disorder",
        "Preconception Perinatal Mental Health Concern",
        "Relationship Difficulties",
        "Self-Care Issues",
        "Self-Harm Behaviours",
        "Suspected Autism",
        "(Suspected) First Episode Psychosis",
        "Unexplained Physical Symptoms",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Referrals_Within_Reporting_Period',
    'row_db_default': 'Referrals_Within_Reporting_Period',
}

other_reason_for_referral_config = {
    "table_name": "other_reason_for_referral_config",
    "row_names" : [
        "Anti-Social Behaviour",
        "At risk of CSE",
        "Bereavement",
        "Bullying",
        "Community Involvement/Participation",
        "Covid 19",
        "Criminal offending behaviour/or at risk of",
        "Dementia",
        "Discrimination",
        "Domestic Abuse",
        "Early Help",
        "Education Support",
        "Emotional Support",
        "Employability",
        "Family Problems/Home Life",
        "Family Support",
        "Financial Support",
        "Historic Domestic Abuse",
        "Homelessness",
        "Housing",
        "In Crisis",
        "LGBTQIA+ support",
        "Mental Health Support",
        "Personal Safety",
        "Physical Health",
        "Sexual Health",
        "Sexualised Abuse",
        "Sleep Hygiene",
        "Social Isolation and Loneliness",
        "Victim of CSE",
        "Wellness Health Education, Guidance and Counselling",
        "Young Carer/Adult Carer",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'MIB_Referrals_Within_Reporting_Period',
    'row_db_default': 'Referrals_Within_Reporting_Period',
}


#
# 
gender_config = {
    "table_name": "gender_config",
    "row_names": [
        "Female (including Transgender Woman)",
        "Male (including Transgender Man)",
        "Non-Binary",
        "Not known (Person stated Gender Code not recorded)",
        "No Stated (patient asked but declined to provide a response)",
        "Prefer not to say",
        "Transgendered",
        "Other (not listed)",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Female (including Transgender Woman)": "MUMUP_URL",
        "Male (including Transgender Man)": "MUMUP_URL",
        "Non-Binary": "MUMUP_URL",
        "Not known (Person stated Gender Code not recorded)": "MUMUP_URL",
        "No Stated (patient asked but declined to provide a response)": "MUMUP_URL",
        "Prefer not to say": "MUMUP_URL",
        "Transgendered": "MUMUP_URL",
        "Other (not listed)": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
        },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

ethnicity_config = {
    "table_name": "ethnicity_config",
    "row_names": [
        "African",
        "Any other Asian background",
        "Any other Black background",
        "Any other Ethnic group",
        "Any other Mixed background",
        "Any other White background",
        "Arab",
        "Bangladeshi",
        "British",
        "Caribbean",
        "Central and Eastern European",
        "Chinese",
        "Gypsy/Roma/Traveller",
        "Indian",
        "Irish",
        "Latin America",
        "Not known",
        "Not stated",
        "Pakistani",
        "White and Asian",
        "White and Black African",
        "White and Black Caribbean",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "African": "MUMUP_URL",
        "Any other Asian background": "MUMUP_URL",
        "Any other Black background": "MUMUP_URL",
        "Any other Ethnic group": "MUMUP_URL",
        "Any other Mixed background": "MUMUP_URL",
        "Any other White background": "MUMUP_URL",
        "Arab": "MUMUP_URL",
        "Bangladeshi": "MUMUP_URL",
        "British": "MUMUP_URL",
        "Caribbean": "MUMUP_URL",
        "Central and Eastern European": "MUMUP_URL",
        "Chinese": "MUMUP_URL",
        "Gypsy/Roma/Traveller": "MUMUP_URL",
        "Indian": "MUMUP_URL",
        "Irish": "MUMUP_URL",
        "Latin America": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Not stated": "MUMUP_URL",
        "Pakistani": "MUMUP_URL",
        "White and Asian": "MUMUP_URL",
        "White and Black African": "MUMUP_URL",
        "White and Black Caribbean": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
        },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

disability_config = {
    "table_name": "disability_config",
    "row_names": [
        "Autism or other Neurological condition",
        "Behaviour and Emotional",
        "Hearing",
        "Manual Dexterity",
        "Memory or ability to concentrate, learn or understand (Learning Disability)",
        "Mobility and Gross Motor",
        "No disability",
        "Not Known",
        "Not stated (Person asked but declined to provide a response)",
        "Other",
        "Perception of Physical Danger",
        "Personal, Self-Care and Continence",
        "Progressive Conditions and Physical Health (such as HIV, Cancer, Multiple Sclerosis, Fits)",
        "Sight",
        "Speech",
        "Yes",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Autism or other Neurological condition": "MUMUP_URL",
        "Behaviour and Emotional": "MUMUP_URL",
        "Hearing": "MUMUP_URL",
        "Manual Dexterity": "MUMUP_URL",
        "Memory or ability to concentrate, learn or understand (Learning Disability)": "MUMUP_URL",
        "Mobility and Gross Motor": "MUMUP_URL",
        "No disability": "MUMUP_URL",
        "Not Known": "MUMUP_URL",
        "Not stated (Person asked but declined to provide a response)": "MUMUP_URL",
        "Other": "MUMUP_URL",
        "Perception of Physical Danger": "MUMUP_URL",
        "Personal, Self-Care and Continence": "MUMUP_URL",
        "Progressive Conditions and Physical Health (such as HIV, Cancer, Multiple Sclerosis, Fits)": "MUMUP_URL",
        "Sight": "MUMUP_URL",
        "Speech": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
        },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

sexual_orientation_config = {
    "table_name": "sexual_orientation_config",
    "row_names": [
        "Asexual",
        "Bisexual",
        "Gay",
        "Heterosexual or Straight",
        "Lesbian",
        "Not asked/Unknown",
        "Not stated (Person asked but declined to provide a response)",
        "Other",
        "Person asked and did not know/is unsure or undecided",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Asexual": "MUMUP_URL",
        "Bisexual": "MUMUP_URL",
        "Gay": "MUMUP_URL",
        "Heterosexual or Straight": "MUMUP_URL",
        "Lesbian": "MUMUP_URL",
        "Not asked/Unknown": "MUMUP_URL",
        "Not stated (Person asked but declined to provide a response)": "MUMUP_URL",
        "Other": "MUMUP_URL",
        "Person asked and did not know/is unsure or undecided": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
        },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

asylum_seeker_refugee_status_config = {
    "table_name": "asylum_seeker_refugee_status_config",
    "row_names": [
        "Asylum seeker / Refugee Status",
        "Yes",
        "No",
        "Not known",
        "Blank (nothing selected )"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Asylum seeker / Refugee Status": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Blank (nothing selected )": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

special_educational_needs_config = {
    "table_name": "special_educational_needs_config",
    "row_names": [
        "Special Educational Needs",
        "No",
        "Not known",
        "Yes",
        "Not applicable",
        "Blank (nothing selected )"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Special Educational Needs": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "Not applicable": "MUMUP_URL",
        "Blank (nothing selected )": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

education_health_care_plan_config = {
    "table_name": "education_health_care_plan_config",
    "row_names": [
        "Education, Health and Care plan",
        "Yes",
        "No",
        "Not known",
        "Not applicable",
        "Blank (nothing selected )"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Education, Health and Care plan": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Not applicable": "MUMUP_URL",
        "Blank (nothing selected )": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

at_risk_of_exploitation_config = {
    "table_name": "at_risk_of_exploitation_config",
    "row_names": [
        "At risk of Exploitation",
        "Yes",
        "No",
        "Not known",
        "Blank (nothing selected )"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "At risk of Exploitation": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Blank (nothing selected )": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}


leaving_care_config = {
    "table_name": "leaving_care_config",
    "row_names": [
        "Leaving Care",
        "Yes",
        "No",
        "Not Known",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Leaving Care": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not Known": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

looked_after_child_config = {
    "table_name": "looked_after_child_config",
    "row_names": [
        "Looked after child",
        "Yes",
        "No",
        "Not known",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Looked after child": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}


child_protection_plan_config = {
    "table_name": "child_protection_plan_config",
    "row_names": [
        "Child Protection Plan",
        "No",
        "Has never been subject to a plan",
        "Not known",
        "Has been previously subject to a plan",
        "Is currently subject to a plan",
        "Under assessment",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Child Protection Plan": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Has never been subject to a plan": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Has been previously subject to a plan": "MUMUP_URL",
        "Is currently subject to a plan": "MUMUP_URL",
        "Under assessment": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

child_in_need_plan_config = {
    "table_name": "child_in_need_plan_config",
    "row_names": [
        "Child in Need Plan",
        "Is currently subject to a Child in need plan",
        "No",
        "Has never been subject to a Child in need plan",
        "Not known",
        "Has previously been subject to a Child in need plan",
        "Under assessment",
        "Blank (nothing selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Child in Need Plan": "MUMUP_URL",
        "Is currently subject to a Child in need plan": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Has never been subject to a Child in need plan": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Has previously been subject to a Child in need plan": "MUMUP_URL",
        "Under assessment": "MUMUP_URL",
        "Blank (nothing selected)": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}

young_carer_config = {
    "table_name": "young_carer_config",
    "row_names": [
        "Young Carer",
        "Yes",
        "No",
        "Not known",
        "Not stated",
        "Blank (nothing Selected)"
    ],
    "column_headings": [
        "Q1_Totals",  
        "Barnardos (Wrap)",
        "BYS All",
        "Brathay Magic",
        "INCIC (CYP)",
        "MIB Know Your Mind",
        "MIB Know Your Mind +",
        "MIB Hospital Buddys Airedale General",
        "MIB Hospital Buddys BRI",
        "SELFA (Mighty Minds)",
    ],
    "placeholder_rows": {
        "Young Carer": "MUMUP_URL",
        "Yes": "MUMUP_URL",
        "No": "MUMUP_URL",
        "Not known": "MUMUP_URL",
        "Not stated": "MUMUP_URL",
        "Blank (nothing Selected)": "MUMUP_URL"
    },
    "row_db_logic": {},
    "mib_row_db_logic": {},
    'mib_row_db_default': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default': 'Contacts_Or_Indirects_Within_Reporting_Period',
}


table_configs = [
    service_info_config,
    yp_gender_config,
    yp_ethnicity_config,
    yp_disabilty_config,
    yp_sexual_orientation_config,
    yp_age_config,
    yp_area_config,
    yp_asylum_status_config,
    yp_special_ed_needs_config,
    yp_ed_health_care_plan_config,
    yp_at_risk_exploitation_config,
    yp_leaving_care_config,
    yp_looked_after_child_config,
    yp_child_protection_plan_config,
    yp_child_in_need_plan_config,
    yp_young_carer_config,
    total_attended_contacts_config,
    goals_based_outcomes_config,
    average_goals_based_outcomes_config,
    goal_themes_goals_based_outcomes_config,
    dss_goals_based_outcomes_config,
    contacts_by_theme_config,
    source_of_referral_config,
    reason_for_referral_config,
    other_reason_for_referral_config,
    gender_config,
    ethnicity_config,
    disability_config,
    sexual_orientation_config,
    asylum_seeker_refugee_status_config,
    special_educational_needs_config,
    education_health_care_plan_config,
    at_risk_of_exploitation_config,
    leaving_care_config,
    looked_after_child_config,
    child_protection_plan_config,
    child_in_need_plan_config,
    young_carer_config,
]
