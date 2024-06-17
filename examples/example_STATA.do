python set exect "path/to/python/env"

python:

"""
Read a 'base' Household dataset  from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""

from data_bridges_utils import DataBridgesShapes, map_value_labels
from data_bridges_utils.load_stata import load_stata
import stata_setup

# set installation path for STATA
stata_path = "C:/Program Files/Stata18"
# set stata version
stata_version = "se" 

stata_setup.config(stata_path, stata_version)
from sfi import Data, Macro,  SFIToolkit, Frame, Datetime as dt

# Path to YAML file containing Data Bridges API credentials
CONFIG_PATH = r"data_bridges_api_config.yaml"

# Example dataset and questionnaire from 2023 Congo CFSVA
CONGO_CFSVA = {
    'questionnaire': 1509,
    'dataset': 3094
}

# Initialize DataBridges client with credentials from YAML file
client = DataBridgesShapes(CONFIG_PATH)

# Get houhold data for survey id
survey_data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='base') # base is the standardized-only dataset
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Map the categories to survey_data
mapped_survey_data = map_value_labels(survey_data, questionnaire)

# Get variable labels
variable_labels = get_column_labels(questionnaire)
# Get value labels
value_labels = get_value_labels(questionnaire)

# Return flat dataset with value labels
survey_data_with_value_labels = map_value_labels(survey_data, questionnaire)

# Export dataset, questionnaire (with variable labels) and choice list in CSV
survey_data.to_csv(f"congo_cfsva_survey_data.csv", index=False)
questionnaire.to_csv(f"congo_cfsva_questionnaire.csv", index=False)	
choices.to_csv(f"congo_csfsva_choice_list.csv", index=False)
# mapped.to_csv(f"congo_cfsva_mapped.csv", index=False)
print("Exported survey data, questionnaire and choice list")

# Load into STATA dataframe
ds = load_stata(survey_data_with_value_labels)

end