from typing import Optional

import logging

import data_bridges_client
import numpy as np
import pandas as pd
from data_bridges_client.rest import ApiException

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


def get_market_geojson_list(self, country_iso3: str = None):
    """Returns a list of geo-referenced markets in a specific country."""
    if country_iso3 is None:
        raise ValueError("country_iso3 parameter is required")
    else:
        adm0code = get_adm0_code(country_iso3)

    # Enter a context with an instance of the API client
    with data_bridges_client.ApiClient(self.configuration) as api_client:
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
    with data_bridges_client.ApiClient(self.configuration) as api_client:
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
            logger.error("Exception when calling MarketsApi->markets_list_get: %s", e)
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

    with data_bridges_client.ApiClient(self.configuration) as api_client:
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
    with data_bridges_client.ApiClient(self.configuration) as api_client:
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
