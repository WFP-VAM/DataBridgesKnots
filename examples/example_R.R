# First, install reticulate if not already installed
install.packages("reticulate")
library(reticulate)

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

