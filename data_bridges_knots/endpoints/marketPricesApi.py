from typing import Optional

import logging
import time
from datetime import date

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


class MarkertPricesApi:
    def get_prices(
        self,
        country_iso3: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page_size: int = 1000,
        market_id: int = 0,
        commodity_id: int = 0,
        currency_id: int = 0,
        price_flag: str = "",
        latest_value_only: bool = False,
    ) -> pd.DataFrame:
        """Fetches market price data for a given country within a specified date range.

        Args:
            country_iso3 (str): The ISO 3-letter country code
            start_date (str, optional): Start date in ISO format (e.g., '2022-01-01').
                If None, defaults to today's date.
            end_date (str, optional): End date in ISO format (e.g., '2022-01-01').
                If None, defaults to today's date.
            page_size (int, optional): Number of items per page. Defaults to 1000.
            market_id (int, optional): Unique ID of a Market. Defaults to 0.
            commodity_id (int, optional): The exact ID of a Commodity. Defaults to 0.
            currency_id (int, optional): The exact ID of a currency. Defaults to 0.
            price_flag (str, optional): Type of price data: [actual|aggregate|estimated|forecasted]. Defaults to ''.
            latest_value_only (bool, optional): Whether to return only latest values. Defaults to False.

        Returns:
            pd.DataFrame: DataFrame containing market price data

        Examples:
            >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
            >>> # Basic usage with dates
            >>> df_prices = client.get_prices("KEN", start_date="2025-01-01", end_date="2025-12-31")
            >>> # Using additional filters
            >>> df_prices = client.get_prices(
            ...     "KEN",
            ...     start_date="2025-01-01",
            ...     market_id=123,
            ...     commodity_id=456,
            ...     price_flag="actual"
            ... )
        """
        if start_date:
            # Format the date according to RFC 3339 standard
            start_date = date.fromisoformat(start_date).strftime(
                "%Y-%m-%dT%H:%M:%S+01:00"
            )
        else:
            start_date = date.today().strftime("%Y-%m-%dT%H:%M:%S+01:00")

        if end_date:
            # Format the date according to RFC 3339 standard
            end_date = date.fromisoformat(end_date).strftime("%Y-%m-%dT%H:%M:%S+01:00")
        else:
            end_date = date.today().strftime("%Y-%m-%dT%H:%M:%S+01:00")

        responses = []
        total_items = 20
        max_item = 0
        page = 0
        while total_items > max_item:
            page += 1
            with data_bridges_client.ApiClient(
                self._setup_configuration_and_authentication(self.config)
            ) as api_client:
                api_instance = data_bridges_client.MarketPricesApi(api_client)
                env = self.env

                try:
                    api_prices = api_instance.market_prices_price_monthly_get(
                        country_code=country_iso3,
                        market_id=market_id,
                        commodity_id=commodity_id,
                        currency_id=currency_id,
                        price_flag=price_flag,
                        format="json",
                        page=page,
                        env=env,
                        start_date=start_date,
                        end_date=end_date,
                        latest_value_only=latest_value_only,
                    )
                    responses.extend(item.to_dict() for item in api_prices.items)
                    total_items = api_prices.total_items
                    logger.info("Fetching page %s/n", page)
                    max_item = page * page_size
                    time.sleep(1)
                except ApiException as e:
                    logger.error(
                        "Exception when calling Market price data->market_prices_price_monthly_get: %s\n",
                        e,
                    )
                    raise

        df = pd.DataFrame(responses)
        df = df.replace({np.nan: None})
        return df
