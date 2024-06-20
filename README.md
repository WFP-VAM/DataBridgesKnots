# Data Bridges Connect

This Python module allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). It is a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

## Installation

> NB This is the dev version of the data_bridges_utils and API client package, it is frequently updated yet not stable.

You can install the `data_bridges_utils` package using `pip` and the Git repository URL:

```
pip install --force-reinstall git+https://github.com/WFP-VAM/DataBridgesConnect.git@dev
```

## Configuration
1. Create a ```data_bridges_api_config.yaml``` in the main folder you're running your core from.
2. The structure of the file is: 
    ```
    NAME: ''
    VERSION : ''
    KEY: ''
    SECRET: ''
    SCOPES:
    - ''
    - ''
    ```
1. Replace your_api_key and your_api_secret with your actual API key and secret from the Data Bridges API. Update the SCOPES list with the required scopes for your use case.
2. (For WFP users) Credentials and scopes for DataBridges API can be requested by opening a ticket with the [TEC Digital Core team](https://dev.azure.com/worldfoodprogramme/Digital%20Core/_workitems). See [documentation](https://docs.api.wfp.org/consumers/index.html#application-accounts)
3. External users can reach out to [wfp.vaminfo@wfp.org](mailto:wfp.vaminfo@wfp.org) for support on getting the API credentials.

### Python
Run the following code to extract household survey data. 

```python
from data_bridges_utils import DataBridgesShapes

CONFIG_PATH = "data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# Get household data for survey id
survey_data = client.get_household_survey(survey_id=3329, access_type='full')
print(survey_data.head())
```
A sample python file with additional examples for other endpoints is provided in the repo. 

### STATA
1. Make sure you declare where your Python instance is by setting ```python set exec "path/to/python/env"```
2. Run the following code to extract household survey data and loading it into STATA as a flat dataset with value labels. Make sure to edit your ```stata_path```and ```stata_version``` to match the one installed in your system.

```stata
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
stata_path = r"C:/Program Files/Stata18"
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

# Load into STATA dataframe
ds = load_stata(survey_data_with_value_labels, stata_path, stata_version)

end
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.
