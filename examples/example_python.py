"""
Reads Household Data from Data Bridges. The script uses the DataBridgesShapes class from the data_bridges_utils module to interact with the Data Bridges API and retrieve various datasets, including:
- Household survey data
- GORP (Global Operational Response Plan) data
- Exchange rates and prices for Afghanistan
- IPC and equivalent food security Data

The script demonstrates how to use the DataBridgesShapes class to fetch these datasets and print the first few rows of the resulting pandas DataFrames.
"""
#%%

from data_bridges_knots import DataBridgesShapes
from data_bridges_knots.load_stata import load_stata

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

#%% XSLForm definition and Household dataset

CONGO_CFSVA = {
    'questionnaire': 1509,
    'dataset': 3094
}
# get household survey data  
survey_data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='full')
# get XLSForm data
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Map the categories to survey_data
mapped_survey_data = map_value_labels(survey_data, questionnaire)


#%% GORP data 
# Get GORP data
latest_data = client.get_gorp('latest')
list_data = client.get_gorp('list') 
regional_latest_data = client.get_gorp('regional_latest')
global_latest_data = client.get_gorp('global_latest')
# #%

#%% Market data
exchage_rates = client.get_exchange_rates('AFG')
prices = client.get_prices('AFG', '2022-01-01')


#%% IPC equivalent 
food_security = client.get_food_security() 
afg_food_security = client.get_food_security("AFG", 2024)

