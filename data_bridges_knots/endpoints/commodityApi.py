from typing import Optional

import logging

import data_bridges_client
import numpy as np
import pandas as pd
from data_bridges_client.rest import ApiException

logname = "data_bridges_api_calls.log"
logging.basicConfig(
    filename=logname,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class CommodityApi:
    def get_commodities_list(
        self,
        country_iso3: Optional[str] = None,
        commodity_name: Optional[str] = None,
        commodity_id: Optional[int] = 0,
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        """
        Retrieves the detailed list of commodities available in the DataBridges platform.

        Args:
            country_iso3 (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_name (str, optional): The name, even partial and case insensitive, of a commodity.
            commodity_id (int, optional): The exact ID of a commodity. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Get full list of commmodities
            >>> commodities_list = client.get_commodities_list()
            >>> # Get commodities for Tanzania
            >>> commodities_df = client.get_commodities_list(country_iso3="TZA")
            >>> # Get commodity with name containing "Maize"
            >>> maize_df = client.get_commodities_list(commodity_name="Maize")
            >>> # Get commodity with specific ID
            >>> specific_commodity_df = client.get_commodities_list(commodity_id=123)

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved commodity data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommoditiesApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodities_list_get(
                    country_code=country_iso3,
                    commodity_name=commodity_name,
                    commodity_id=commodity_id,
                    page=page,
                    format=format,
                    env=env,
                )
                logger.info("Successfully retrieved commodities list")

                # Convert the response to a DataFrame
                if hasattr(api_response, "items"):
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                else:
                    df = pd.DataFrame([api_response.to_dict()])

                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(
                    f"Exception when calling CommoditiesApi->commodities_list_get: {e}"
                )
                raise


    def get_commodity_units_conversion_list(
        self,
        country_iso3: Optional[str] = None,
        commodity_id: Optional[int] = 0,
        from_unit_id: Optional[int] = 0,
        to_unit_id: Optional[int] = 0,
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        """
        Retrieves conversion factors to Kilogram or Litres for each convertible unit of measure.

        Args:
            country_iso3 (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_id (int, optional): The exact ID of a Commodity, as found in /Commodities/List. Defaults to 0.
            from_unit_id (int, optional): The exact ID of the original unit of measure of the price of a commodity. Defaults to 0.
            to_unit_id (int, optional): The exact ID of the converted unit of measure of the price of a commodity. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> # Get full list of commodity units conversions
        >>> full_list = client.get_commodity_units_conversion_list()
        >>> # Get conversion factors for Tanzania
        >>> conversion_factors_df = client.get_commodity_units_conversion_list(country_iso3="TZA")

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved conversion factors.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommodityUnitsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodity_units_conversion_list_get(
                    country_code=country_iso3,
                    commodity_id=commodity_id,
                    from_unit_id=from_unit_id,
                    to_unit_id=to_unit_id,
                    page=page,
                    format=format,
                    env=env,
                )
                logger.info("Successfully retrieved commodity units conversion list")

                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(
                    f"Exception when calling CommodityUnitsApi->commodity_units_conversion_list_get: {e}"
                )
                raise


    def get_commodity_units_list(
        self,
        country_iso3: Optional[str] = None,
        commodity_unit_name: Optional[str] = None,
        commodity_unit_id: Optional[int] = 0,
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        """
        Retrieves the detailed list of the unit of measure available in DataBridges platform.

        Args:
            country_iso3 (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_unit_name (str, optional): The name, even partial and case insensitive, of a commodity unit.
            commodity_unit_id (int, optional): The exact ID of a commodity unit. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Get commodity units for Tanzania
            >>> units_df = client.get_commodity_units_list(country_iso3="TZA")
            >>> # Get commodity unit with name containing "Kg"
            >>> kg_unit_df = client.get_commodity_units_list(commodity_unit_name="Kg")
            >>> # Get commodity unit with specific ID
            >>> specific_unit_df = client.get_commodity_units_list(commodity_unit_id=5)

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved commodity units data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommodityUnitsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodity_units_list_get(
                    country_code=country_iso3,
                    commodity_unit_name=commodity_unit_name,
                    commodity_unit_id=commodity_unit_id,
                    page=page,
                    format=format,
                    env=env,
                )
                logger.info("Successfully retrieved commodity units list")

                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(
                    f"Exception when calling CommodityUnitsApi->commodity_units_list_get: {e}"
                )
                raise


    def get_commodity_categories_list(
        self,
        category_id: Optional[int] = 0,
        country_iso3: Optional[str] = None,
        category_name: Optional[str] = None,
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        # Enter a context with an instance of the API client
        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.CommoditiesApi(api_client)
            env = self.env

            try:
                # Provides the list of categories.
                api_response = api_instance.commodities_categories_list_get(
                    country_code=country_iso3,
                    category_name=category_name,
                    category_id=category_id,
                    page=page,
                    format=format,
                    env=env,
                )

                logger.info(
                    "The response of CommoditiesApi->commodities_categories_list_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling CommoditiesApi->commodities_categories_list_get: %s\n"
                    % e
                )
