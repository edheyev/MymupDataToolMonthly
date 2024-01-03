file_info = {
    "Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "contacts_or_indirects_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "MIB_Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "mib_contacts_or_indirects_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "MIB_Contacts_Within_Twenty_One_Days": {
        "filename": "mib_contacts_within_twenty_one_days.csv",
        "columns": ["client_id"],
    },
    "Attended_Contacts_Within_Twenty_One_Days": {
        "filename": "attended_contacts_within_twenty_one_days.csv",
        "columns": ["client_id"],
    },
    "Contacts_After_Referrals": {
        "filename": "contacts_after_referrals.csv",
        "columns": ["client_id"],
    },
    "Contacts_Within_Twenty_One_Days": {
        "filename": "contacts_within_twenty_one_days.csv",
        "columns": ["client_id"],
    },
    "File_Closures_And_Goals_Within_Reporting_Period": {
        "filename": "file_closures_and_goals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "MIB_File_Closures_And_Goals_Within_Reporting_Period": {
        "filename": "mib_file_closures_and_goals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "File_Closures_Within_Reporting_Period": {
        "filename": "file_closures_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "Initial_Goals_Within_Reporting_Period": {
        "filename": "initial_goals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "MIB_Attended_Contacts_Within_Twenty_One_Days": {
        "filename": "mib_attended_contacts_within_twenty_one_days.csv",
        "columns": ["client_id"],
    },
    "MIB_Contacts_After_Referrals": {
        "filename": "mib_contacts_after_referrals.csv",
        "columns": ["client_id"],
    },
    "Referrals_Within_Reporting_Period": {
        "filename": "referrals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    "MIB_Referrals_Within_Reporting_Period": {
        "filename": "mib_referrals_within_reporting_period.csv",
        "columns": ["client_id"],
    },
    # Add more file information as needed
}

yim_providers = [
    "Barnardos",
    "Bradford Youth Service (BYS)",
    "Brathay -MAGIC service type only",
    "INCIC -service type CYP only",
    "Mind in Bradford (MiB) service type Know Your Mind, Know Your Mind plus, Hospital Buddies BRI and Hospital Buddies  AGH only",
    "SELFA",
]

Other_VCSE = [
    "All Star Youth Entertainment",
    "Bradford Counselling Service",
    "Bradford Bereavement Support",
    "Family Action Bradford",
    "Roshnighar",
    "STEP 2",
    "The Cellar Trust",
]

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
        "How many unique referrals": "MYMUP_URL",
        "How many new people referred": "MYMUP_URL",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)": "MYMUP_URL",
        "% clients who had the first support session offered within 21 days of referral": "MYMUP_URL",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral": "MYMUP_URL",
    },
    "row_db_logic": {
        "Number of unique people supported": "Contacts_Or_Indirects_Within_Reporting_Period",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?": "File_Closures_Within_Reporting_Period",
        "How many were declined by the service?": "File_Closures_Within_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "Active cases": "Referrals_Within_Reporting_Period",
    },
    "mib_row_db_logic": {
        "Number of unique people supported": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?": "File_Closures_Within_Reporting_Period",
        "How many were declined by the service?": "File_Closures_Within_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "Active cases": "Referrals_Within_Reporting_Period",
    },
    'mib_row_db_default:': 'MIB_Contacts_Or_Indirects_Within_Reporting_Period',
    'row_db_default:': 'Contacts_Or_Indirects_Within_Reporting_Period',
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
        "Craven Ward  -Skipton North",
        "Craven Ward  -Skipton West",
        "Craven Ward -Settle Ribblebanks",
        "Craven Ward -Sutton in Craven",
        "Carven ward -Skipton South",
        "Craven Ward -Hellifield and Long Preston",
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
        "% of closed case that have an initial and follow up/final paired GBO",
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
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
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
    "placeholder_rows": {},
    "row_db_logic": {
        # Logic mappings for each status
    },
    "mib_row_db_logic": {
        # MIB-specific logic mappings for each status
    },
    'mib_row_db_default': 'File_Closures_And_Goals_Within_Reporting_Period',
    'row_db_default': 'File_Closures_And_Goals_Within_Reporting_Period',
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
    # Add more config tables as needed
]
