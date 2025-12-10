# Getting started with DataBridgesKnots

DataBridgesKnots is a Python module to allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). It is a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

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

R users need to have `reticulate` installed in their machine to run this package as explained in the [examples folder](https://github.com/WFP-VAM/DataBridgesKnots/tree/main/examples).

```R
install.packages("reticulate")
library(reticulate)
```

## Configuration

There are three ways to configure DataBridgesShapes:

### Option 1: YAML Configuration File (Recommended for Production)

1. Create a ```data_bridges_api_config.yaml``` in the main folder you're running your code from.
2. The structure of the file is:

    ```yaml
    NAME: ''
    VERSION : ''
    KEY: ''
    SECRET: ''
    DATABRIDGES_API_KEY: ''
    SCOPES:
    - ''
    - ''
    ```
3. Replace the placeholders with your actual API key and secret from the Data Bridges API. Update the SCOPES list with the required scopes for your use case.

### Option 2: Dictionary Configuration (Recommended for Testing/Programmatic Use)

You can also initialize the client directly with a Python dictionary:

```python
from data_bridges_knots import DataBridgesShapes

config = {
    'KEY': 'your-api-key',
    'SECRET': 'your-api-secret',
    'VERSION': '5.0.0',
    'SCOPES': [
        'vamdatabridges_household-fulldata_get',
        'vamdatabridges_marketprices-pricemonthly_get'
    ],
    'DATABRIDGES_API_KEY': 'optional-databridges-key'
}

client = DataBridgesShapes(config)
```

### Option 3: Environment Variables (Recommended for CI/CD and Containers)

Set the following environment variables and use the `config_from_env()` helper:

```bash
export DATABRIDGES_KEY="your-api-key"
export DATABRIDGES_SECRET="your-api-secret"
export DATABRIDGES_VERSION="5.0.0"
export DATABRIDGES_SCOPES="scope1,scope2,scope3"
export DATABRIDGES_API_KEY="optional-databridges-key"
```

Then in your Python code:

```python
from data_bridges_knots.client import config_from_env, DataBridgesShapes

config = config_from_env()
client = DataBridgesShapes(config)
```

### Getting Credentials

- **(For WFP users)** Credentials and scopes for DataBridges API can be requested by opening a ticket with the [TEC Digital Core team](https://dev.azure.com/worldfoodprogramme/Digital%20Core/_workitems). See [documentation](https://docs.api.wfp.org/consumers/index.html#application-accounts)
- **External users** can reach out to [wfp.vaminfo@wfp.org](mailto:wfp.vaminfo@wfp.org) for support on getting the API credentials.

## License
This project is licensed under the AGPL 3.0 License.
