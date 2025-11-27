from typing import Dict

import pandas as pd

from data_bridges_knots.labels import get_column_labels, get_value_labels


def test_sample_questionnaire_df(sample_xslform_df):
    assert isinstance(sample_xslform_df, pd.DataFrame)


# % TESTS FOR GET_COLUMN_LABELS
def test_get_column_labels_basic_labels():
    data = {
        "name": ["q1", "q2", "q3"],
        "label": ["Question 1", "Question 2", "Question 3"],
    }
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"q1": "Question 1", "q2": "Question 2", "q3": "Question 3"}
    assert result == expected


def test_get_column_labels_empty_label():
    data = {"name": ["q1", "q2"], "label": ["", "Question 2"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"q1": "q1", "q2": "Question 2"}
    assert result == expected


def test_get_column_labels_duplicate_names():
    data = {"name": ["q1", "q1", "q2"], "label": ["First", "Second", "Second Question"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    # The last occurrence should overwrite previous ones
    expected = {"q1": "Second", "q2": "Second Question"}
    assert result == expected


def test_get_column_labels_empty_dataframe():
    df = pd.DataFrame(columns=["name", "label"])
    result = get_column_labels(df)
    assert result == {}


def test_get_column_labels_empty_string():
    data = {"name": ["", "q2"], "label": ["Label for empty", "Label for q2"]}
    df = pd.DataFrame(data)
    result = get_column_labels(df)
    expected = {"": "Label for empty", "q2": "Label for q2"}
    assert result == expected


def test_return_column_labels_as_df(sample_xslform_df):
    result = get_column_labels(sample_xslform_df, format="df")
    assert isinstance(result, pd.DataFrame)


def test_return_column_labels_as_dict(sample_xslform_df):
    result = get_column_labels(sample_xslform_df, format="dict")
    assert isinstance(result, Dict)


def test_return_column_labels_as_json(sample_xslform_df):
    result = get_column_labels(sample_xslform_df, format="json")
    assert isinstance(result, str)


# % TESTS FOR GET_VALUE_LABELS

# def test_return_value_labels_as_df(sample_xslform_df):
#     result = get_value_labels(sample_xslform_df, "df")
#     assert isinstance(result, pd.DataFrame)


def test_return_value_labels_as_dict(sample_xslform_df):
    result = get_value_labels(sample_xslform_df)
    assert isinstance(result, Dict)


# def test_return_value_labels_as_json(sample_xslform_df):
#     result = get_value_labels(sample_xslform_df, "json")
#     assert isinstance(result, str)
