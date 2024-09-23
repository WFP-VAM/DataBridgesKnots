"""
Reads Household Data from Data Bridges. The script uses the DataBridgesShapes class from the data_bridges_knots module to interact with the Data Bridges API and retrieve various datasets, including:
- Household survey data
- GORP (Global Operational Response Plan) data
- Exchange rates and prices for Afghanistan
- IPC and equivalent food security Data

The script demonstrates how to use the DataBridgesShapes class to fetch these datasets and print the first few rows of the resulting pandas DataFrames.
"""

from data_bridges_knots import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# COMMODITY DATA
commodity_units_list = client.get_commodity_units_list(country_code="TZA", commodity_unit_name="Kg", page=1, format='json')
comodity_unit_conversion_list = client.get_commodity_units_conversion_list(country_code="TZA", commodity_id=1, from_unit_id=1, to_unit_id=2, page=1, format='json')

currency_list = client.get_currency_list(country_code="TZA", currency_name="TZS", currency_id=0, page=1, format='json')
usd_indirect_quotation = client.get_usd_indirect_quotation(country_iso3="TZA", currency_name="TZS", page=1, format='json')
print(commodity_units_list)

## MARKETS DATA
# Get a complete list of markets in a country
markets_list = client.get_markets_list(country_code="TZA")

# Get a complete list of markets in a country
markets_csv = client.get_markets_as_csv(adm0code=4, local_names=False) 

# Get markets near a given location by longitude and latitude within a 15Km distance 
nearby_markets = client.get_nearby_markets(adm0code=56)

### FOOD SECURITY DATA 
# Get IPC and equivalent food insecurity numbers for all countries
get_food_security_list = client.get_food_security_list()

### Global Operation Response Plan (GOPR)
# Get country-level latest data from the Global Operation Response Plan (GOPR) 
country_latest_df = client.get_gorp('country_latest') # no data currently uploaded

# Get global latest data from the Global Operation Response Plan (GOPR)
global_latest_df = client.get_gorp('global_latest')

# Get latest data (paginated) from the Global Operation Response Plan (GOPR)
latest_df = client.get_gorp('latest', page=1)

# Get full list data (paginated from the Global Operation Response Plan (GOPR)
list_df = client.get_gorp('list', page=1)

# Get regional latest data
regional_latest_df = client.get_gorp('regional_latest')

### HOUSEHOLD DATA
# Get list of household surveys available
surveys_list = client.get_household_surveys()

# Get survey data for a specific survey
survey_data = client.get_household_survey(survey_id=3094, access_type="official")

# Get XLSForm definition for a specific survey
xlsform = client.get_household_xslform_definition(xls_form_id=1509)

# Get survey questionnaire for a specific survey
questionnaire = client.get_household_questionnaire(xls_form_id=1509)

# Get choice list for a specific survey
choices = client.get_choice_list(xls_form_id=1509)


