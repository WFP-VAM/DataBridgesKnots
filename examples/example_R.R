# Load required packages
library(reticulate)
library(dplyr)

# Set up Python environment
# use_python("/path/to/python/env")
python_path <- "C:/Users/alessandra.gherardel/AppData/Local/miniconda3/envs/data_bridges_knots/python.exe"
use_python(path.expand(python_path))

# Import DataBridgesShapes class
databridges_knots <- import("data_bridges_knots")
DataBridgesShapes <- databridges_knots$DataBridgesShapes

# Initialize DataBridges client with credentials from YAML file
CONFIG_PATH <- "data_bridges_api_config.yaml"
client <- DataBridgesShapes(CONFIG_PATH)

# Get household data for survey id
survey_data <- client$get_household_survey(survey_id=3329, access_type='full')
survey_data_r <- py_to_r(survey_data)
print(head(survey_data_r))

