
DataBridgesKnots is a Python module that allows you to get data from the WFP Data Bridges API, including **household survey data**, **market prices**, **exchange rates**, and **Market Functionality Index surveys**.

It simplifies the official Data Bridges API Client, making it easier for analysts to work in:
- Python  
- R  
- STATA  

📖 **Full User Documentation:** https://wfp-vam.github.io/DataBridgesKnots/reference/


## Installation
We recommend using `uv` as package manager to run this project. See [here](https://docs.astral.sh/uv/getting-started/installation/) for installation, and [here](https://docs.astral.sh/uv/guides/projects/) for basic use.

You can install the `data-bridges-knots` by running this `uv` command:
```
uv pip install data-bridges-knots \
  --extra-index-url https://d2i4vvypvg40rv.cloudfront.net/pypi/ \
  --index-strategy unsafe-first-match
```

You can also install the `data_bridges_knots` package using regular `pip`:

```
pip install data-bridges-knots \
  --extra-index-url https://d2i4vvypvg40rv.cloudfront.net/pypi/
  --index-strategy unsafe-first-match
```

STATA and R users will also need the appropriate optional dependencies to use this package in their respective software. To install the package with these dependencies, use the following command:

### STATA users

STATA users need to install the `data_bridges_knots` with additional STATA dependencies (`pystata`, and `stata-setup`):

```
uv venv .venv && source .venv/bin/activate && uv pip install "data-bridges-knots[STATA]" \
  --extra-index-url https://d2i4vvypvg40rv.cloudfront.net/pypi/
```

### R users

R users need to have `reticulate` installed in their machine to run this package as explained in the [user documentation](https://wfp-vam.github.io/DataBridgesKnots/reference/)

```R
install.packages("reticulate")
library(reticulate)

```

### Project setup using uv
`uv` uses information on dependencies in the `pyproject.toml` file and continuously maintains a detailed description of the required environment in the `uv.lock` file.


You can set up a `uv` project by running in your project folder.
```
uv init
```

Then configure `pyproject.toml` as follows: 

```
[[tool.uv.index]]
url = "https://d2i4vvypvg40rv.cloudfront.net/pypi/"
name = "wfp-private"
explicit = true

[tool.uv.sources]
data-bridges-knots = { index = "wfp-private" }
data-bridges-client = { index = "wfp-private" }
```

and install the dependencies with 

```
uv sync
```

## Getting Credentials

### WFP users

- **For analysts**: If you are a data analyst/data scientist, we recommend using HIP Workshop as it already comes with batteries for data analysis, including this tool pre-installed. Reach out to [https://teams.microsoft.com/l/team/19%3A4ca595f7681f4ffa8a86b7af58832e8d%40thread.skype/conversations?groupId=cbd1e508-c6e8-459d-96b7-6cac3039c42c&tenantId=462ad9ae-d7d9-4206-b874-71b1e079776f](the DataBridges Community) for support.
- **For digital solutions**: If you are a tech lead or product manager for a digital solution, you can request your API Key and secret by opening a ticket with the [TEC Digital Core team](https://dev.azure.com/worldfoodprogramme/Digital%20Core/_workitems). See [documentation](https://docs.api.wfp.org/consumers/index.html#application-accounts)

### Partners and other external users

- External users can reach out to [wfp.vaminfo@wfp.org](mailto:wfp.vaminfo@wfp.org) for support on getting the API credentials.

## Configuration

There are three ways to configure DataBridgesKnots:

### Option 1: YAML Configuration File (Recommended for Production)

1. Create a ```data_bridges_api_config.yaml``` in the main folder you're running your code from.
2. The structure of the file is:

    ```yaml
    WFP_API_CLIENT_ID: 'your-api-key'
    WFP_API_CLIENT_SECRET: 'your-api-secret'
    DATABRIDGES_API_KEY: 'optional-databridges-key' # used for getting household survey full and internal data
    ```
3. Replace the placeholders with your actual credentials from the Data Bridges API portal.

### Option 2: Dictionary Configuration (Recommended for Testing/Programmatic Use)

You can also initialize the client directly with a Python dictionary:

```python
from data_bridges_knots import DataBridgesKnots

config = {
    'WFP_API_CLIENT_ID': 'your-api-key',
    'WFP_API_CLIENT_SECRET': 'your-api-secret',
    'DATABRIDGES_API_KEY': 'optional-databridges-key' # used for getting household survey full and internal data
}

client = DataBridgesKnots(config)
```

### Option 3: Environment Variables (Recommended for CI/CD and Containers)

Set the following environment variables and use the `config_from_env()` helper:

```bash
export WFP_API_CLIENT_ID="your-api-key"
export WFP_API_CLIENT_SECRET="your-api-secret"
export DATABRIDGES_API_KEY="optional-databridges-key" # used for getting household survey full and internal data
```

Then in your Python code:

```python
from data_bridges_knots.client import config_from_env, DataBridgesKnots

config = config_from_env()
client = DataBridgesKnots(config)
```