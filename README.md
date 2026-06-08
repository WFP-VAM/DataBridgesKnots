# Data Bridges Knots

[![Python package](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/python-package.yml/badge.svg)](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/python-package.yml)

[![CodeQL](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/github-code-scanning/codeql)

[![pages-build-deployment](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/pages/pages-build-deployment)

[![Release Please](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/release-please.yml/badge.svg)](https://github.com/WFP-VAM/DataBridgesKnots/actions/workflows/release-please.yml)


This Python module allows you to get data from the WFP Data Bridges API, including **household survey data**, **market prices**, **exchange rates**, and **Market Functionality Index surveys**.

It simplifies the official Data Bridges API Client, making it easier for analysts to work in:
- Python  
- R  
- STATA  

📖 **Full documentation:** https://wfp-vam.github.io/DataBridgesKnots/reference/


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

R users need to have `reticulate` installed in their machine to run this package as explained in the [R example file](examples/example_R.R)

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

## Development version
If you're looking for a specific release/development version, you can install it by running this command, and adding the release number:

```
 uv pip install git+https://github.com/WFP-VAM/DataBridgesKnots/@release/vX.x.x
```


## Configuration

There are three ways to configure DataBridgesShapes:

### Option 1: YAML Configuration File (Recommended for Production)

1. Create a ```data_bridges_api_config.yaml``` in the main folder you're running your code from.
2. The structure of the file is:

    ```yaml
    WFP_API_CLIENT_ID: ''
    WFP_API_CLIENT_SECRET: ''
    DATABRIDGES_API_KEY: ''
    ```
3. Replace the placeholders with your actual credentials from the Data Bridges API portal.

### Option 2: Dictionary Configuration (Recommended for Testing/Programmatic Use)

You can also initialize the client directly with a Python dictionary:

```python
from data_bridges_knots import DataBridgesShapes

config = {
    'WFP_API_CLIENT_ID': 'your-api-key',
    'WFP_API_CLIENT_SECRET': 'your-api-secret',
    'DATABRIDGES_API_KEY': 'optional-databridges-key'
}

client = DataBridgesShapes(config)
```

### Option 3: Environment Variables (Recommended for CI/CD and Containers)

Set the following environment variables and use the `config_from_env()` helper:

```bash
export WFP_API_CLIENT_ID="your-api-key"
export WFP_API_CLIENT_SECRET="your-api-secret"
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
commodity_units_list = client.get_commodity_units_list(country_iso3="TZA", commodity_unit_name="Kg", page=1, format='json')

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

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Use [Commitizen](https://commitizen-tools.github.io/commitizen/) for an interactive prompt:

```commandline
$ uv run cz commit
```

Commit prefixes directly control versioning — choose carefully:

| Prefix | Example | Version bump |
|---|---|---|
| `fix:` | `fix: handle missing country code` | patch (`x.y.Z`) |
| `feat:` | `feat: add get_rpme_data endpoint` | minor (`x.Y.z`) |
| `feat!:` / `BREAKING CHANGE:` | `feat!: rename auth params` | major (`X.y.z`) |
| `chore:`, `docs:`, `ci:`, `refactor:`, `test:` | `chore: update dependencies` | no release |

### Release process

Releases are fully automated via [Release Please](https://github.com/googleapis/release-please-action):

1. Conventional commits land on `main` through normal PRs
2. Release Please automatically opens a **release PR** that bumps the version in `pyproject.toml` and updates `CHANGELOG.md`
3. A maintainer reviews and merges the release PR
4. The package is automatically built and published to the S3 PyPI index

To **manually trigger a publish** (e.g. to recover a failed release), go to **Actions → Release Please → Run workflow → main** in the GitHub UI.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.

