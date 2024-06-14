# Data Bridges Utils

This Python module provides utilities for working with the WFP Data Bridges API. It allows you to fetch various datasets from the API, including household survey data, GORP (Global Operational Response Plan) data, market prices, exchange rates, and food security data (IPC equivalent).

## Installation

You can install the `data_bridges_utils` package using `pip` and the Git repository URL:

```
pip install --force-reinstall git+https://github.com/WFP-VAM/DataBridgesUtils.git@dev
```

### STATA users

To use the `data_bridges_utils` package with STATA, you'll need to have STATA 18+ installed and added to your system's PATH. Additionally, you'll need to install the optional dependencies for STATA.

```pip install data-bridges-utils-STATA```

## Usage

### Python

```python
from data_bridges_utils import DataBridgesShapes

CONFIG_PATH = "data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# Get household data for survey id
survey_data = client.get_household_survey(survey_id=3329, access_type='full')
print(survey_data.head())

```
### STATA
```
from data_bridges_utils import DataBridgesShapes, load_stata

CONFIG_PATH = r"data_bridges_api_config.yaml"

# Initialize DataBridges client with credentials from YAML file
client = DataBridgesShapes(CONFIG_PATH)

# Get household data for survey id
survey_data = client.get_household_survey(survey_id=3329, access_type='full')

# Load into STATA dataframe
ds = load_stata(survey_data)
```

### R 
Instructions for using the data_bridges_utils package with R are coming soon.

Make sure to replace data_bridges_api_config.yaml with the path to your API configuration file containing your API key, secret, and other settings.

## Configuration
1. Rename the ```data_bridges_api_config_sample.yaml``` into ```data_bridges_api_config.yaml```. 
2. Replace your_api_key and your_api_secret with your actual API key and secret from the Data Bridges API. Update the SCOPES list with the required scopes for your use case.
3. (For WFP users) Credentials and scopes for DataBridges API can be requested by opening a ticket with the [TEC Digital Core team](https://dev.azure.com/worldfoodprogramme/Digital%20Core/_workitems). See [documentation](https://docs.api.wfp.org/consumers/index.html#application-accounts) 

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.