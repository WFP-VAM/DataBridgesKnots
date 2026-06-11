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


def get_mfi_surveys_base_data(
    self, survey_id=None, page: Optional[int] = 1, page_size=20
):
    """
    Get data that includes the core Market Functionality Index (MFI) fields only by Survey ID.

    Args:
        survey_id (int): Unique identifier for the collected data
        page (int): Page number for paged results
        page_size (int): Number of items per page

    Examples:
        >>> client = DataBridgesKnotss("data_bridges_api_config.yaml")
        >>> # Get MFI base data for a specific survey
        >>> base_data = client.get_mfi_surveys_base_data(survey_id=123)

    Returns:
        pandas.DataFrame: DataFrame containing MFI base survey data
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.SurveysApi(api_client)
        env = self.env

        try:
            api_response = api_instance.m_fi_surveys_base_data_get(
                survey_id=survey_id, page=page, page_size=page_size, env=env
            )
            logger.info("Successfully retrieved MFI surveys base data")
            return pd.DataFrame(api_response.items)

        except ApiException as e:
            logger.error(
                f"Exception when calling SurveysApi->m_fi_surveys_base_data_get: {e}"
            )
            raise


def get_mfi_surveys_full_data(
    self, survey_id=None, page: Optional[int] = 1, page_size=20
):
    """
    Get a full dataset that includes all the fields included in the survey in addition to the core Market Functionality Index (MFI) fields by Survey ID.
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.SurveysApi(api_client)
        env = self.env
        try:
            api_response = api_instance.m_fi_surveys_full_data_get(
                survey_id=survey_id,
                format="json",
                page=page,
                page_size=page_size,
                env=env,
            )
            logger.info("Successfully retrieved MFI surveys full data")
            df = pd.DataFrame(api_response.items)
            return df
        except ApiException as e:
            logger.error(
                f"Exception when calling SurveysApi->m_fi_surveys_full_data_get: {e}"
            )
            raise


def get_mfi_surveys(
    self, adm0_code=0, page: Optional[int] = 1, start_date=None, end_date=None
):
    """
    Retrieve Survey IDs, their corresponding XLS Form IDs, and Base XLS Form of all MFI surveys conducted in a country.
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.SurveysApi(api_client)
        env = self.env

        try:
            api_response = api_instance.m_fi_surveys_get(
                adm0_code=adm0_code,
                page=page,
                start_date=start_date,
                end_date=end_date,
                env=env,
            )
            logger.info("Successfully retrieved MFI surveys list")
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            df = df.replace({np.nan: None})
            return df
        except ApiException as e:
            logger.error(f"Exception when calling SurveysApi->m_fi_surveys_get: {e}")
            raise


def get_mfi_surveys_processed_data(
    self,
    survey_id=None,
    page: Optional[int] = 1,
    page_size=20,
    format: Optional[str] = "json",
    start_date=None,
    end_date=None,
    adm0_codes=None,
    market_id=None,
    survey_type=None,
):
    """
    Get MFI processed data in long format.
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.SurveysApi(api_client)
        env = self.env

        try:
            api_response = api_instance.m_fi_surveys_processed_data_get(
                survey_id=survey_id,
                page=page,
                page_size=page_size,
                format=format,
                start_date=start_date,
                end_date=end_date,
                adm0_codes=adm0_codes,
                market_id=market_id,
                survey_type=survey_type,
                env=env,
            )
            logger.info("Successfully retrieved MFI surveys processed data")
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            df = df.replace({np.nan: None})
            return df
        except ApiException as e:
            logger.error(
                f"Exception when calling SurveysApi->m_fi_surveys_processed_data_get: {e}"
            )
            raise


def get_mfi_xls_forms(
    self, adm0_code=0, page: Optional[int] = 1, start_date=None, end_date=None
):
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.XlsFormsApi(api_client)
        env = self.env

        try:
            api_response = api_instance.m_fi_xls_forms_get(
                adm0_code=adm0_code,
                page=page,
                start_date=start_date,
                end_date=end_date,
                env=env,
            )
            logger.info("Successfully retrieved MFI XLS forms")
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            df = df.replace({np.nan: None})
            return df
        except ApiException as e:
            logger.error(f"Exception when calling XlsFormsApi->m_fi_xls_forms_get: {e}")
            raise


def get_mfi_xls_forms_detailed(
    self, adm0_code=0, page: Optional[int] = 1, start_date=None, end_date=None
):
    """
    Get a complete list of XLS Forms uploaded on the MFI Data Bridge in a given period of data collection.

    Args:
        adm0_code (int): Code for the country. Defaults to 0.
        page (int): Page number for paged results. Defaults to 1.
        start_date (str): Starting date for data collection range (YYYY-MM-DD format)
        end_date (str): Ending date for data collection range (YYYY-MM-DD format)

    Examples:
        >>> client = DataBridgesKnotss("data_bridges_api_config.yaml")
        >>> # Get detailed XLS forms for country code 231
        >>> detailed_forms = client.get_mfi_xls_forms_detailed(adm0_code=231)
        >>> # Get forms within a date range
        >>> forms_in_range = client.get_mfi_xls_forms_detailed(
        ...     adm0_code=231,
        ...     start_date="2023-01-01",
        ...     end_date="2023-12-31"
        ... )

    Returns:
        pandas.DataFrame: DataFrame containing XLS Forms data
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.XlsFormsApi(api_client)
        env = self.env

        try:
            api_response = api_instance.m_fi_xls_forms_get(
                adm0_code=adm0_code,
                page=page,
                start_date=start_date,
                end_date=end_date,
                env=env,
            )
            logger.info("Successfully retrieved detailed MFI XLS forms")

            # Convert response items to DataFrame
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            df = df.replace({np.nan: None})

            # Add total items count as DataFrame attribute
            df.total_items = api_response.total_items

            return df

        except ApiException as e:
            logger.error(f"Exception when calling XlsFormsApi->m_fi_xls_forms_get: {e}")
            raise
