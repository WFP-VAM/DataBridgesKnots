from typing import Optional

import logging
import time

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
        >>> client = DataBridgesShapes("data_bridges_api_config.yaml")
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
