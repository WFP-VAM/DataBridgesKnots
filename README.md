# Data Bridges Knots

This Python module allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). It is a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

## Installation

> NB This is the development version of the data_bridges_knots and API client package, it is frequently updated yet not stable.

You can install the `data_bridges_knots` package using `pip` and the Git repository URL:

```
pip install --force-reinstall git+https://github.com/WFP-VAM/DataBridgesKnots.git@dev
```

STATA and R users will also need the appropriate optional dependencies to use this package in their respective software. To install the package with these dependencies, use the following command:

***STATA users***
```
pip install git+https://github.com/WFP-VAM/DataBridgesKnots.git#egg=data_bridges_knots[STATA]
```

***R users***
```
pip install git+https://github.com/WFP-VAM/DataBridgesusKnots.git#egg=data_bridges_knots[R]
```

## Configuration
1. Create a ```data_bridges_api_config.yaml``` in the main folder you're running your core from.
2. The structure of the file is: 
    ```yaml
    NAME: ''
    VERSION : ''
    KEY: ''
    SECRET: ''
    DATA_BRIDGES_API_KEY = ''
    SCOPES:
    - ''
    - ''
    ```
1. Replace your_api_key and your_api_secret with your actual API key and secret from the Data Bridges API. Update the SCOPES list with the required scopes for your use case.
2. (For WFP users) Credentials and scopes for DataBridges API can be requested by opening a ticket with the [TEC Digital Core team](https://dev.azure.com/worldfoodprogramme/Digital%20Core/_workitems). See [documentation](https://docs.api.wfp.org/consumers/index.html#application-accounts)
3. External users can reach out to [wfp.vaminfo@wfp.org](mailto:wfp.vaminfo@wfp.org) for support on getting the API credentials.

### Python
Run the following code to extract commoditiy data. 

```python

from data_bridges_knots import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# COMMODITY DATA
commodity_units_list = client.get_commodity_units_list(country_code="TZA", commodity_unit_name="Kg", page=1, format='json')

```
Additional examples are in the [examples](https://github.com/WFP-VAM/DataBridgesKnots/tree/main/examples) folder.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.
