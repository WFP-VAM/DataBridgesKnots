from typing import Dict, Union

import logging
import os
import warnings

import data_bridges_client
import yaml
from data_bridges_client.token import WfpApiToken

from data_bridges_knots.endpoints.commodityApi import (
    get_commodities_list,
    get_commodity_categories_list,
    get_commodity_units_conversion_list,
    get_commodity_units_list,
)
from data_bridges_knots.endpoints.currencyApi import (
    get_currency_list,
    get_exchange_rates,
    get_usd_indirect_quotation,
)
from data_bridges_knots.endpoints.economicDataApi import get_economic_indicator_list
from data_bridges_knots.endpoints.globalOutlookApi import get_global_outlook
from data_bridges_knots.endpoints.householdApi import (
    get_choice_list,
    get_household_questionnaire,
    get_household_survey,
    get_household_surveys_list,
    get_household_xlsform_definition,
)
from data_bridges_knots.endpoints.hungerHotpotApi import get_hunger_hotspot_data
from data_bridges_knots.endpoints.incubationApi import (
    get_cari_data,
)
from data_bridges_knots.endpoints.ipcChApi import (
    get_ipc_and_equivalent_data,
)
from data_bridges_knots.endpoints.marketPricesApi import get_prices
from data_bridges_knots.endpoints.marketsApi import (
    get_market_geojson_list,
    get_markets_as_csv,
    get_markets_list,
    get_nearby_markets,
)
from data_bridges_knots.endpoints.rpmeApi import (
    get_rpme_base_data,
    get_rpme_full_data,
    get_rpme_output_values,
    get_rpme_surveys,
    get_rpme_variables,
    get_rpme_xls_forms,
)
from data_bridges_knots.endpoints.surveysApi import (
    get_mfi_surveys,
    get_mfi_surveys_base_data,
    get_mfi_surveys_full_data,
    get_mfi_surveys_processed_data,
    get_mfi_xls_forms,
    get_mfi_xls_forms_detailed,
)

