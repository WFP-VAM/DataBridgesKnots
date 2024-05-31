# Data Bridges Utils

This Python module provides utilities for working with the WFP Data Bridges API. It allows you to fetch various datasets from the API, including household survey data, GORP (Global Operational Response Plan) data, market prices, exchange rates, and food security data (IPC equivalent).

## Installation

1. Clone the repository: 
```git clone https://github.com/your_org/data_bridges_utils.git```

2. Install the required dependencies:
```pip install -r requirements.txt
```

## Usage

Here's an example of how to use the `DataBridgesShapes` class from the `data_bridges_utils` module:

```python
from data_bridges_utils import DataBridgesShapes

CONFIG_PATH = "data_bridges_api_config.yaml"

client = DataBridgesShapes(CONFIG_PATH)

# Get household data for survey id
survey_data = client.get_household_survey(survey_id=3329, access_type='full')
print(survey_data.head())

# Get GORP data
latest_data = client.get_gorp('latest')
print(latest_data)

# Get market data
exchange_rates = client.get_exchange_rates('AFG')
print(exchange_rates.head())

prices = client.get_prices('AFG', '2022-01-01')
print(prices.head())

# Get IPC equivalent food security data
food_security = client.get_food_security()
print(food_security.head())

afg_food_security = client.get_food_security("AFG", 2024)
print(afg_food_security.head())
```

Make sure to replace data_bridges_api_config.yaml with the path to your API configuration file containing your API key, secret, and other settings.

## Configuration
The ```data_bridges_api_config.yaml``` file should have the following structure:

```yaml
KEY: your_api_key
SECRET: your_api_secret
SCOPES:
  - scope1
  - scope2
VERSION: v1
```

Replace your_api_key and your_api_secret with your actual API key and secret from the Data Bridges API. Update the SCOPES list with the required scopes for your use case.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the AGPL 3.0 License.