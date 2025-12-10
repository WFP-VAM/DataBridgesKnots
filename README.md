# Data Bridges Knots

This Python module allows you to get data from the WFP Data Bridges API, including household survey data, market prices, exchange rates, GORP (Global Operational Response Plan) data, and food security data (IPC equivalent). It is a wrapper for the [Data Bridges API Client](https://github.com/WFP-VAM/DataBridgesAPI), providing an easier way to data analysts to get VAM and monitoring data using their language of choice (Python, R and STATA).

## Getting started
User guide on the package can be found [here](https://wfp-vam.github.io/DataBridgesKnots/reference/)

## Installation

### Using uv
>  :point_right: We recommend using `uv` as package manager. You can install it using the [instructions here](https://docs.astral.sh/uv/getting-started/installation/). 

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

R users need to have `reticulate` installed in their machine to run this package as explained in the [R example file](examples/example_R.R)

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

## Examples
### Python

Run the following example to extract commodity data: 
```python

from data_bridges_knots import DataBridgesShapes

CONFIG_PATH = r"data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# COMMODITY DATA
commodity_units_list = client.get_commodity_units_list(country_code="TZA", commodity_unit_name="Kg", page=1, format='json')

```
Additional examples are in the [examples](https://github.com/WFP-VAM/DataBridgesKnots/tree/main/examples) folder and in the [API Reference document](https://wfp-vam.github.io/DataBridgesKnots/reference/)


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
  country_iso3 = "TZA",
  commodity_unit_name = "Kg",
  page = 1L,
  format = "json"
)
```

Additional examples are in the [examples](https://github.com/WFP-VAM/DataBridgesKnots/tree/main/examples) folder.

## Developer set-up

### Installing required tools

This project uses `uv` to manage dependencies and environments. See [here](https://docs.astral.sh/uv/getting-started/installation/) for installation, and [here](https://docs.astral.sh/uv/guides/projects/) for basic use.
`uv` uses information on dependencies in the `pyproject.toml` file and continuously maintains a detailed description of the required environment in the `uv.lock` file.

This project uses `make` to automate common project management tasks. For installation see: [Windows](https://leangaurav.medium.com/how-to-setup-install-gnu-make-on-windows-324480f1da69), [Ubuntu Linux](https://linuxhint.com/install-make-ubuntu/), [OSX](https://formulae.brew.sh/formula/make)

### Virtual environment
To set up the environment for the first time (including all dev tools like black, isort, ruff, mypy, pytest, mkdocs, etc.), run:

```commandline
$ make install
```

This will install the package with all dependencies and dev tools defined in `pyproject.toml`.

To run any script or command inside the environment, run:

```commandline
$ uv run my_script.py
```
See [here](https://docs.astral.sh/uv/guides/projects/) for further information on using `uv`.

### Code formatting and linting

Run checks

```commandline
$ make check-codestyle
```

Apply fixes

```commandline
$ make codestyle
```

### Commits

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for conventional commits. To create a properly formatted commit:

```commandline
$ uv run cz commit
```

This interactive tool guides you through creating commits that follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.

