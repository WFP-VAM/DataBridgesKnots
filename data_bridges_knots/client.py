from typing import Dict, Literal, Optional, Union

import logging
import os
import warnings

import data_bridges_client
import numpy as np
import pandas as pd
import yaml
from data_bridges_client.rest import ApiException
from data_bridges_client.token import WfpApiToken

from data_bridges_knots.endpoints.commodityUnitsApi import (
    get_commodities_list,
    get_commodity_unit_conversion_list,
    get_commodity_units_list,
)
from data_bridges_knots.endpoints.currencyApi import (
    get_currency_list,
    get_exchange_rates,
    get_usd_indirect_quotation,
)
from data_bridges_knots.endpoints.householdApi import (
    get_household_questionnaire,
    get_household_survey,
    get_household_surveys_list,
    get_household_xlsform_definition,
)
from data_bridges_knots.endpoints.marketPricesApi import get_prices
from data_bridges_knots.helpers import get_adm0_code

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

    def get_economic_indicator_list(
        self,
        page: Optional[int] = 1,
        indicator_name: Optional[str] = "",
        country_iso3: Optional[str] = "",
        format: Optional[str] = "json",
    ):
        """
        Returns the lists of indicators for which Vulnerability Analysis and Mapping - Economic and Market Analysis Unit has redistribution licensing from Trading Economics.

        Args:
            page (int, optional): Page number for paged results. Defaults to 1.
            indicator_name (str, optional): Unique indicator name. Defaults to ''.
            iso3 (str, optional): The code to identify the country. Must be a ISO-3166 Alpha 3 code. Defaults to ''.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved economic indicator data.
        """
        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.EconomicDataApi(api_client)

            try:
                # Returns the lists of indicators.
                api_response = api_instance.economic_data_indicator_list_get(
                    page=page,
                    indicator_name=indicator_name,
                    iso3=country_iso3,
                    format=format,
                    env=self.env,
                )
                logger.info(
                    "The response of EconomicDataApi->economic_data_indicator_list_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
                return api_response
            except Exception as e:
                logger.error(
                    "Exception when calling EconomicDataApi->economic_data_indicator_list_get: %s",
                    e,
                )
                raise

    def get_market_geojson_list(self, country_iso3: str = None):
        """Returns a list of geo-referenced markets in a specific country."""
        if country_iso3 is None:
            raise ValueError("country_iso3 parameter is required")
        else:
            adm0code = get_adm0_code(country_iso3)

        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.MarketsApi(api_client)

            try:
                # Provide a list of geo referenced markets in a specific country
                api_response = api_instance.markets_geo_json_list_get(
                    adm0code=adm0code, env=self.env
                )
                logger.info("The response of MarketsApi->markets_geo_json_list_get:\n")

                geojson_dict = api_response.model_dump()

                return geojson_dict
                return api_response
            except Exception as e:
                logger.error(
                    "Exception when calling MarketsApi->markets_geo_json_list_get: %s",
                    e,
                )
                raise

    def get_markets_list(
        self, country_iso3: Optional[str] = None, page: Optional[int] = 1
    ) -> pd.DataFrame:
        """Retrieves a complete list of markets in a country.

        Args:
            country_iso3 (str, optional): The ISO3 code to identify the country. Defaults to None.
            page (int, optional): Page number for paginated results. Defaults to 1.

        Returns:
            pd.DataFrame: DataFrame containing market information with columns:
                - market_id: Unique identifier for the market
                - market_name: Name of the market
                - adm0_code: Country administrative code
                - latitude: Market location latitude
                - longitude: Market location longitude
                And other market-related fields

        Examples:
            >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
            >>> # Get markets for Afghanistan
            >>> afg_markets = client.get_markets_list("AFG")

        Raises:
            ApiException: If there's an error accessing the Markets API
        """
        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.MarketsApi(api_client)
            format = "json"  # str | Output format: [JSON|CSV] Json is the default value (optional) (default to 'json')
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Get a complete list of markets in a country
                api_response = api_instance.markets_list_get(
                    country_code=country_iso3, page=page, format=format, env=env
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling MarketsApi->markets_list_get: %s", e
                )
                raise

    def get_markets_as_csv(
        self, country_iso3: Optional[str] = None, local_names: bool = False
    ) -> str:
        """Retrieves a complete list of markets in a country in CSV format.

        Args:
            country_iso3 (str, optional): Country administrative code. Defaults to None.
            local_names (bool, optional): If True, market and region names will be
                localized if available. Defaults to False.

        Returns:
            str: CSV formatted string containing market data

        Examples:
            >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
            >>> # Get markets CSV for Afghanistan
            >>> markets_csv = client.get_markets_as_csv("AFG")
            >>> # Get localized market names
            >>> local_markets = client.get_markets_as_csv("AFG", local_names=True)

        Raises:
            ApiException: If there's an error accessing the Markets API
        """

        adm0code = get_adm0_code(country_iso3)

        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            api_instance = data_bridges_client.MarketsApi(api_client)
            local_names = False  # bool | If true the name of markets and regions will be localized if available (optional) (default to False)

            try:
                # Get a complete list of markets in a country
                api_response = api_instance.markets_markets_as_csv_get(
                    adm0code=adm0code, local_names=local_names, env=self.env
                )
                logger.info("The response of MarketsApi->markets_markets_as_csv_get:\n")
                return api_response
            except Exception as e:
                logger.error(
                    "Exception when calling MarketsApi->markets_markets_as_csv_get: %s",
                    e,
                )
                raise

    def get_nearby_markets(
        self, country_iso3: str = None, lat: float = None, lng: float = None
    ) -> pd.DataFrame:
        """Finds markets near a given location within a 15km distance.

        Args:
            country_iso3 (str): Country administrative code. Defaults to None.
            lat (float): Latitude of the search point. Defaults to None.
            lng (float): Longitude of the search point. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing nearby markets with columns:
                - market_id: Unique identifier for the market
                - market_name: Name of the market
                - distance: Distance from search point in kilometers
                - latitude: Market location latitude
                - longitude: Market location longitude
                And other market-related fields

        Examples:
            >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
            >>> # Find markets near coordinates in Afghanistan
            >>> nearby = client.get_nearby_markets("AFG", 34.515, 69.208)
            >>> # Sort markets by distance
            >>> closest = nearby.sort_values('distance').iloc[0]

        Raises:
            ApiException: If there's an error accessing the Markets API
        """

        adm0code = get_adm0_code(country_iso3)
        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            api_instance = data_bridges_client.MarketsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.markets_nearby_markets_get(
                    adm0code=adm0code, lat=lat, lng=lng, env=env
                )
                logger.info("Successfully retrieved nearby markets")
                df = pd.DataFrame([item.to_dict() for item in api_response])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(
                    f"Exception when calling MarketsApi->markets_nearby_markets_get: {e}"
                )
                raise

    def get_global_outlook(
        self,
        data_type: Literal["country_latest", "global_latest", "regional_latest"],
        page: Optional[int] = None,
    ) -> pd.DataFrame:
        """Retrieves data from the Global Outlook API.

        The Global Outlook API provides access to WFP’s forward-looking analysis and
        aggregated insights at different geographical levels, including country,
        regional, and global summaries.

        Args:
            data_type (str): The type of Global Outlook data to retrieve. Must be one of:
                - 'country_latest': Latest data at country level
                - 'global_latest': Latest global aggregated data
                - 'regional_latest': Latest data aggregated by region
            page (int, optional): Page number for paginated results. Currently not used
                for latest endpoints. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing Global Outlook data for the selected scope.

        Examples:
            >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
            >>> # Get latest country-level outlook
            >>> country_data = client.get_global_outlook("country_latest")
            >>> # Get global outlook summary
            >>> global_data = client.get_global_outlook("global_latest")
            >>> # Get regional outlook data
            >>> regional_data = client.get_global_outlook("regional_latest")

        Raises:
            ValueError: If data_type is not one of the allowed values
            ApiException: If there is an error accessing the Global Outlook API
        """

        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(
            self._setup_configuration_and_authentication(self.config)
        ) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.GlobalOutlookApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                if data_type == "country_latest":
                    api_response = api_instance.global_outlook_country_latest_get(
                        env=env
                    )
                elif data_type == "global_latest":
                    api_response = api_instance.global_outlook_global_latest_get(
                        env=env
                    )

                elif data_type == "regional_latest":
                    api_response = api_instance.global_outlook_regional_latest_get(
                        env=env
                    )
                else:
                    raise ValueError(f"Invalid data_type: {data_type}")
                logger.info(
                    f"Successfully retrieved Global Outlook data for type: {data_type}"
                )
                return pd.DataFrame([item.to_dict() for item in api_response.items])

            except Exception as e:
                logger.error(
                    "Exception when calling GlobalOutlookApi->%s: %s", data_type, e
                )
                raise

    def get_choice_list(self, xls_form_id: int) -> pd.DataFrame:
        """Extracts choice lists from a questionnaire form definition.

        Args:
            xls_form_id (int): The ID of the questionnaire form to process

        Returns:
            pd.DataFrame: DataFrame containing choice lists with columns:
                - name: Name of the choice list
                - value: Choice value/code
                - label: Human-readable choice label

        Examples:
            >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
            >>> choices = client.get_choice_list(123)
        """
        questionnaire = self.get_household_questionnaire(xls_form_id)

        choiceList = pd.json_normalize(questionnaire["choiceList"]).dropna()
        choices = choiceList.explode("choices")
        choices["value"] = choices["choices"].apply(lambda x: x["name"])
        choices["label"] = choices["choices"].apply(lambda x: x["label"])
        return choices[["name", "value", "label"]]

        # TODO: Get the scope and test these functions
        def get_rpme_base_data(
            self, survey_id=None, page: Optional[int] = 1, page_size=20
        ):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_base_data_get(
                        survey_id=survey_id, page=page, page_size=page_size, env=env
                    )
                    logger.info("Successfully retrieved RPME base data")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_base_data_get: {e}"
                    )
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_full_data(
            self,
            survey_id=None,
            format: Optional[str] = "json",
            page: Optional[int] = 1,
            page_size=20,
        ):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_full_data_get(
                        survey_id=survey_id,
                        format=format,
                        page=page,
                        page_size=page_size,
                        env=env,
                    )
                    logger.info("Successfully retrieved RPME full data")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_full_data_get: {e}"
                    )
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_output_values(
            self,
            page: Optional[int] = 1,
            adm0_code=None,
            survey_id=None,
            shop_id=None,
            market_id=None,
            adm0_code_dots="",
        ):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_output_values_get(
                        page=page,
                        adm0_code=adm0_code,
                        survey_id=survey_id,
                        shop_id=shop_id,
                        market_id=market_id,
                        adm0_code_dots=adm0_code_dots,
                        env=env,
                    )
                    logger.info("Successfully retrieved RPME output values")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_output_values_get: {e}"
                    )
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_surveys(
            self, adm0_code=0, page: Optional[int] = 1, start_date=None, end_date=None
        ):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_surveys_get(
                        adm0_code=adm0_code,
                        page=page,
                        start_date=start_date,
                        end_date=end_date,
                        env=env,
                    )
                    logger.info("Successfully retrieved RPME surveys")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_surveys_get: {e}"
                    )
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_variables(self, page: Optional[int] = 1):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_variables_get(page=page, env=env)
                    logger.info("Successfully retrieved RPME variables")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_variables_get: {e}"
                    )
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_xls_forms(
            self, adm0_code=0, page: Optional[int] = 1, start_date=None, end_date=None
        ):
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_xls_forms_get(
                        adm0_code=adm0_code,
                        page=page,
                        start_date=start_date,
                        end_date=end_date,
                        env=env,
                    )
                    logger.info("Successfully retrieved RPME XLS forms")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(
                        f"Exception when calling RpmeApi->rpme_xls_forms_get: {e}"
                    )
                    raise

        # Add this function to the DataBridgesShapes class

    def get_ipc_and_equivalent_data(self):
        pass

    def get_hotpost_data(self):
        pass

    def get_aims_data(self):
        pass

    def get_rpme_data(self):
        pass

    def get_cari_data(self):
        pass


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

# Currency Endpoints (CurrencyApi)
DataBridgesKnots.get_exchange_rate = get_exchange_rates
DataBridgesKnots.get_currency_list = get_currency_list
DataBridgesKnots.get_usd_indirect_quotation = get_usd_indirect_quotation

# Market Prices Endpoints (MarketPricesApi)
DataBridgesKnots.marketPricesApi.get_prices = get_prices

# Commodity Units Endpoints (CommodityUnitsApi)
DataBridgesKnots.commodityUnitsApi.get_commodities_list = get_commodities_list
DataBridgesKnots.commodityUnitsApi.get_commodity_units_list = get_commodity_units_list
DataBridgesKnots.commodityUnitsApi.get_commodity_units_conversion_list = (
    get_commodity_unit_conversion_list
)

if __name__ == "__main__":
    pass
