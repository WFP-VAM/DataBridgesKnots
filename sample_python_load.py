
"""
Read Household Data from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""
from data_bridges_utils import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

#%% Household data
# Get houhold data for survey id
survey_data = client.get_household_survey(survey_id=3329, access_type='full') # 3094 -> Congo
print(survey_data.head())
#%

#%% GORP data 
# Get GORP data
latest_data = client.get_gorp('latest')
print(latest_data)
list_data = client.get_gorp('list') 
print(list_data)
regional_latest_data = client.get_gorp('regional_latest')
print(regional_latest_data)
global_latest_data = client.get_gorp('global_latest')
print(global_latest_data)
# #%

#%% Market data
exchage_rates = client.get_exchange_rates('AFG')
print(exchage_rates.head())
prices = client.get_prices('AFG', '2022-01-01')
print(prices.head())


#%% IPC equivalent 
food_security = client.get_food_security() 
afg_food_security = client.get_food_security("AFG", 2024)
print(afg_food_security.head())


