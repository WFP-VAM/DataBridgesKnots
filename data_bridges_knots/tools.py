
def discover_surveys():
    """Port of the discover_survey.r in JOR automation"""


    print("========================================\n")
    print("DATABRIDGES SURVEY DISCOVERY\n")
    print("========================================\n\n")

    # Step 1: List all available surveys
    print("========================================\n")
    print("STEP 1: LIST AVAILABLE SURVEYS\n")
    print("========================================\n")
    print("Fetching household surveys...\n\n")

    # Step 2: Search function
    print("========================================\n")
    print("STEP 2: SEARCH FOR YOUR SURVEY\n")
    print("========================================\n\n")

    # Step 3: Inspect a specific survey
    print("========================================\n")
    print("STEP 3: INSPECT A SPECIFIC SURVEY\n")
    print("========================================\n")
    print("Once you have a survey ID, inspect its data structure:\n\n")

    # Step 4: Interactive exploration
    print("========================================\n")
    print("STEP 4: INTERACTIVE EXPLORATION\n")
    print("========================================\n\n")

    print("Available data:\n")
    print("  available_surveys           # All surveys (if loaded)\n")
    print("  current_survey_data         # Currently inspected survey data\n\n")

    print("Available functions:\n")
    print("  search_surveys('keyword')   # Search for surveys by name\n")
    print("  inspect_survey(susvey_id)   # Load and inspect a survey\n\n")

    print("Example workflow:\n")
    print("  1. search_surveys('BCM')                   # Find BCM surveys\n")
    print("  2. inspect_survey(5387)                    # Inspect a specific survey\n")
    print("  3. View(current_survey_data)               # Open in viewer\n")
    print("  4. names(current_survey_data)              # See all columns\n")
    print("  5. table(current_survey_data$column_name)  # Analyze a column\n\n")

    print("Exploration commands:\n")
    print("  View(current_survey_data)              # Open in viewer\n")
    print("  names(current_survey_data)             # All column names\n")
    print("  unique(current_survey_data$COLUMN)     # Unique values\n")
    print("  table(current_survey_data$COLUMN)      # Count by printegory\n")
    print("  str(current_survey_data)               # Data structure\n")
    print("  summary(current_survey_data)           # Summary statistics\n\n")

    print("========================================\n")
    print("READY FOR DISCOVERY!\n")
    print("========================================\n")
    print("Complete workflow:\n")
    print("  1. Browse available surveys above (Step 1)\n")
    print("  2. Search for your survey (Step 2)\n")
    print("  3. Inspect the survey structure (Step 3)\n")
    print("  4. Explore the data (Step 4)\n")
    print("  5. Create your exercise file using the information gathered\n\n")
