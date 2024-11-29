from data_bridges_knots import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

#%% COMMODITY DATA
# Get commodity unit list for a country
commodity_units_list = client.get_commodity_units_list(country_code="TZA", commodity_unit_name="Kg", page=1, format='json')

# Get commodity unit conversion list for a country
comodity_unit_conversion_list = client.get_commodity_units_conversion_list(country_code="TZA", commodity_id=1, from_unit_id=1, to_unit_id=2, page=1, format='json')

#%% CURRENCTY DATA
# Get currency list
currency_list = client.get_currency_list(country_code="TZA", currency_name="TZS", currency_id=0, page=1, format='json')

# Get USD indirect quotation for a country
usd_indirect_quotation = client.get_usd_indirect_quotation(country_iso3="TZA", currency_name="TZS", page=1, format='json')

#%% MARKETS DATA
# Get a complete list of markets in a country
markets_list = client.get_markets_list(country_code="TZA")

# Get a complete list of markets in a country
markets_csv = client.get_markets_as_csv(adm0code=4, local_names=False) 

# Get markets near a given location by longitude and latitude within a 15Km distance 
nearby_markets = client.get_nearby_markets(adm0code=56)

#%% MARKET FUNCTIONALITY INDEX
# Get the MFI surveys for a given country
get_mfi_surveys = client.get_mfi_surveys(adm0_code=1)

# Get the MFI functionality index for a given country (standardized data)
get_mfi_surveys_base_data = client.get_mfi_surveys_base_data(survey_id=3673)

# Get the MFI functionality index for a given country (full data)
get_mfi_surveys_full_data = client.get_mfi_surveys_full_data(survey_id=3673)

# Get the MFI functionality index for a given country (processed data)
get_mfi_surveys_processed_data = client.get_mfi_surveys_processed_data(survey_id=3673) 

# Get MFI XLSForm information
mfi_xls_forms = client.get_mfi_xls_forms(page=1, start_date='2023-01-01', end_date='2023-12-31')

xls_forms = client.get_mfi_xls_forms_detailed(
    adm0_code=0,
    page=1, 
    start_date='2023-01-01',
    end_date='2023-12-31'
)



#%% FOOD SECURITY DATA 
# Get IPC and equivalent food insecurity numbers for all countries
get_food_security_list = client.get_food_security_list()

#%% GLOBAL OPERATION RESPONSE PLAN (GOPR)
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

#%% HOUSEHOLD ASSESSMENT & MONITORING DATA
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