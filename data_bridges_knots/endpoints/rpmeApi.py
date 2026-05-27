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


# TODO: Get the scope and test these functions
def get_rpme_base_data(self, survey_id=None, page: Optional[int] = 1, page_size=20):
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
            logger.error(f"Exception when calling RpmeApi->rpme_base_data_get: {e}")
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
            logger.error(f"Exception when calling RpmeApi->rpme_full_data_get: {e}")
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
            logger.error(f"Exception when calling RpmeApi->rpme_output_values_get: {e}")
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
            logger.error(f"Exception when calling RpmeApi->rpme_surveys_get: {e}")
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
            logger.error(f"Exception when calling RpmeApi->rpme_variables_get: {e}")
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
            logger.error(f"Exception when calling RpmeApi->rpme_xls_forms_get: {e}")
            raise
