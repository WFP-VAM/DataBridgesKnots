from typing import Literal, Optional

import logging

import data_bridges_client
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


# GlobalOutlookApi 	global_outlook_country_latest_get 	GET /GlobalOutlook/CountryLatest 	Return the latest country dataset of number of acutely food insecure (in thousands) based on WFP's Global Outlook.
# GlobalOutlookApi 	global_outlook_global_latest_get 	GET /GlobalOutlook/GlobalLatest 	Return the latest global dataset of number of acutely food insecure (in millions) based on WFP's Global Outlook.
# GlobalOutlookApi 	global_outlook_regional_latest_get 	GET /GlobalOutlook/RegionalLatest 	Return the latest regional dataset of number of acutely food insecure (in millions) based on WFP's Global Outlook.


# FIXME: Get scopes to test this function
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
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        # Create an instance of the API class
        api_instance = data_bridges_client.GlobalOutlookApi(api_client)
        env = (
            self.env
        )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

        try:
            if data_type == "country_latest":
                api_response = api_instance.global_outlook_country_latest_get(env=env)
            elif data_type == "global_latest":
                api_response = api_instance.global_outlook_global_latest_get(env=env)

            elif data_type == "regional_latest":
                api_response = api_instance.global_outlook_regional_latest_get(env=env)
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
