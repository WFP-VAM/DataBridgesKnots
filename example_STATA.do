python:

"""
Read a 'full' Household dataset  from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""

from data_bridges_utils import DataBridgesShapes, map_value_labels
from data_bridges_utils.load_stata import load_stata

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
survey_data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='full')
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Map the categories to survey_data
mapped_survey_data = map_value_labels(survey_data, questionnaire)

# Load into STATA dataframe
survey_data = load_stata(survey_data)

/* Data.setVarLabel(var, label)
# Set the variable label. The field "label" has to be str, "var" the name of an existing variable in the Stata Data object.

ValueLabel.createLabel('repair')
# Create a value label with a name (e.g.: 'repair'). This is only the empty dictionary that interprets the value of a specific variable.

ValueLabel.getNames()
# Gets the list of value labels available in Data.

ValueLabel.setLabelValue('repair', 1, 'One')
# Populates the dictionary of value labels

ValueLabel.getValueLabels('repair')
# Returns the list of value labels of a specific dictionary
# {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}

ValueLabel.setVarValueLabel('rep78', 'repair')
# associates the value labels dictionary (repair) to an existing variable (e.g.: rep78)

ValueLabel.getVarValueLabel('rep78')
# returns the value label (e.g.: repair) from an existing variable (e.g.: rep78) */


end