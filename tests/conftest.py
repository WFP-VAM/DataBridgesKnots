import json

import pandas as pd
import pytest

from data_bridges_knots import DataBridgesShapes, config_from_env


@pytest.fixture
def sample_survey_df():
    """Fixture providing a sample survey dataset"""
    client = DataBridgesShapes(config_from_env())
    df = client.get_household_survey(
        4872, "full"
    )  # FIXME: this should read from a static file
    return df


@pytest.fixture
def sample_xlsform_df():
    """Fixture providing a sample questionnaire in xlsForm"""
    client = DataBridgesShapes(config_from_env())
    df = client.get_household_questionnaire(
        1883
    )  # FIXME: this should read from a static file
    return df


@pytest.fixture
def sample_xlsform_pkl():
    """Fixture providing a sample survey dataset"""
    return pd.read_pickle("tests/static/test_xlsform.pkl")


@pytest.fixture
def sample_list():
    """Fixture providing a sample list for testing."""
    return [1, 2, 3]


@pytest.fixture
def sample_values_labels_expected():
    with open(
        "tests/static/test_xlsform_value_labels_expected.json"
    ) as f:  # adjust path
        return json.load(f)

def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (API calls)",
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-integration"):
        return

    skip_integration = pytest.mark.skip(reason="need --run-integration option to run")

    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)

