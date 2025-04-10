python set exect "path/to/python/env"

python:

"""
Read a 'full' Household dataset  from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""

from data_bridges_knots import DataBridgesShapes
from data_bridges_knots.labels import get_column_labels, get_value_labels, map_value_labels
from data_bridges_knots.load_stata import load_stata
import numpy as np
import stata_setup
from sfi import Data, Macro,  SFIToolkit, Frame, Datetime as dt

stata_path = r"E:\Program Files\Stata18"
stata_version = "mp"

# Path to YAML file containing Data Bridges API credentials
CONFIG_PATH = r"data_bridges_api_config.yaml"

# Example dataset and questionnaire from 2023 Congo CFSVA
CONGO_CFSVA = {
    'questionnaire': 1509,
    'dataset': 3094
}

# Initialize DataBridges client with credentials from YAML file
client = DataBridgesShapes(CONFIG_PATH)

survey_data = client.get_household_survey(survey_id=CONGO_CFSVA['dataset'], access_type='full', page_size=800)
questionnaire = client.get_household_questionnaire(CONGO_CFSVA['questionnaire'])
choice_list = client.get_choice_list(CONGO_CFSVA['questionnaire'])


variable_labels = get_column_labels(questionnaire)
# get value labels
value_labels = get_value_labels(questionnaire)

survey_data_value_labels = map_value_labels(survey_data, questionnaire)
# mapped.replace({np.nan: None})

# # Export
survey_data.to_csv(f"congo_cfsva_survey_data.csv", index=False)
questionnaire.to_csv(f"congo_cfsva_questionnaire.csv", index=False)	
choice_list.to_csv(f"congo_csfsva_choice_list .csv", index=False)
survey_data_value_labels.to_csv(f"congo_cfsva_mapped.csv", index=False)

# Load into STATA dataframe
ds = load_stata(survey_data_value_labels, stata_path=stata_path, stata_version=stata_version, variable_labels=variable_labels, value_labels=value_labels)


end