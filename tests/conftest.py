import json

import pandas as pd
import pytest


@pytest.fixture
def sample_survey_df():
    """Fixture providing a sample survey dataset"""
    return pd.read_csv("tests/static/test_df.csv")


@pytest.fixture
def sample_xslform_df():
    """Fixture providing a sample questionnaire in XSLForm"""
    return pd.read_csv("tests/static/test_xslform.csv")


@pytest.fixture
def sample_list():
    """Fixture providing a sample list for testing."""
    return [1, 2, 3]


@pytest.fixture
def sample_values_labels_expected():
    with open("tests/static/get_values_labels_expected.json") as f:  # adjust path
        return json.load(f)