logname = "data_bridges_api_calls.log"
logging.basicConfig(
    filename=logname,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def config_from_env() -> Dict:
    """Construct DataBridges configuration dictionary from environment variables.

    Reads configuration from the following environment variables:
        - WFP_API_CLIENT_ID: WFP API Gateway key for authentication
        - WFP_API_CLIENT_SECRET: WFP API Gateway secret for authentication
        - DATABRIDGES_API_KEY: (Optional) DataBridges-specific API key for certain endpoints

    Returns:
        dict: Configuration dictionary with required keys for DataBridgesShapes

    Raises:
        ValueError: If any required environment variables are missing

    Examples:
        >>> import os
        >>> os.environ['WFP_API_CLIENT_ID'] = 'your_key'
        >>> os.environ['WFP_API_CLIENT_SECRET'] = 'your_secret'
        >>> config = config_from_env()
        >>> client = DataBridgesShapes(config)
    """

    required_vars = [
        "WFP_API_CLIENT_ID",
        "WFP_API_CLIENT_SECRET",
        "DATABRIDGES_VERSION",
    ]

    config = {}
    missing = []

    for env_var in required_vars:
        value = os.getenv(env_var)
        if value is None:
            missing.append(env_var)
        else:
            config[env_var] = value

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    databridges_api_key = os.getenv("DATABRIDGES_API_KEY")
    if databridges_api_key:
        config["DATABRIDGES_API_KEY"] = databridges_api_key

    return config


class DataBridgesKnots:
    """Interface to the Data Bridges API.

    Provides methods for fetching market prices, exchange rates, food security data,
    commodities, and more. Can be initialized from a YAML file, a dictionary, or
    environment variables.

    Args:
        config_path (str | dict): Either:
            - Path to a YAML configuration file (str), or
            - Configuration dictionary (e.g. .env) with required keys: WFP_API_CLIENT_ID,
              WFP_API_CLIENT_SECRET, and optionally DATABRIDGES_API_KEY
        env (str, optional): Environment to use ('prod' or 'dev'). Defaults to "prod".
        api_version (str, optional): Data Bridges API version to use. Defaults to "v1" (current version)


    Examples:
        >>> # Initialize with YAML file
        >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
        >>> df_prices = client.get_prices("KEN", "2025-09-01")

        >>> # Initialize with dictionary
        >>> config = {
        ...     'WFP_API_CLIENT_ID': 'your-client-id',
        ...     'WFP_API_CLIENT_SECRET': 'your-client-secret',
        ...     'DATABRIDGES_API_KEY': 'optional-databridges-key'
        ... }
        >>> client = DataBridgesKnots(config)

        >>> # Initialize from environment variables
        >>> from data_bridges_knots.client import config_from_env
        >>> client = DataBridgesKnots(config_from_env())
    """

    def __init__(self, config_path, env="prod", api_version="v1"):
        self.api_version = api_version
        self.env = env
        self.xlsform = None

        self.config = self._load_config(config_path)
        self._validate_config(self.config)
        self.configuration = self._setup_configuration_and_authentication(self.config)
        self.data_bridges_api_key = self.config.get("DATABRIDGES_API_KEY", "")

    def __repr__(self):
        return f"DataBridgesKnots(host='{self.configuration.host}', env='{self.env}'), api_version='{self.api_version}'"

    def __str__(self):
        return (
            f"DataBridgesKnots\n"
            f"  API Host: {self.configuration.host}\n"
            f"  Environment: {self.env}\n"
            f"\n"
            f"Brought to you with <3 by WFP VAM"
        )

    def _load_config(self, config: Union[str, Dict]) -> Dict:
        """Load configuration from YAML file or dictionary.

        Args:
            config (str | dict): Either a path to YAML file or a configuration dictionary

        Returns:
            dict: Configuration dictionary with required keys

        Raises:
            TypeError: If config is neither str nor dict
            FileNotFoundError: If YAML file path doesn't exist
            ValueError: If YAML file is invalid
        """

        if isinstance(config, str):
            # Load from YAML file
            with open(config, "r") as yamlfile:
                return yaml.load(yamlfile, Loader=yaml.FullLoader)
        elif isinstance(config, dict):
            # Use dict directly
            return config
        else:
            raise TypeError(
                f"config must be str (path to YAML file) or dict, got {type(config).__name__}"
            )

    def _validate_config(self, config: Dict) -> None:
        """Validate that configuration contains all required fields.

        Args:
            config (dict): Configuration dictionary to validate

        Raises:
            ValueError: If required fields are missing from configuration
        """
        required_fields = ["WFP_API_CLIENT_ID", "WFP_API_CLIENT_SECRET"]
        missing = [field for field in required_fields if field not in config]
        if missing:
            raise ValueError(
                f"Missing required configuration fields: {', '.join(missing)}"
            )

    def _setup_configuration_and_authentication(self, config: Dict):
        """Sets up authentication using configuration dictionary.

        Args:
            config (dict): Configuration dictionary containing authentication credentials

        Returns:
            Configuration: DataBridges configuration object

        """
        key = config["WFP_API_CLIENT_ID"]
        secret = config["WFP_API_CLIENT_SECRET"]
        BASE_URI = "https://gateway.api.wfp.org/vam-data-bridges"
        host = f"{BASE_URI}/{self.api_version.strip('/')}"
        print("host: ", host)

        logger.info("DataBridges API: %s", host)

        token = WfpApiToken(api_key=key, api_secret=secret)
        configuration = data_bridges_client.Configuration(
            host=host, access_token=token.refresh()
        )

        logger.debug("Token used: %s", token.__repr__())
        return configuration


class DataBridgesShapes(DataBridgesKnots):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            (
                "\n[FUTURE WARNING]"
                "DataBridgesShapes will be deprecated and be removed in v4.0.0 (July 2026).\n"
                "Use 'DataBridgesKnots' instead.\n"
            ),
            FutureWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"DataBridgesShapes(host='{self.configuration.host}', env='{self.env}'), api_version='{self.api_version}'"

    def __str__(self):
        return (
            f"DataBridgesShapes\n"
            f"  API Host: {self.configuration.host}\n"
            f"  Environment: {self.env}\n"
            f"\n"
            f"Brought to you with <3 by WFP VAM"
        )


# Binding endpoints to the DataBridgesKnots class
# Household Endpoints (IncubationApi)
DataBridgesKnots.get_household_survey = get_household_survey
DataBridgesKnots.get_household_surveys_list = get_household_surveys_list
DataBridgesKnots.get_household_xlsform_definition = get_household_xlsform_definition
DataBridgesKnots.get_household_questionnaire = get_household_questionnaire
DataBridgesKnots.get_choice_list = get_choice_list

# Currency Endpoints (CurrencyApi)
DataBridgesKnots.get_exchange_rates = get_exchange_rates
DataBridgesKnots.get_currency_list = get_currency_list
DataBridgesKnots.get_usd_indirect_quotation = get_usd_indirect_quotation

# Market Prices Endpoints (MarketPricesApi)
DataBridgesKnots.get_prices = get_prices

# Commodity Units Endpoints (CommodityUnitsApi)
DataBridgesKnots.get_commodities_list = get_commodities_list
DataBridgesKnots.get_commodity_units_conversion_list = (
    get_commodity_units_conversion_list
)
DataBridgesKnots.get_commodity_units_list = get_commodity_units_list
DataBridgesKnots.get_commodity_categories_list = get_commodity_categories_list

# Market Endpoints (MarketsApi)
DataBridgesKnots.get_market_geojson_list = get_market_geojson_list
DataBridgesKnots.get_markets_list = get_markets_list
DataBridgesKnots.get_markets_as_csv = get_markets_as_csv
DataBridgesKnots.get_nearby_markets = get_nearby_markets


# RPME Endpoints (RpmeApi)
DataBridgesKnots.get_rpme_base_data = get_rpme_base_data
DataBridgesKnots.get_rpme_full_data = get_rpme_full_data
DataBridgesKnots.get_rpme_output_values = get_rpme_output_values
DataBridgesKnots.get_rpme_surveys = get_rpme_surveys
DataBridgesKnots.get_rpme_variables = get_rpme_variables
DataBridgesKnots.get_rpme_xls_forms = get_rpme_xls_forms

# Global Outlook
DataBridgesKnots.get_global_outlook = get_global_outlook

# Economic Data
DataBridgesKnots.get_economic_indicator_list = get_economic_indicator_list

# Ipc and CH data
DataBridgesKnots.get_ipc_and_equivalent_data = get_ipc_and_equivalent_data

# CARI data
DataBridgesKnots.get_cari_data = get_cari_data

# Hunger Hotspot data
DataBridgesKnots.get_hunger_hotspot_data = get_hunger_hotspot_data


# MFI Endpoints (SurveysApi)
DataBridgesKnots.get_mfi_surveys_base_data = get_mfi_surveys_base_data
DataBridgesKnots.get_mfi_surveys_full_data = get_mfi_surveys_full_data
DataBridgesKnots.get_mfi_surveys = get_mfi_surveys
DataBridgesKnots.get_mfi_surveys_processed_data = get_mfi_surveys_processed_data
DataBridgesKnots.get_mfi_xls_forms = get_mfi_xls_forms
DataBridgesKnots.get_mfi_xls_forms_detailed = get_mfi_xls_forms_detailed


if __name__ == "__main__":
    pass
