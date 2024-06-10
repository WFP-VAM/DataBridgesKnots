import time
import logging
from datetime import timedelta, date
import pandas as pd
import numpy as np
import yaml
from data_bridges_client.rest import ApiException
from data_bridges_client.token import WfpApiToken
import data_bridges_client


logname = "data_bridges_api_calls.log"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



class DataBridgesShapes:
    """
    Retrieves survey data using the specified configuration and access type.
    
    Args:
        survey_id (str): The ID of the survey to retrieve.
        access_type (str): The type of access to use for retrieving the survey data.
            Can be one of '', 'full', 'draft', 'official', or 'public'.
        page_size (int, optional): The number of items to retrieve per page. Defaults to 200.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved survey data.
    """


    def __init__(self, yaml_config_path, env='prod'):
        self.configuration = self.setup_configuration_and_authentication(yaml_config_path)
        self.env = env
        self.data = {}

    def __repr__(self):
        return "DataBridgesShapes(yamlpath='%s')" % self.configuration.host

    def __str__(self):
        return ("DataBridgesShapes(yamlpath='%s') \n\n Brought to you with <3 by SHAPES \n\n"
                % self.configuration.host)

    def setup_configuration_and_authentication(self, yaml_config_path):
        """Loads configuration from a YAML file and sets up authentication."""

        with open(yaml_config_path, "r") as yamlfile:
            databridges_config = yaml.load(yamlfile, Loader=yaml.FullLoader)

        key = databridges_config['KEY']
        secret = databridges_config['SECRET']
        scopes = databridges_config['SCOPES']
        version = databridges_config['VERSION']
        uri = "https://api.wfp.org/vam-data-bridges/"
        host = str(uri + version)
        
        logger.info("DataBridges API: %s", host)

        token = WfpApiToken(api_key=key, api_secret=secret)
        configuration = data_bridges_client.Configuration(
            host=host, access_token=token.refresh(scopes=scopes)
        )
        return configuration

    def get_household_survey(self, survey_id, access_type, page_size=600):
        """Retrieves survey data using the specified configuration and access type.

        Args:
            survey_id (str): The ID of the survey to retrieve.
            access_type (str): The type of access to use for retrieving the survey data.
                Can be one of '', 'full', 'draft', 'official', or 'public'.
            page_size (int, optional): The number of items to retrieve per page. Defaults to 200.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved survey data.
        """

        responses = []
        total_items = 1
        max_item = 0
        page = 0

        while total_items > max_item:
            page += 1
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.IncubationApi(api_client)
                env = self.env

                try:
                    logger.info(f"Calling get_household_survey for survey {survey_id}") 
                    # Select appropriate API call based on access_type
                    api_survey = {
                        '': api_instance.household_public_base_data_get,
                        'full': api_instance.household_full_data_get,
                        'draft': api_instance.household_draft_internal_base_data_get,
                        'official': api_instance.household_official_use_base_data_get,
                        'public': api_instance.household_public_base_data_get
                    }.get(access_type)(survey_id=survey_id, page=page, page_size=page_size, env=env)

                    logger.info("Fetching page %s", page)
                    logger.info("Items: %s", len(api_survey.items))
                    responses.extend(api_survey.items)
                    total_items = api_survey.total_items
                    max_item = len(api_survey.items) + max_item
                    time.sleep(1)

                except ApiException as e:
                    logger.error("Exception when calling Household data-> %s%s\n", access_type, e)
                    raise

        df = pd.DataFrame(responses)

        df.apply(lambda x: pd.to_numeric(x, errors='coerce', downcast='integer').fillna(9999).astype(np.int64 if x.dtype == 'int64' else x.dtype))
        df = df.replace({9999: None})
        return df

    def get_prices(self, country_iso3, survey_date, page_size=1000):
        """
        Fetches market price data for a given country and survey date.

        Args:
            country_iso3 (str): The ISO 3-letter country code.
            survey_date (str): The survey date in ISO format (e.g. '2022-01-01').
                If an empty string is provided, the function will fetch data starting from Jan 1, 1990.
            page_size (int, optional): The number of items to fetch per page. Defaults to 1000.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched market price data.
        """

        if survey_date != '':
            start_date = date.fromisoformat(survey_date) - timedelta(days=365)
        else:
            start_date = date.fromisocalendar(1990, 1, 1)
        responses = []
        total_items = 20
        max_item = 0
        page = 0
        while total_items > max_item:
            page += 1
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.MarketPricesApi(api_client)
                env = self.env

                try:
                    api_prices = api_instance.market_prices_price_monthly_get(
                        country_code=country_iso3, format='JSON', page=page, env=env, start_date=start_date
                    )
                    responses.extend(item.to_dict() for item in api_prices.items)
                    total_items = api_prices.total_items
                    logger.info("Fetching page %s", page)
                    max_item = page * page_size
                    time.sleep(1)
                except ApiException as e:
                    logger.error("Exception when calling Market price data->market_prices_price_monthly_get: %s\n", e)
                    raise
                
        df = pd.DataFrame(responses)
        df = df.replace({np.nan: None})
        return df

    def get_exchange_rates(self, country_iso3, page_size=1000):
        """
        Retrieves exchange rates for a given country ISO3 code from the Data Bridges API.

        Args:
            country_iso3 (str): The ISO3 country code for which to retrieve exchange rates.
            page_size (int, optional): The number of items to retrieve per page. Defaults to 1000.

        Returns:
            pandas.DataFrame: A DataFrame containing the exchange rate data.
        """

        responses = []
        total_items = 20
        max_item = 0
        page = 0
        while total_items > max_item:
            page += 1
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.CurrencyApi(api_client)
                env = self.env

                try:
                    api_exchange_rates = api_instance.currency_usd_indirect_quotation_get(
                        country_iso3=country_iso3, format='JSON', page=page, env=env
                    )
                    responses.extend(item.to_dict() for item in api_exchange_rates.items)
                    total_items = api_exchange_rates.total_items
                    logger.info("Fetching page %s", page)
                    max_item = page * page_size
                    time.sleep(1)
                except ApiException as e:
                    logger.error("Exception when calling Exchange rates data->household_full_data_get: %s\n", e)
                    raise
        df = pd.DataFrame(responses)
        df = df.replace({np.nan: None})
        return df
        
    
    def get_gorp(self, data_type, page=None):
        """
        Retrieves data from the Global Operational Response Plan (GORP) API.

        Args:
            data_type (str): The type of GORP data to retrieve. Can be one of 'country_latest', 'global_latest', 'latest', 'list', or 'regional_latest'.
            page (int, optional): The page number for paginated results. Defaults to None.
            env (str, optional): The environment to use. Can be 'prod' or 'dev'. Defaults to 'prod'.

        Returns:
            The requested GORP data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            gorp_api_instance = data_bridges_client.GorpApi(api_client)
            env = self.env

            responses = []

            try:
                if data_type == 'country_latest':
                    gorp_data =  gorp_api_instance.gorp_country_latest_get(env=env)
                elif data_type == 'global_latest':
                    gorp_data = gorp_api_instance.gorp_global_latest_get(env=env)
                elif data_type == 'latest':
                                         
                    gorp_data = gorp_api_instance.gorp_latest_get(page=page, env=env)
                elif data_type == 'list':
                    gorp_data = gorp_api_instance.gorp_list_get(page=page, env=env)
                elif data_type == 'regional_latest':
                    gorp_data =  gorp_api_instance.gorp_regional_latest_get(env=env)
                else:
                    raise ValueError(f"Invalid data_type: {data_type}")
            except ApiException as e:
                logger.error("Exception when calling Exchange rates data->household_full_data_get: %s\n", e)
                raise

            if "GorpGlobalApiDto" in gorp_data.__doc__:
                responses.extend(item for item in gorp_data)
            else:
                try:
                    responses.extend(item.to_dict() for item in gorp_data.items)
                except AttributeError:
                    responses.extend(item.to_dict() for item in gorp_data)
            
            df = pd.DataFrame(responses)
            df = df.replace({np.nan: None})
            return df
        
    def get_food_security(self, country_iso3=None, year=None, page=None, env='prod'):
        """
        Retrieves food security data from the Data Bridges API.

        Args:
            country_iso3 (str, optional): The ISO3 code of the country to retrieve data for. Defaults to None.
            year (int, optional): The year to retrieve data for. Defaults to None.
            page (int, optional): The page number for paginated results. Defaults to None.
            env (str, optional): The environment to use. Can be 'prod' or 'dev'. Defaults to 'prod'.

        Returns:
            The requested food security data.
        """
        responses =[]
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            food_security_api_instance = data_bridges_client.FoodSecurityApi(api_client)

            try:
                food_security_data = food_security_api_instance.food_security_list_get(
                    iso3=country_iso3,
                    year=year,
                    page=page,
                    env=env
                )
            except data_bridges_client.ApiException as e:
                logger.error(f"Exception when calling Food Security data: {e}")
                raise
            
            responses.extend(item.to_dict() for item in food_security_data.items)
            return pd.DataFrame(responses)

    def get_household_questionnaire(self, xls_form_id, env='prod', page_size=200):
        """
        This function fetches questionnaire data for a given form ID from the Data Bridges API.

        Args:
            form_id (int): The ID of the questionnaire form to retrieve data for.
            page_size (int, optional): The maximum number of items to retrieve per API call. Defaults to 200.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched questionnaire data.

        Raises:
            ApiException: If an error occurs while calling the Data Bridges API.
        """

        page = 0
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = self.env
            responses = []
            try:
                # Select appropriate API call based on access_type
                api_survey = api_instance.xls_forms_definition_get(xls_form_id=xls_form_id, env=env)
                page += 1
                try:
                    logger.info(f"Fetching page {page} from XLSForm definition")
                    responses.extend(item.to_dict() for item in api_survey.items)
                except AttributeError:
                    responses.extend(item.to_dict() for item in api_survey)
                time.sleep(1)

            except ApiException as e:
                logger.error("Exception when calling Household questionnaire-> %s%s\n", xls_form_id, e)
                raise

        df = pd.DataFrame(responses)
        df = df.replace({np.nan: None})
        
        questionnaire = pd.DataFrame(list(df.fields)[0])
        self.data[xls_form_id] = questionnaire
        return questionnaire

    def get_choice_list(self, xls_form_id):
        questionnaire = self.data[xls_form_id]
        choiceList = pd.json_normalize(questionnaire['choiceList']).dropna()
        choices = choiceList.explode('choices')
        return choices


if __name__ == "__main__":
    pass
