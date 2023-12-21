file_info = {
    "Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "contacts_or_indirects_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "MIB_Contacts_Or_Indirects_Within_Reporting_Period": {
        "filename": "mib_contacts_or_indirects_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "MIB_Contacts_Within_Twenty_One_Days": {
        "filename": "mib_contacts_within_twenty_one_days.csv",
        "columns": ['client_id']
    },
    "Attended_Contacts_Within_Twenty_One_Days": {
        "filename": "attended_contacts_within_twenty_one_days.csv",
        "columns": ['client_id']
    },
    "Contacts_After_Referrals": {
        "filename": "contacts_after_referrals.csv",
        "columns": ['client_id']
    },
    "Contacts_Within_Twenty_One_Days": {
        "filename": "contacts_within_twenty_one_days.csv",
        "columns": ['client_id']
    },
    "File_Closures_And_Goals_Within_Reporting_Period": {
        "filename": "file_closures_and_goals_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "File_Closures_Within_Reporting_Period": {
        "filename": "file_closures_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "Initial_Goals_Within_Reporting_Period": {
        "filename": "initial_goals_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "MIB_Attended_Contacts_Within_Twenty_One_Days": {
        "filename": "mib_attended_contacts_within_twenty_one_days.csv",
        "columns": ['client_id']
    },
    "MIB_Contacts_After_Referrals": {
        "filename": "mib_contacts_after_referrals.csv",
        "columns": ['client_id']
    },
    "Referrals_Within_Reporting_Period": {
        "filename": "referrals_within_reporting_period.csv",
        "columns": ['client_id']
    },
    "MIB_Referrals_Within_Reporting_Period": {
        "filename": "mib_referrals_within_reporting_period.csv",
        "columns": ['client_id']
    },
    # Add more file information as needed
}


YiM_Providers = [
    "Barnardos",
    "Bradford Youth Service (BYS)",
    "Brathay -MAGIC service type only",
    "INCIC -service type CYP only",
    "Mind in Bradford (MiB) service type Know Your Mind, Know Your Mind plus, Hospital Buddies BRI and Hospital Buddies  AGH only",
    "SELFA"
]

Other_VCSE = [
    "All Star Youth Entertainment",
    "Bradford Counselling Service",
    "Bradford Bereavement Support",
    "Family Action Bradford",
    "Roshnighar",
    "STEP 2",
    "The Cellar Trust"
]


service_info_config = {
    'row_names': [
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
    'column_headings': [
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
    'placeholder_rows': {
        "Number of unique people supported (old rule)": "MYMUP_URL",
        "How many unique referrals": "MYMUP_URL",
        "How many new people referred": "MYMUP_URL",
        "% clients with initial contact within 7 days of referral (old rule not including admin contacts)": "MYMUP_URL",
        "% clients who had the first support session offered within 21 days of referral": "MYMUP_URL",
        "% clients attended the first contact by video/face to face/telephone within 21 days of referral": "MYMUP_URL",
    },
    'key_logic': {
        "Number of unique people supported": "MIB_Contacts_Or_Indirects_Within_Reporting_Period",
        "How many young people disengaged, couldn’t be contacted or rejected a referral?": "File_Closures_Within_Reporting_Period",
        "How many were declined by the service?": "File_Closures_Within_Reporting_Period",
        "How many people have moved on": "File_Closures_Within_Reporting_Period",
        "Active cases": "Referrals_Within_Reporting_Period",
    },
    'filter_function': SI_row_filter,  # Assuming SI_row_filter is your specific filter function
}