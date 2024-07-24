# Data Bridges Knots

This Python module allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). It is a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

## Installation

> NB This is the dev version of the data_bridges_knots and API client package, it is frequently updated yet not stable.

You can install the `data_bridges_knots` package using `pip` and the Git repository URL:

```
pip install git+https://github.com/WFP-VAM/DataBridgesKnots.git
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

from data_bridges_knots import DataBridgesShapes

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

# converts numeric columns into ints
numeric_columns = [ 'FCSDairy', 'FCSDairy_SRf', 'FCSFat', 'FCSFat_SRf', 'FCSFruit', 'FCSFruit_SRf', 'FCSNFruiOrg', 'FCSNPrEggs', 'FCSNPrFish', 'FCSNPrMeatF', 'FCSNPrMeatO', 'FCSNVegGre', 'FCSNVegOrg', 'FCSPr', 'FCSPr_SRf', 'FCSPulse', 'FCSPulse_SRf', 'FCSStap', 'FCSStap_SRf', 'FCSSugar', 'FCSSugar_SRf', 'FCSVeg', 'FCSVeg_SRf', 'HHSize', 'HHSize01F', 'HHSize01M', 'HHSize', 'HHSize01F', 'HHSize01M', 'HHSize1217F', 'HHSize1217M', 'HHSize1859F', 'HHSize1859M', 'HHSize24F', 'HHSize24M', 'HHSize511F', 'HHSize511M', 'HHSize60AboveF', 'HHSize60AboveM', 'RESPAge' ]
df = as_numeric(survey_data, numeric_columns)

```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.
