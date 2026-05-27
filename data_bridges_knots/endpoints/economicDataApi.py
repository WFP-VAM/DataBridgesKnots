from typing import Optional

import logging

import data_bridges_client
import numpy as np
import pandas as pd

logname = "data_bridges_api_calls.log"
logging.basicConfig(
    filename=logname,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


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
