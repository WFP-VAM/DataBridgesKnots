# Data Bridges Utils

This Python module provides utilities for working with the WFP Data Bridges API. It allows you to fetch various datasets from the API, including household survey data, GORP (Global Operational Response Plan) data, market prices, exchange rates, and food security data (IPC equivalent).

## Installation

You can install the `data_bridges_utils` package using `pip` and the Git repository URL:

```
pip install --force-reinstall git+https://github.com/WFP-VAM/DataBridgesUtils.git@dev
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


### Python

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
2. Run the following code to extract household survey data. Make suere to edit your ```stata_path```and ```stata_version``` to match the one installed in your system.

```stata
python:

"""
Read a 'full' Household dataset  from Data Bridges and load it into STATA.
Only works if user has STATA 18+ installed and added to PATH.
"""

from data_bridges_utils import DataBridgesShapes
from data_bridges_utils.labels import map_value_labels, get_stata_variable_labels
from data_bridges_utils.load_stata import load_stata
import stata_setup

stata_path = r"E:\Program Files\Stata18"
stata_version = "mp"

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
survey_data = client.get_household_survey(survey_id=CONGO_CFSVA["dataset"], access_type='full')
questionnaire = client.get_household_questionnaire(CONGO_CFSVA["questionnaire"])

# Map the categories to survey_data
mapped_survey_data = map_value_labels(survey_data, questionnaire)

# Load into STATA dataframe
ds1 = load_stata(mapped_survey_data, stata_path, stata_version)

var_label = get_stata_variable_labels(questionnaire)
ds2 = load_stata(survey_data, stata_path, stata_version, variable_labels=var_label)


end
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.