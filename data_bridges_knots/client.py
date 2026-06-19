from typing import Dict, Union

import logging
import os

import data_bridges_client
import yaml
from data_bridges_client.token import WfpApiToken

from data_bridges_knots.endpoints import (
    CommodityApi,
    CurrencyApi,
    EconomicDataApi,
    GlobalOutlookApi,
    HouseholdApi,
    HungerHotspotApi,
    IncubationApi,
    IpcchApi,
    MarketPricesApi,
    MarketsApi,
    MfiSurveysApi,
    RpmeApi,
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
        dict: Configuration dictionary with required keys for DataBridgesKnots

    Raises:
        ValueError: If any required environment variables are missing

    Examples:
        >>> import os
        >>> os.environ['WFP_API_CLIENT_ID'] = 'your_key'
        >>> os.environ['WFP_API_CLIENT_SECRET'] = 'your_secret'
        >>> os.environ['DATABRIDGES_API_KEY'] = 'your_databridges_key'  # Optional
        >>> os.environ['DATABRIDGES_VERSION'] = 'v2'  # Optional, defaults to v2
        >>> config = config_from_env()
        >>> client = DataBridgesKnots(config)
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


class DataBridgesKnots(
    HouseholdApi,
    CommodityApi,
    CurrencyApi,
    EconomicDataApi,
    GlobalOutlookApi,
    HungerHotspotApi,
    IncubationApi,
    IpcchApi,
    MarketPricesApi,
    MarketsApi,
    RpmeApi,
    MfiSurveysApi,
):
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
        api_version (str, optional): Data Bridges API version to use. Defaults to "v2" (current version)


    Examples:
        >>> # Initialize with YAML file
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
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

    def __init__(self, config_path, env="prod", api_version="v2"):
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
        # print("host: ", host) #FIXME: this run every single page!

        logger.info("DataBridges API: %s", host)

        token = WfpApiToken(api_key=key, api_secret=secret)
        configuration = data_bridges_client.Configuration(
            host=host, access_token=token.refresh()
        )

        logger.debug("Token used: %s", token.__repr__())
        return configuration


if __name__ == "__main__":
    pass
