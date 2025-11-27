import pandas as pd
from typing import Dict
from data_bridges_knots.labels import get_column_labels 


def test_sample_questionnaire(sample_xslform_df):
    assert isinstance(sample_xslform_df, pd.DataFrame)

def test_basic_labels():
    data = {
        "name": ["q1", "q2", "q3"],
        "label": ["Question 1", "Question 2", "Question 3"],
    }
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"q1": "Question 1", "q2": "Question 2", "q3": "Question 3"}
    assert result == expected


def test_empty_label():
    data = {"name": ["q1", "q2"], "label": ["", "Question 2"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"q1": "q1", "q2": "Question 2"}
    assert result == expected


def test_duplicate_names():
    data = {"name": ["q1", "q1", "q2"], "label": ["First", "Second", "Second Question"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    # The last occurrence should overwrite previous ones
    expected = {"q1": "Second", "q2": "Second Question"}
    assert result == expected


def test_empty_dataframe():
    df = pd.DataFrame(columns=["name", "label"])
    result = get_column_labels(df)
    assert result == {}


def test_name_empty_string():
    data = {"name": ["", "q2"], "label": ["Label for empty", "Label for q2"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"": "Label for empty", "q2": "Label for q2"}
    assert result == expected

def test_return_column_labels_as_df(sample_xslform_df):
    result = get_column_labels(sample_xslform_df, "df")
    assert isinstance(result, pd.DataFrame)

def test_return_column_labels_as_df(sample_xslform_df):
    result = get_column_labels(sample_xslform_df, "dict")
    assert isinstance(result, Dict)

# def test_get_columns_as_dict(sample_xslform_df):
#     result = get_column_labels(sample_xslform_df, "dict")
#     assert isinstance(result, Dict)