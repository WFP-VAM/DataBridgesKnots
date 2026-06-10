
from unittest.mock import MagicMock, patch
import data_bridges_client

import pytest
from dotenv import load_dotenv

from data_bridges_knots.client import (
    DataBridgesShapes,
    config_from_env,
)
from data_bridges_knots.endpoints.householdApi import get_household_survey


@pytest.fixture
def valid_config():
    load_dotenv()
    config = config_from_env()

    return config


@pytest.fixture
def client(valid_config):
    return DataBridgesShapes(valid_config)



from unittest.mock import MagicMock, patch
import pytest

from data_bridges_knots.endpoints.householdApi import get_household_survey



def test_get_household_full_data_success(client):
    mock_api_instance = MagicMock()
    mock_api_instance.household_full_data_get.return_value = {"data": ["ok"]}

    with patch(
        "data_bridges_knots.endpoints.householdApi.data_bridges_client.IncubationApi",
        return_value=mock_api_instance,
    ), patch(
        "data_bridges_knots.endpoints.householdApi.data_bridges_client.ApiClient"
    ) as mock_api_client:

        result = client.get_household_survey(
            api_key="test_key",
            survey_id=123,
            access_type="full",
        )

    assert result == {"data": ["ok"]}
    mock_api_instance.household_full_data_get.assert_called_once()
