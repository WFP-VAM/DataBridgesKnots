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


def get_household_survey(
    self, survey_id: int, access_type: str, page_size: Optional[int] = 600, **kwargs
) -> pd.DataFrame:
    """Retrieves household survey data using the specified access type.

    Args:
        survey_id (int): The ID of the survey to retrieve.
        access_type (str): The type of access to use. Must be one of:
            - 'draft': Draft internal base data (requires API key)
            - 'full': Complete survey data (requires API key). Data is returned as inserted by the country office and it might contain PII and unstandardized fields.
            - 'official': Official use base data. Only data mapped against the standards is returned.
            - 'public': Public base data
        page_size (int, optional): Number of items per page. Defaults to 600.
        apply_mapping (bool, optional): Whether to apply standardized column name mapping to the full data. Only applicable when access_type is 'full'. Defaults to False.
        full_data (bool, optional): Whether to return full data to 'full' data access type. Only applicable when access_type is 'full'. Defaults to True.
    
    Returns:
        pd.DataFrame: DataFrame containing survey data with columns specific to the
            access type and survey structure

    Raises:
        KeyError: If access_type is not one of the allowed values
        ApiException: If there's an error accessing the API

    Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> # Get full, unmapped survey data
        >>> full_data = client.get_household_survey(3094, "full", apply_mapping=True)
        >>> # Get standard data for official use (no PII)
        >>> official_data = client.get_household_survey(3094, "official")

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
                    "full": api_instance.household_full_data_get,
                    "draft": api_instance.household_draft_internal_base_data_get,
                    "official": api_instance.household_official_use_base_data_get,
                    "public": api_instance.household_public_base_data_get,
                }.get(access_type)

                if access_type == "full":
                    apply_mapping = kwargs.get("apply_mapping", False)
                    full_data = kwargs.get("full_data", True)
                    try:
                        api_survey = api_call(
                            self.data_bridges_api_key,
                            survey_id=survey_id,
                            page=page,
                            page_size=page_size,
                            env=env,
                            apply_mapping=apply_mapping,
                            full_data=full_data,
                        )
                    except ApiException as e:
                        logger.error(
                            f"API key required when calling Household data-> '{access_type}': {e}"
                        )
                        raise
                elif access_type == "draft":
                    try:
                        api_survey = api_call(
                            self.data_bridges_api_key,
                            survey_id=survey_id,
                            page=page,
                            page_size=page_size,
                            env=env,
                        )
                    except ApiException as e:
                        logger.error(
                            f"API key required when calling Household data-> '{access_type}': {e}"
                        )
                        raise
                else:
                    api_survey = api_call(
                        survey_id=survey_id, page=page, page_size=page_size, env=env
                    )

                logger.info(f"Fetching page {page}")
                logger.info(f"Items: {len(api_survey.items)}")
                responses.extend(api_survey.items)
                total_items = api_survey.total_items
                max_item = len(api_survey.items) + max_item
                time.sleep(1)

            except ApiException as e:
                logger.error(
                    f"Exception when calling Household data-> {access_type}{e}"
                )
                raise

    df = pd.DataFrame(responses)
    return df


def get_household_surveys_list(
    self,
    country_iso3: Optional[int] = None,
    page: Optional[int] = 1,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    survey_id: Optional[int] = None,
) -> pd.DataFrame:
    """Retrieves a list of household surveys for a country with their metadata.

    Args:
        country_iso3 (str, optional): ISO3 Country code
        page (int, optional): Page number for paginated results. Defaults to 1
        start_date (str, optional): Start date filter in ISO format (YYYY-MM-DD)
        end_date (str, optional): End date filter in ISO format (YYYY-MM-DD)
        survey_id (int, optional): Specific survey ID to retrieve

    Returns:
        pd.DataFrame: DataFrame containing survey metadata with columns:
            - survey_id: Unique identifier for the survey
            - xls_form_id: ID of the questionnaire form used
            - title: Survey title
            - country: Country name
            - start_date: Survey start date
            - end_date: Survey end date
            And other metadata fields

    Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> # Get all surveys for a country
        >>> surveys = client.get_household_surveys_list(country_iso3="COG")
        >>> # Get surveys within date range
        >>> surveys = client.get_household_surveys_list(
        ...     country_iso3="COG",
        ...     start_date="2024-01-01",
        ...     end_date="2024-12-31"
        ... )

    Raises:
        ApiException: If there's an error accessing the API
    """

    adm0code = get_adm0_code(country_iso3) if country_iso3 else None

    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.IncubationApi(api_client)
        env = self.env

        try:
            api_response = api_instance.household_surveys_get(
                adm0_code=adm0code,
                page=page,
                start_date=start_date,
                end_date=end_date,
                survey_id=survey_id,
                env=env,
            )
            logger.info("Successfully retrieved household surveys")
            df = pd.DataFrame([item.to_dict() for item in api_response.items])
            df = df.replace({np.nan: None})
            return df
        except ApiException as e:
            logger.error(
                f"Exception when calling IncubationApi->household_surveys_get: {e}"
            )
            raise


def get_household_xlsform_definition(self, xls_form_id: int) -> pd.DataFrame:
    """Retrieves the complete XLS Form definition for a questionnaire.

    Args:
        xls_form_id (int): The ID of the questionnaire form to retrieve

    Returns:
        pd.DataFrame: DataFrame containing the form definition with columns:
            - fields: List of field definitions
            - choices: Available choices for select questions
            - settings: Form settings
            And other form structure information

    Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> # Get form definition
        >>> form_def = client.get_household_xlsform_definition(2067)
        >>> # Access form fields
        >>> fields = form_def['fields'].iloc[0]

    Raises:
        ApiException: If there's an error accessing the API
    """
    with data_bridges_client.ApiClient(self.configuration) as api_client:
        api_instance = data_bridges_client.IncubationApi(api_client)
        env = self.env

        try:
            api_response = api_instance.xls_forms_definition_get(
                xls_form_id=xls_form_id, env=env
            )
            logger.info(
                f"Successfully retrieved XLS Form definition for ID: {xls_form_id}"
            )
            self.xlsform = pd.DataFrame([item.to_dict() for item in api_response])
            return self.xlsform

        except ApiException as e:
            logger.error(
                f"Exception when calling IncubationApi->xls_forms_definition_get: {e}"
            )
            raise


def get_household_questionnaire(self, xls_form_id: int) -> pd.DataFrame:
    """Extracts the questionnaire structure from an XLS Form definition.

    Args:
        xls_form_id (int): The ID of the questionnaire form to process

    Returns:
        pd.DataFrame: DataFrame containing the questionnaire structure with
            one row per field in the form

    Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> questionnaire = client.get_household_questionnaire(2075)
    """
    if self.xlsform is None:
        self.xlsform = self.get_household_xlsform_definition(xls_form_id)
    return pd.DataFrame(list(self.xlsform.fields)[0])


def get_choice_list(self, xls_form_id: int) -> pd.DataFrame:
    """Extracts choice lists from a questionnaire form definition.

    Args:
        xls_form_id (int): The ID of the questionnaire form to process

    Returns:
        pd.DataFrame: DataFrame containing choice lists with columns:
            - name: Name of the choice list
            - value: Choice value/code
            - label: Human-readable choice label

    Examples:
        >>> client = DataBridgesKnots("data_bridges_api_config.yaml")
        >>> choices = client.get_choice_list(123)
    """
    questionnaire = self.get_household_questionnaire(xls_form_id)

    choiceList = pd.json_normalize(questionnaire["choiceList"]).dropna()
    choices = choiceList.explode("choices")
    choices["value"] = choices["choices"].apply(lambda x: x["name"])
    choices["label"] = choices["choices"].apply(lambda x: x["label"])
    return choices[["name", "value", "label"]]
