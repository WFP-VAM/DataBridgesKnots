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

    def __init__(self, yaml_config_path, env='prod'):
        self.configuration = self.setup_configuration_and_authentication(yaml_config_path)
        self.data_bridges_api_key = self.setup_databridges_configuration(yaml_config_path)
        self.env = env
        self.xlsform = None

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
    
    def setup_databridges_configuration(self, yaml_config_path):
        """Loads configuration from a YAML file and sets up authentication."""
        with open(yaml_config_path, "r") as yamlfile:
            data_bridges_api_key = yaml.load(yamlfile, Loader=yaml.FullLoader)
        
        return data_bridges_api_key['DATABRIDGES_API_KEY']

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

        
    def get_food_security_list(self, iso3=None, year=None, page=1):
        """
        Retrieves food security data from the Data Bridges API.

        Args:
            iso3 (str, optional): The country ISO3 code.
            year (int, optional): The year to retrieve data for.
            page (int, optional): Page number for paged results. Defaults to 1.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved food security data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            food_security_api_instance = data_bridges_client.FoodSecurityApi(api_client)
            env = self.env

            try:
                api_response = food_security_api_instance.food_security_list_get(
                    iso3=iso3,
                    year=year,
                    page=page,
                    env=env
                )
                logger.info("Successfully retrieved food security data")
                
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling FoodSecurityApi->food_security_list_get: {e}")
                raise


    
    def get_commodities_list(self, country_code=None, commodity_name=None, commodity_id=0, page=1, format='json'):
        """
        Retrieves the detailed list of commodities available in the DataBridges platform.

        Args:
            country_code (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_name (str, optional): The name, even partial and case insensitive, of a commodity.
            commodity_id (int, optional): The exact ID of a commodity. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved commodity data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommoditiesApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodities_list_get(
                    country_code=country_code,
                    commodity_name=commodity_name,
                    commodity_id=commodity_id,
                    page=page,
                    format=format,
                    env=env
                )
                logger.info("Successfully retrieved commodities list")
                
                # Convert the response to a DataFrame
                if hasattr(api_response, 'items'):
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                else:
                    df = pd.DataFrame([api_response.to_dict()])
                
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling CommoditiesApi->commodities_list_get: {e}")
            raise

    def get_commodity_units_conversion_list(self, country_code=None, commodity_id=0, from_unit_id=0, to_unit_id=0, page=1, format='json'):
        """
        Retrieves conversion factors to Kilogram or Litres for each convertible unit of measure.

        Args:
            country_code (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_id (int, optional): The exact ID of a Commodity, as found in /Commodities/List. Defaults to 0.
            from_unit_id (int, optional): The exact ID of the original unit of measure of the price of a commodity. Defaults to 0.
            to_unit_id (int, optional): The exact ID of the converted unit of measure of the price of a commodity. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved conversion factors.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommodityUnitsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodity_units_conversion_list_get(
                    country_code=country_code,
                    commodity_id=commodity_id,
                    from_unit_id=from_unit_id,
                    to_unit_id=to_unit_id,
                    page=page,
                    format=format,
                    env=env
                )
                logger.info("Successfully retrieved commodity units conversion list")
                
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling CommodityUnitsApi->commodity_units_conversion_list_get: {e}")
                raise

    def get_commodity_units_list(self, country_code=None, commodity_unit_name=None, commodity_unit_id=0, page=1, format='json'):
        """
        Retrieves the detailed list of the unit of measure available in DataBridges platform.

        Args:
            country_code (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            commodity_unit_name (str, optional): The name, even partial and case insensitive, of a commodity unit.
            commodity_unit_id (int, optional): The exact ID of a commodity unit. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved commodity units data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CommodityUnitsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.commodity_units_list_get(
                    country_code=country_code,
                    commodity_unit_name=commodity_unit_name,
                    commodity_unit_id=commodity_unit_id,
                    page=page,
                    format=format,
                    env=env
                )
                logger.info("Successfully retrieved commodity units list")
                
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling CommodityUnitsApi->commodity_units_list_get: {e}")
                raise

    def get_currency_list(self, country_code=None, currency_name=None, currency_id=0, page=1, format='json'):
        """
        Returns the list of currencies available in the internal VAM database, with Currency 3-letter code, matching with ISO 4217.

        Args:
            country_code (str, optional): The code to identify the country. It can be an ISO-3166 Alpha 3 code or the VAM internal admin0code.
            currency_name (str, optional): Currency 3-letter code, matching with ISO 4217.
            currency_id (int, optional): Unique code to identify the currency in internal VAM currencies. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

        Returns:
            pandas.DataFrame: A DataFrame containing the retrieved currency data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.CurrencyApi(api_client)
            env = self.env

            try:
                api_response = api_instance.currency_list_get(
                    country_code=country_code,
                    currency_name=currency_name,
                    currency_id=currency_id,
                    page=page,
                    format=format,
                    env=env
                )
                logger.info("Successfully retrieved currency list")
                
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling CurrencyApi->currency_list_get: {e}")
                raise

    def get_usd_indirect_quotation(self, country_iso3='', currency_name='', page=1, format='json'):
        """
        Returns the value of the Exchange rates from Trading Economics, for official rates, and DataViz for unofficial rates.

        Args:
            country_iso3 (str, optional): The code to identify the country. Must be a ISO-3166 Alpha 3 code. Defaults to ''.
            currency_name (str, optional): The ISO3 code for the currency, based on ISO4217. Defaults to ''.
            page (int, optional): Page number for paged results. Defaults to 1.
            format (str, optional): Output format: 'json' or 'csv'. Defaults to 'json'.

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
                    env=env
                )
                logger.info("Successfully retrieved USD indirect quotation data")
                
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling CurrencyApi->currency_usd_indirect_quotation_get: {e}")
                raise

    # FIXME: JSON response 
    def get_economic_indicator_list(self, page=1, indicator_name='', iso3='', format='json'):
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
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.EconomicDataApi(api_client)

            try:
                # Returns the lists of indicators.
                api_response = api_instance.economic_data_indicator_list_get(page=page, indicator_name=indicator_name, iso3=iso3, format=format, env=self.env)
                print("The response of EconomicDataApi->economic_data_indicator_list_get:\n")
                return api_response
            except Exception as e:
                print("Exception when calling EconomicDataApi->economic_data_indicator_list_get: %s\n" % e)

    # BUG: Unsupported content type: 'application/geo+json
    def get_market_geojson_list(self, adm0code=None):
                # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.MarketsApi(api_client)

            try:
                # Provide a list of geo referenced markets in a specific country
                api_response = api_instance.markets_geo_json_list_get(adm0code=adm0code, env=self.env)
                print("The response of MarketsApi->markets_geo_json_list_get:\n")
                return api_response
            except Exception as e:
                print("Exception when calling MarketsApi->markets_geo_json_list_get: %s\n" % e)

    def get_markets_list(self, country_code=None, page=1):
        # Enter a context with an instance of the API client
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = data_bridges_client.MarketsApi(api_client)
            format = 'json' # str | Output format: [JSON|CSV] Json is the default value (optional) (default to 'json')
            env = self.env # str | Environment.   * `prod` - api.vam.wfp.org   * `dev` - dev.api.vam.wfp.org (optional)

            try:
                # Get a complete list of markets in a country
                api_response = api_instance.markets_list_get(country_code=country_code, page=page, format=format, env=env)
                print("The response of MarketsApi->markets_list_get:\n")
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except Exception as e:
                print("Exception when calling MarketsApi->markets_list_get: %s\n" % e)

    # FIXME: JSON response
    def get_markets_as_csv(self, adm0code=None, local_names=False):
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.MarketsApi(api_client)
            local_names = False # bool | If true the name of markets and regions will be localized if available (optional) (default to False)

            try:
                # Get a complete list of markets in a country
                api_response = api_instance.markets_markets_as_csv_get(adm0code=adm0code, local_names=local_names, env=self.env)
                logger.info("The response of MarketsApi->markets_markets_as_csv_get:\n")
                return api_response
            except Exception as e:
                logger.error("Exception when calling MarketsApi->markets_markets_as_csv_get: %s\n" % e)

    def get_nearby_markets(self, adm0code=None, lat=None, lng=None):
        """
        Find markets near a given location by longitude and latitude within a 15Km distance.

        Args:
            adm0code (int, optional): Code for the country as retrieved from https://api.vam.wfp.org/geodata/CountriesInRegion.
            lat (float, optional): Latitude of the point that will be used to search for existing nearby markets.
            lng (float, optional): Longitude of the point that will be used to search for existing nearby markets.

        Returns:
            pandas.DataFrame: A DataFrame containing the nearby markets data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.MarketsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.markets_nearby_markets_get(adm0code=adm0code, lat=lat, lng=lng, env=env)
                logger.info("Successfully retrieved nearby markets")
                df = pd.DataFrame([item.to_dict() for item in api_response])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(f"Exception when calling MarketsApi->markets_nearby_markets_get: {e}")
                raise

    def get_gorp(self, data_type, page=None):
        """
        Retrieves data from the Global Operational Response Plan (GORP) API.

        Args:
            data_type (str): The type of GORP data to retrieve. Can be one of 'country_latest', 'global_latest', 'latest', 'list', or 'regional_latest'.
            page (int, optional): The page number for paginated results. Required for 'latest' and 'list' data types.

        Returns:
            pandas.DataFrame: A DataFrame containing the requested GORP data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            gorp_api_instance = data_bridges_client.GorpApi(api_client)
            env = self.env

            try:
                if data_type == 'country_latest':
                    gorp_data = gorp_api_instance.gorp_country_latest_get(env=env)
                elif data_type == 'global_latest':
                    gorp_data = gorp_api_instance.gorp_global_latest_get(env=env)
                elif data_type == 'latest':
                    gorp_data = gorp_api_instance.gorp_latest_get(page=page, env=env)
                elif data_type == 'list':
                    gorp_data = gorp_api_instance.gorp_list_get(page=page, env=env)
                elif data_type == 'regional_latest':
                    gorp_data = gorp_api_instance.gorp_regional_latest_get(env=env)
                else:
                    raise ValueError(f"Invalid data_type: {data_type}")

                logger.info(f"Successfully retrieved GORP data for type: {data_type}")
                
                if isinstance(gorp_data, list):
                    df = pd.DataFrame([item.to_dict() for item in gorp_data])
                elif hasattr(gorp_data, 'items'):
                    df = pd.DataFrame([item.to_dict() for item in gorp_data.items])
                else:
                    df = pd.DataFrame([gorp_data.to_dict()])
                
                df = df.replace({np.nan: None})
                return df

            except ApiException as e:
                logger.error(f"Exception when calling GorpApi->{data_type}: {e}")
            raise

    def get_household_survey(self, survey_id, access_type, page_size=600):
        """Retrieves survey data using the specified configuration and access type.

        Args:
            survey_id (str): The ID of the survey to retrieve.
            access_type (str): The type of access to use for retrieving the survey data.
                Can be one of 'full', 'draft', 'official', or 'public'.
            page_size (int, optional): The number of items to retrieve per page. Defaults to 600.

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
                    api_call = {
                        'full': api_instance.household_full_data_get,
                        'draft': api_instance.household_draft_internal_base_data_get,
                        'official': api_instance.household_official_use_base_data_get,
                        'public': api_instance.household_public_base_data_get
                    }.get(access_type)

                    if access_type in ['full', 'draft']:
                        api_survey = api_call(self.data_bridges_api_key, survey_id=survey_id, page=page, page_size=page_size, env=env)
                    else:
                        api_survey = api_call(survey_id=survey_id, page=page, page_size=page_size, env=env)

                    logger.info(f"Fetching page {page}")
                    logger.info(f"Items: {len(api_survey.items)}")
                    responses.extend(api_survey.items)
                    total_items = api_survey.total_items
                    max_item = len(api_survey.items) + max_item
                    time.sleep(1)

                except ApiException as e:
                    logger.error(f"Exception when calling Household data-> {access_type}{e}")
                    raise

        df = pd.DataFrame(responses)
        return df


    def get_household_surveys(self, adm0_code=None, page=1, start_date=None, end_date=None, survey_id=None):
        """
        Retrieve Survey IDs, their corresponding XLS Form IDs, and Base XLS Form of all household surveys conducted in a country.

        Args:
            adm0_code (int, optional): Code for the country. Defaults to 0.
            page (int, optional): Page number for paged results. Defaults to 1.
            start_date (datetime, optional): Starting date for the range in which data was collected.
            end_date (datetime, optional): Ending date for the range in which data was collected.
            survey_id (int, optional): Specific survey ID to retrieve.

        Returns:
            pandas.DataFrame: A DataFrame containing the survey information.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = self.env

            try:
                api_response = api_instance.household_surveys_get(
                    adm0_code=adm0_code, 
                    page=page, 
                    start_date=start_date, 
                    end_date=end_date, 
                    survey_id=survey_id, 
                    env=env
                )
                logger.info("Successfully retrieved household surveys")
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(f"Exception when calling IncubationApi->household_surveys_get: {e}")
                raise

    def get_household_xslform_definition(self, xls_form_id):
        """
        Get a complete set of XLS Form definitions of a given XLS Form ID.

        Args:
            xls_form_id (int): The ID of the questionnaire form to retrieve data for.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched questionnaire data.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = self.env

            try:
                api_response = api_instance.xls_forms_definition_get(xls_form_id=xls_form_id, env=env)
                logger.info(f"Successfully retrieved XLS Form definition for ID: {xls_form_id}")
                self.xlsform = pd.DataFrame([item.to_dict() for item in api_response])
                return self.xlsform

            except ApiException as e:
                logger.error(f"Exception when calling IncubationApi->xls_forms_definition_get: {e}")
                raise

    def get_household_questionnaire(self, xls_form_id):
        if self.xlsform is None:
            self.xlsform = self.get_household_xslform_definition(xls_form_id)
        return pd.DataFrame(list(self.xlsform.fields)[0])
            
    def get_choice_list(self, xls_form_id):
        questionnaire = self.get_household_questionnaire(xls_form_id)
    
        choiceList = pd.json_normalize(questionnaire['choiceList']).dropna()
        choices = choiceList.explode('choices')
        choices['value'] = choices['choices'].apply(lambda x: x['name'])
        choices['label'] = choices['choices'].apply(lambda x: x['label'])
        return choices[['name', 'value', 'label']]

    # FIXME: Get scopes for AIMS then  test the following function
    def get_aims_analysis_rounds(self, adm0_code):
        """
        Download all analysis rounds for AIMS (Asset Impact Monitoring System) data.

        Args:
            adm0_code (int): The country adm0Code.

        Returns:
            bytes: The downloaded data as bytes.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = self.env

            try:
                api_response = api_instance.aims_download_all_analysis_rounds_get(adm0_code=adm0_code, env=env)
                logger.info(f"Successfully downloaded AIMS analysis rounds for adm0Code: {adm0_code}")
                return api_response
            except ApiException as e:
                logger.error(f"Exception when calling IncubationApi->aims_download_all_analysis_rounds_get: {e}")
                raise

    # FIXME: Get scopes for AIMS then  test the following function
    def get_aims_polygon_files(self, adm0_code):
        """
        Download polygon files for Landscape Impact Assessment (LIA) assets.

        Args:
            adm0_code (int): The country adm0Code.

        Returns:
            bytes: The downloaded polygon files as bytes.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.IncubationApi(api_client)
            env = self.env

            try:
                api_response = api_instance.aims_download_polygon_files_get(adm0_code=adm0_code, env=env)
                logger.info(f"Successfully downloaded AIMS polygon files for adm0Code: {adm0_code}")
                return api_response
            except ApiException as e:
                logger.error(f"Exception when calling IncubationApi->aims_download_polygon_files_get: {e}")
                raise

    def get_mfi_surveys_base_data(self, survey_id=None, page=1, page_size=20):
        """
        Get data that includes the core Market Functionality Index (MFI) fields only by Survey ID.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.SurveysApi(api_client)
            env = self.env

            try:
                api_response = api_instance.m_fi_surveys_base_data_get(
                    survey_id=survey_id, page=page, page_size=page_size, env=env
                )
                logger.info("Successfully retrieved MFI surveys base data")

                df = pd.DataFrame(api_response.items)
                return df
            except ApiException as e:
                logger.error(f"Exception when calling SurveysApi->m_fi_surveys_base_data_get: {e}")
            raise

    def get_mfi_surveys_full_data(self, survey_id=None, page=1, page_size=20):
        """
        Get a full dataset that includes all the fields included in the survey in addition to the core Market Functionality Index (MFI) fields by Survey ID.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.SurveysApi(api_client)
            env = self.env
            try:
                api_response = api_instance.m_fi_surveys_full_data_get(
                    survey_id=survey_id, format='json', page=page, page_size=page_size, env=env
                )
                logger.info("Successfully retrieved MFI surveys full data")
                df = pd.DataFrame(api_response.items)
                return df
            except ApiException as e:
                logger.error(f"Exception when calling SurveysApi->m_fi_surveys_full_data_get: {e}")
                raise

    def get_mfi_surveys(self, adm0_code=0, page=1, start_date=None, end_date=None):
        """
        Retrieve Survey IDs, their corresponding XLS Form IDs, and Base XLS Form of all MFI surveys conducted in a country.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.SurveysApi(api_client)
            env = self.env

            try:
                api_response = api_instance.m_fi_surveys_get(
                    adm0_code=adm0_code, page=page, start_date=start_date, end_date=end_date, env=env
                )
                logger.info("Successfully retrieved MFI surveys list")
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(f"Exception when calling SurveysApi->m_fi_surveys_get: {e}")
                raise

    def get_mfi_surveys_processed_data(self, survey_id=None, page=1, page_size=20, format='json', start_date=None, end_date=None, adm0_codes=None, market_id=None, survey_type=None):
        """
        Get MFI processed data in long format.
        """
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.SurveysApi(api_client)
            env = self.env

            try:
                api_response = api_instance.m_fi_surveys_processed_data_get(
                    survey_id=survey_id, page=page, page_size=page_size, format=format,
                    start_date=start_date, end_date=end_date, adm0_codes=adm0_codes,
                    market_id=market_id, survey_type=survey_type, env=env
                )
                logger.info("Successfully retrieved MFI surveys processed data")
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(f"Exception when calling SurveysApi->m_fi_surveys_processed_data_get: {e}")
                raise

        # TODO: Get the scope and test these functions
        def get_rpme_base_data(self, survey_id=None, page=1, page_size=20):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_base_data_get(survey_id=survey_id, page=page, page_size=page_size, env=env)
                    logger.info("Successfully retrieved RPME base data")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(f"Exception when calling RpmeApi->rpme_base_data_get: {e}")
                    raise

        # TODO: Get the scope and test these functions
        def get_rpme_full_data(self, survey_id=None, format='json', page=1, page_size=20):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_full_data_get(survey_id=survey_id, format=format, page=page, page_size=page_size, env=env)
                    logger.info("Successfully retrieved RPME full data")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(f"Exception when calling RpmeApi->rpme_full_data_get: {e}")
                    raise
        # TODO: Get the scope and test these functions
        def get_rpme_output_values(self, page=1, adm0_code=None, survey_id=None, shop_id=None, market_id=None, adm0_code_dots=''):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_output_values_get(page=page, adm0_code=adm0_code, survey_id=survey_id, 
                                                                    shop_id=shop_id, market_id=market_id, adm0_code_dots=adm0_code_dots, env=env)
                    logger.info("Successfully retrieved RPME output values")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(f"Exception when calling RpmeApi->rpme_output_values_get: {e}")
                    raise
        # TODO: Get the scope and test these functions
        def get_rpme_surveys(self, adm0_code=0, page=1, start_date=None, end_date=None):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_surveys_get(adm0_code=adm0_code, page=page, start_date=start_date, end_date=end_date, env=env)
                    logger.info("Successfully retrieved RPME surveys")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(f"Exception when calling RpmeApi->rpme_surveys_get: {e}")
                    raise
        # TODO: Get the scope and test these functions
        def get_rpme_variables(self, page=1):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
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
        def get_rpme_xls_forms(self, adm0_code=0, page=1, start_date=None, end_date=None):
            with data_bridges_client.ApiClient(self.configuration) as api_client:
                api_instance = data_bridges_client.RpmeApi(api_client)
                env = self.env

                try:
                    api_response = api_instance.rpme_xls_forms_get(adm0_code=adm0_code, page=page, start_date=start_date, end_date=end_date, env=env)
                    logger.info("Successfully retrieved RPME XLS forms")
                    df = pd.DataFrame([item.to_dict() for item in api_response.items])
                    df = df.replace({np.nan: None})
                    return df
                except ApiException as e:
                    logger.error(f"Exception when calling RpmeApi->rpme_xls_forms_get: {e}")
                    raise

        # Add this function to the DataBridgesShapes class

    def get_mfi_xls_forms(self, adm0_code=0, page=1, start_date=None, end_date=None):
        with data_bridges_client.ApiClient(self.configuration) as api_client:
            api_instance = data_bridges_client.XlsFormsApi(api_client)
            env = self.env

            try:
                api_response = api_instance.m_fi_xls_forms_get(adm0_code=adm0_code, page=page, start_date=start_date, end_date=end_date, env=env)
                logger.info("Successfully retrieved MFI XLS forms")
                df = pd.DataFrame([item.to_dict() for item in api_response.items])
                df = df.replace({np.nan: None})
                return df
            except ApiException as e:
                logger.error(f"Exception when calling XlsFormsApi->m_fi_xls_forms_get: {e}")
            raise

    

if __name__ == "__main__":
    import yaml
    # FOR TESTING
    CONFIG_PATH = r"data_bridges_api_config.yaml"

    client = DataBridgesShapes(CONFIG_PATH)

    # FIXME: JSON Response + printing instead of logging
    # economic_indicator_list = client.get_economic_indicator_list(page=1, indicator_name='', iso3='', format='json')

    # BUG: Error: Unsupported content type application/geo+json
    # markets_geo_json = client.get_market_geojson_list(adm0code=56)

    # FIXME: Get scopes for AIMS then  test the following function
    # # Get AIMS analysis rounds
    # aims_data = client.get_aims_analysis_rounds(adm0_code=1)
    # print("\nAIMS Analysis Rounds Data:")
    # print(f"Downloaded {len(aims_data)} bytes")

    # FIXME: Get scopes for AIMS then  test the following function
    # # Get AIMS polygon files
    # polygon_files = client.get_aims_polygon_files(adm0_code=1)
    # print("\nAIMS Polygon Files:")
    # print(f"Downloaded {len(polygon_files)} bytes")

    # FIXME: Get scopes for RPME then  test the following function
    # Get RPME base data
    # rpme_base_data = client.get_rpme_base_data(survey_id=123, page=1, page_size=50)

    # FIXME: Get scopes for RPME then  test the following function
    # # Get RPME full data
    # rpme_full_data = client.get_rpme_full_data(survey_id=123, format='json', page=1, page_size=50)

    # FIXME: Get scopes for RPME then  test the following function
    # # Get RPME output values
    # rpme_output_values = client.get_rpme_output_values(page=1, adm0_code=456, survey_id=123)

    # FIXME: Get scopes for RPME then  test the following function
    # # Get RPME surveys
    # rpme_surveys = client.get_rpme_surveys(adm0_code=456, page=1, start_date='2023-01-01', end_date='2023-12-31')

    # FIXME: Get scopes for RPME then  test the following function
    # # Get RPME variables
    # rpme_variables = client.get_rpme_variables(page=1)

    # FIXME: Get scopes for RPME then  test the following function
    # # Get RPME XLS forms
    # rpme_xls_forms = client.get_rpme_xls_forms(adm0_code=456, page=1, start_date='2023-01-01', end_date='2023-12-31')

    mfi_xls_forms = client.get_mfi_xls_forms(page=1, start_date='2023-01-01', end_date='2023-12-31')

