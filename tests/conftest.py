import json

import pytest

from data_bridges_knots import DataBridgesShapes


@pytest.fixture
def sample_survey_df():
    """Fixture providing a sample survey dataset"""
    client = DataBridgesShapes("data_bridges_api_config.yaml")
    df = client.get_household_survey(
        4872, "full"
    )  # FIXME: this should read from a static file
    return df


@pytest.fixture
def sample_xslform_df():
    """Fixture providing a sample questionnaire in XSLForm"""
    client = DataBridgesShapes("data_bridges_api_config.yaml")
    df = client.get_household_questionnaire(
        1883
    )  # FIXME: this should read from a static file
    return df


@pytest.fixture
def sample_list():
    """Fixture providing a sample list for testing."""
    return [1, 2, 3]


@pytest.fixture
def sample_values_labels_expected():
    with open("tests/static/get_values_labels_expected.json") as f:  # adjust path
        return json.load(f)
