# Welcome to DataBridgesKnots

This Python package  allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). DataBridgesKnots a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

## Installation

### Using uv
>  We recommend using `uv` as package manager. You can install it using the [instructions here](https://docs.astral.sh/uv/getting-started/installation/). 

Install the `data_bridges_knots` package in your environment using uv:

```
uv venv .venv && source .venv/bin/activate && uv pip install git+https://github.com/WFP-VAM/DataBridgesKnots.git
```

### Using pip
You can also install the `data_bridges_knots` package using regular `pip` and the Git repository URL:

```
pip3 install --force-reinstall git+https://github.com/WFP-VAM/DataBridgesKnots.git
```

STATA and R users will also need the appropriate optional dependencies to use this package in their respective software. To install the package with these dependencies, use the following command:

### STATA users

STATA users need to install the `data_bridges_knots` with additional STATA dependencies (`pystata`, and `stata-setup`):

```
uv venv .venv && source .venv/bin/activate && uv pip install git+https://github.com/WFP-VAM/DataBridgesKnots.git#egg=data_bridges_knots[STATA]
```

### R users

R users need to have `reticulate` installed in their machine to run this package as explained in the [R example file](https://github.com/WFP-VAM/DataBridgesKnots/blob/main/examples/example_R.R)

```R
install.packages("reticulate")
library(reticulate)
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

### R 

```R
library(reticulate)

# Import the Python module through reticulate
data_bridges_knots <- import("data_bridges_knots")

# Point to our virtual environment's Python
use_python(".venv/bin/python")

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
```