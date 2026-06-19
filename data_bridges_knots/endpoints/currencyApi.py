from typing import Optional

import logging
import time

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


class CurrencyApi:
    def get_exchange_rates(
        self, country_iso3: str, page_size: int = 1000
    ) -> pd.DataFrame:
        """Retrieves exchange rates for a given country from the Data Bridges API.

        Args:
            country_iso3 (str): The ISO3 country code
            page_size (int, optional): Number of items per page. Defaults to 1000

        Returns:
            pd.DataFrame: DataFrame containing exchange rate data with columns:
                - date: Date of exchange rate
                - rate: Exchange rate value
                - currency: Currency code
                And other relevant exchange rate information

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Get exchange rates for Ethiopia
            >>> rates_df = client.get_exchange_rates("ETH")
            >>> # Check latest exchange rate
            >>> latest_rate = rates_df.sort_values('date').iloc[-1]

        Raises:
            ApiException: If there's an error calling the Exchange rates API
        """

        responses = []
        total_items = 20
        max_item = 0
        page = 0
        while total_items > max_item:
            page += 1
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.CurrencyApi(api_client)
                env = self.env

                try:
                    api_exchange_rates = (
                        api_instance.currency_usd_indirect_quotation_get(
                            country_iso3=country_iso3, format="json", page=page, env=env
                        )
                    )
                    responses.extend(
                        item.to_dict() for item in api_exchange_rates.items
                    )
                    total_items = api_exchange_rates.total_items
                    logger.info("Fetching page %s", page)
                    max_item = page * page_size
                    time.sleep(1)
                except ApiException as e:
                    logger.error(
                        "Exception when calling Exchange rates data-> : %s\n",
                        e,
                    )
                    raise
        df = pd.DataFrame(responses)
        df = df.replace({np.nan: None})
        return df

    def get_currency_list(
        self,
        country_iso3: Optional[str] = None,
        currency_name: Optional[str] = None,
        currency_id: Optional[str] = 0,
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        """
        Returns the list of currencies available in the internal VAM database, with Currency 3-letter code, matching with ISO 4217.

        Args:
            country_iso3 (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            currency_name (str, optional): Currency 3-letter code, matching with ISO 4217.
            currency_id (int, optional): Unique code to identify the currency in internal VAM currencies. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Get currencies for Tanzania
            >>> currencies_df = client.get_currency_list(country_iso3="TZA")
            >>> # Get currency with name "ETB"
            >>> etb_df = client.get_currency_list(currency_name="ETB")
            >>> # Get currency with specific ID
            >>> specific_currency_df = client.get_currency_list(currency_id=1)

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved currency data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CurrencyApi(api_client)
            env = self.env

            try:
                api_response = api_instance.currency_list_get(
                    country_code=country_iso3,
                    currency_name=currency_name,
                    currency_id=currency_id,
                    page=page,
                    format=format,
                    env=env,
                )
                logger.info("Successfully retrieved currency list")

                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(
                    f"Exception when calling CurrencyApi->currency_list_get: {e}"
                )
                raise

    def get_usd_indirect_quotation(
        self,
        country_iso3: Optional[str] = "",
        currency_name: Optional[str] = "",
        page: Optional[int] = 1,
        format: Optional[str] = "json",
    ) -> pd.DataFrame:
        """
        Returns the value of the Exchange rates from Trading Economics, for official rates, and DataViz for unofficial rates.

        Args:
            country_iso3 (str, optional): The code to identify the country. Must be a ISO-3166 Alpha 3 code. Defaults to ''.
            currency_name (str, optional): The ISO3 code for the currency, based on ISO4217. Defaults to ''.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Get USD indirect quotation for Ethiopia
            >>> usd_df = client.get_usd_indirect_quotation(country_iso3="ETH")
            >>> # Get USD indirect quotation for currency "ETB"
            >>> etb_usd_df = client.get_usd_indirect_quotation(currency_name="ETB")

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved exchange rate data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CurrencyApi(api_client)
            env = self.env

            try:
                api_response = api_instance.currency_usd_indirect_quotation_get(
                    country_iso3=country_iso3,
                    currency_name=currency_name,
                    page=page,
                    format=format,
                    env=env,
                )
                logger.info("Successfully retrieved USD indirect quotation data")

                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(
                    f"Exception when calling CurrencyApi->currency_usd_indirect_quotation_get: {e}"
                )
                raise
