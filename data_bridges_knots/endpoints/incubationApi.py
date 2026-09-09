import logging

import data_bridges_client
import numpy as np
import pandas as pd

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


class IncubationApi:
    """
    Retrieves a paginated list of Adm0 and Adm1 CARI results based on the specified indicator, administrative code, and survey.
    """

    def get_cari_adm0(
        self, country_iso3=None, survey_id=None, indicator_id=None, page=1
    ) -> pd.DataFrame:
        """ "
        Retrieves a paginated list of Adm0 CARI results based on the specified indicator, administrative code, and survey.

        Args:
            country_iso3 (str, optional): ISO3 code of the country for which to retrieve Adm0 CARI results. If not provided, retrieves results for all countries.
            survey_id (str, optional): ID of the survey for which to retrieve Adm0 CARI results. If not provided, retrieves results for all surveys.
            indicator_id (str, optional): ID of the indicator for which to retrieve Adm0 CARI results. If not provided, retrieves results for all indicators.
            page (int, optional): Page number for paginated results. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved Adm0 CARI results.

        Raises:
            ApiException: If an error occurs while calling the IncubationApi.

        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IncubationApi(api_client)
            adm0code = get_adm0_code(country_iso3) if country_iso3 else None

            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Retrieves a paginated list of Adm0 CARI results based on the specified indicator, administrative code, and  survey.
                api_response = api_instance.cari_adm0_values_get(
                    adm0_code=adm0code,
                    survey_id=survey_id,
                    indicator_id=indicator_id,
                    page=page,
                    env=env,
                )
                logger.info(
                    f"The response of IncubationApi->cari_adm0_values_get: {api_response}\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except Exception as e:
                logger.error(
                    f"Exception when calling IncubationApi->cari_adm0_values_get: {e}\n"
                )
                raise

    def get_cari_adm1(
        self, country_iso3=None, survey_id=None, indicator_id=None, page=1
    ):
        """ "
        Retrieves a paginated list of Adm1 CARI results based on the specified indicator, administrative code, and survey.

        Args:
            country_iso3 (str, optional): ISO3 code of the country for which to retrieve Adm1 CARI results. If not provided, retrieves results for all countries.
            survey_id (str, optional): ID of the survey for which to retrieve Adm1 CARI results. If not provided, retrieves results for all surveys.
            indicator_id (str, optional): ID of the indicator for which to retrieve Adm1 CARI results. If not provided, retrieves results for all indicators.
            page (int, optional): Page number for paginated results. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved Adm1 CARI results.

        Raises:
            ApiException: If an error occurs while calling the IncubationApi.

        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            adm0code = get_adm0_code(country_iso3) if country_iso3 else None

            try:
                api_response = api_instance.cari_adm1_values_get(
                    adm0_code=adm0code,
                    survey_id=survey_id,
                    indicator_id=indicator_id,
                    page=page,
                    env=env,
                )
                logger.info(
                    f"The response of IncubationApi->cari_adm1_values_get: {api_response}\n"
                )
                logger.info(api_response)
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except Exception as e:
                logger.error(
                    f"Exception when calling IncubationApi->cari_adm1_values_get: {e}\n"
                )
                raise

    def get_cari_data(
        self,
        admin_level="admin0",
        country_iso3=None,
        survey_id=None,
        indicator_id=None,
        page=1,
    ):
        """ "
        Retrieves a paginated list of Admin0 or Admin1 CARI results based on the specified indicator, administrative code, and survey.

        Args:
            country_iso3 (str, optional): ISO3 code of the country for which to retrieve CARI results. If not provided, retrieves results for all countries.
            survey_id (str, optional): ID of the survey for which to retrieve CARI results. If not provided, retrieves results for all surveys.
            indicator_id (str, optional): ID of the indicator for which to retrieve  CARI results. If not provided, retrieves results for all indicators.
            page (int, optional): Page number for paginated results. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved Admin0 or Admin1 CARI results.

        Raises:
            ValueError: If admin_level is not "admin0" or "admin1".

        """

        if admin_level == "admin0" or admin_level == "admin1":
            if admin_level == "admin0":
                return self.get_cari_adm0(
                    country_iso3=country_iso3,
                    survey_id=survey_id,
                    indicator_id=indicator_id,
                    page=page,
                )
            elif admin_level == "admin1":
                return self.get_cari_adm1(
                    country_iso3=country_iso3,
                    survey_id=survey_id,
                    indicator_id=indicator_id,
                    page=page,
                )
        else:
            raise ValueError("admin_level must be either 'admin0' or 'admin1'")
