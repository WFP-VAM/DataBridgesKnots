from typing import Dict, Optional

import json
from pathlib import Path

# Cache return value from _load_country_codes() into global variable
codes_mapping = None


def _load_country_codes() -> Dict[str, int]:
    """Load country codes mapping from JSON file.

    Returns:
        Dict[str, int]: Mapping of ISO3 codes to ADM0 codes

    Examples:
        >>> codes = _load_country_codes()
        >>> isinstance(codes, dict)
        True
    """
    global codes_mapping
    if codes_mapping is None:
        try:
            json_path = Path(__file__).parent / "country_list.json"
            with open(json_path, "r", encoding="utf-8") as f:
                country_list = json.load(f)

            codes_mapping = {
                country["iso3Alpha3"]: country["adm0Code"]
                for country in country_list
                if country.get("adm0Code") is not None
                and country.get("iso3Alpha3") is not None
            }
        except FileNotFoundError:
            raise FileNotFoundError(f"Country list file not found at {json_path}")

    return codes_mapping


def get_adm0_code(country_iso3: str) -> Optional[int]:
    """Get ADM0 code for a given ISO3 country code.

    Args:
        iso3 (str): ISO3 country code (e.g. 'AFG' for Afghanistan)

    Returns:
        Optional[int]: ADM0 code if found, None if not found

    Examples:
        >>> code = get_code("ETH")  # Ethiopia
        >>> isinstance(code, int)
        True
        >>> get_code("XXX") is None  # Invalid code
        True
    """

    if not isinstance(country_iso3, str):
        raise TypeError("iso3 must be a string")

    codes = _load_country_codes()
    return codes.get(country_iso3.upper())


def discover_surveys():
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
    print("  inspect_survey(survey_id)   # Load and inspect a survey\n\n")

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
