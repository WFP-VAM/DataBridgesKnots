# First, install reticulate if not already installed
#install.packages("reticulate")
library(reticulate)

# Use the correct conda environment
use_condaenv("knots-3.11", required = TRUE)

# Import the Python module through reticulate
data_bridges_knots <- import("data_bridges_knots")

# Create client instance
config_path <- "data_bridges_api_config.yaml"
client <- data_bridges_knots$DataBridgesShapes(config_path)

# COMMODITY DATA
# Get commodity unit list for Tanzania
commodity_units <- client$get_commodity_units_list(
  country_code = "TZA",
  commodity_unit_name = "Kg",
  page = 1L,
  format = "json"
)

# CURRENCY DATA 
# Get Tanzania Shilling exchange rates
exchange_rates <- client$get_usd_indirect_quotation(
  country_iso3 = "TZA",
  currency_name = "TZS",
  page = 1L,
  format = "json"
)




# ── FOOD SECURITY DATA ──
# Get IPC and equivalent food insecurity numbers for all countries
food_security_list <- client$get_food_security_list()

# ── GLOBAL OPERATION RESPONSE PLAN (GOPR) ──
# Get country-level latest data
country_latest_df <- client$get_gorp("country_latest")  # no data currently uploaded

# Get global latest data
global_latest_df <- client$get_gorp("global_latest")

# Get regional latest data
regional_latest_df <- client$get_gorp("regional_latest")

# ── HOUSEHOLD ASSESSMENT & MONITORING DATA ──
# Get list of household surveys available
surveys_list <- client$get_household_surveys()

# Get survey data for a specific survey
survey_data <- client$get_household_survey(
  survey_id = 3094L,
  access_type = "official"
)

# Get XLSForm definition for a specific survey
xlsform <- client$get_household_xslform_definition(
  xls_form_id = 1509L
)

# Get survey questionnaire for a specific survey
questionnaire <- client$get_household_questionnaire(
  xls_form_id = 1509L
)

# Get choice list for a specific survey
choices <- client$get_choice_list(
  xls_form_id = 1509L
)


