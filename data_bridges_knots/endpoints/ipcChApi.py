import logging

import data_bridges_client
import pandas as pd
from datetime import datetime

logname = "data_bridges_api_calls.log"
logging.basicConfig(
    filename=logname,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


class IpcchApi:
    """
    This class is responsible for interacting with the IPC CH API to retrieve data related to IPC (Integrated Food Security Phase Classification) and equivalent historical peaks, latest peaks, most recent data, and WFP dashboard peaks.
    """

    def get_ipc_and_equivalent_historical_peaks(
        self,
        reference_year: int | None = None,
        iso3: str | None = None,
        page: int | None = 1,
    ) -> pd.DataFrame:
        """
        Retrieves a paginated list of historical IPCCH and Equivalent peaks data, optionally filtered by ISO3 country code.

        Args:
            reference_year (int, optional): The reference year for the data. If not provided, data for all years will be retrieved.
            iso3 (str, optional): The ISO3 country code to filter the data. If not provided, data for all countries will be retrieved.
            page (int, optional): The page number for paginated results. Defaults to 1.
            env (str, optional): The environment to use for the API call. Defaults to "prod".

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved IPCCH and Equivalent historical peaks data.

        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IpcchApi(api_client)
            env = self.env

        try:
            # Retrieves a paginated list of historical IPCCH and Equivalent peaks data, optionally filtered by ISO3 country code.
            api_response = api_instance.ipcch_ipcch_and_equivalent_historical_peaks_get(
                reference_year=reference_year, iso3=iso3, page=page, env=env
            )
            logger.info(
                "The response of IpcchApi->ipcch_ipcch_and_equivalent_historical_peaks_get:\n"
            )
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            return df

        except Exception as e:
            logger.error(
                "Exception when calling IpcchApi->ipcch_ipcch_and_equivalent_historical_peaks_get: %s\n"
                % e
            )
            raise e

    def get_ipc_and_equivalent_latest_peaks(
        self, iso3: str | None = None, page: int | None = 1
    ) -> pd.DataFrame:
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IpcchApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Retrieves a paginated list of the latest IPCCH and Equivalent peaks data, optionally filtered by ISO3 country code.
                api_response = api_instance.ipcch_ipcch_and_equivalent_latest_peaks_get(
                    iso3=iso3, page=page, env=env
                )
                logger.info(
                    "The response of IpcchApi->ipcch_ipcch_and_equivalent_latest_peaks_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling IpcchApi->ipcch_ipcch_and_equivalent_latest_peaks_get: %s\n"
                    % e
                )
                raise e

    def get_ipc_and_equivalent_most_recent(
        self, iso3: str | None = None, page: int | None = 1
    ) -> pd.DataFrame:
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IpcchApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Retrieves a paginated list of the most recent IPCCH and Equivalent data, optionally filtered by ISO3 country code.
                api_response = api_instance.ipcch_ipcch_and_equivalent_most_recent_get(
                    iso3=iso3, page=page, env=env
                )
                logger.info(
                    "The response of IpcchApi->ipcch_ipcch_and_equivalent_most_recent_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling IpcchApi->ipcch_ipcch_and_equivalent_most_recent_get: %s\n"
                    % e
                )
                raise e

    def get_ipc_and_equivalent_peaks_wfp_dashboard(
        self, iso3: str | None = None, page: int | None = 1
    ) -> pd.DataFrame:
        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IpcchApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Retrieves a paginated list of IPCCH and Equivalent Peaks data for the WFP Dashboard.
                api_response = (
                    api_instance.ipcch_ipcch_and_equivalent_peaks_wfp_dashboard_get(
                        iso3=iso3, page=page, env=env
                    )
                )
                logger.info(
                    "The response of IpcchApi->ipcch_ipcch_and_equivalent_peaks_wfp_dashboard_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling IpcchApi->ipcch_ipcch_and_equivalent_peaks_wfp_dashboard_get: %s\n"
                    % e
                )
                raise e

    #BUG: Requests seems to fail due to validation issues, API schema requires datetime but server expects string
    def get_ipc_historical_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        iso3: str | None = None,
        page: int | None = 1,
    ) -> pd.DataFrame:  

        # from_date = datetime.fromisoformat(from_date) #FIXME: is this required?
        # to_date = datetime.fromisoformat(to_date)

        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.IpcchApi(api_client)
            env = (
                self.env
            )  # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Retrieves a paginated list of IPCCH and Equivalent Historical Data.
                api_response = api_instance.ipcch_ipcch_historical_data_get(
                    from_date=from_date, to_date=to_date, iso3=iso3, page=page, env=env
                )
                logger.info(
                    "The response of IpcchApi->ipcch_ipcch_historical_data_get:\n"
                )
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                return df
            except Exception as e:
                logger.error(
                    "Exception when calling IpcchApi->ipcch_ipcch_historical_data_get: %s\n"
                    % e
                )
                raise e
