import pandas as pd
import pytest


@pytest.fixture
def sample_survey_df():
    """Fixture providing a sample survey dataset"""
    return pd.read_csv("tests/static/test_df.csv")


@pytest.fixture
def sample_xslform_df():
    """Fixture providing a sample questionnaire in XSLForm"""
    return pd.read_csv("static/test_xlsform.csv")


@pytest.fixture
def sample_list():
    """Fixture providing a sample list for testing."""
    return [1, 2, 3]
