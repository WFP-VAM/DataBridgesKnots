from typing import Dict
import pandas as pd
import json


def get_column_labels(xlsform_df: pd.DataFrame, format='dict') -> Dict:
    """Get column labels as Python dictionary, JSON or Pandas Dataframes."""
    labels_dict = {}

    for _, row in xlsform_df.iterrows():
        name = str(row["name"])
        label = str(row["label"])
        if name in labels_dict and len(name) > 0:
            labels_dict[name] = label
        elif label == "":
            labels_dict[name] = name
        else:
            labels_dict[name] = label
    if format == 'json':
        return json.dumps(labels_dict, indent=4)
    elif format == 'df':
        return pd.DataFrame.from_dict(labels_dict)
    
    return labels_dict

def get_value_labels(xlsform_df: pd.DataFrame) -> Dict:
    choiceList = pd.json_normalize(xlsform_df["choiceList"])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(xlsform_df["name"]).dropna()
    choices = choiceList.explode("choices")

    categories_dict = {}
    for _, row in choices.iterrows():
        name = row["name"]
        choice = row["choices"]
        if name in categories_dict:
            categories_dict[name].update({(choice["name"]): choice["label"]})
        else:
            categories_dict[name] = {(choice["name"]): choice["label"]}

    return categories_dict



# Map values if int
def map_value_labels(survey_df, xlsform_df):
    survey_data = survey_df.convert_dtypes()
    choiceList = pd.json_normalize(xlsform_df["choiceList"])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(xlsform_df["name"]).dropna()
    choices = choiceList.explode("choices")

    categories_dict = dict()
    for _, row in choices.iterrows():
        name = row["name"]
        choice = row["choices"]
        if name in categories_dict:
            categories_dict[name].update({(choice["name"]): choice["label"]})
        else:
            categories_dict[name] = {(choice["name"]): choice["label"]}

    # Map the categories to survey_data
    survey_data_value_labels = survey_data.copy()
    for col in survey_data_value_labels.columns:
        if col in categories_dict:
            category_dict = categories_dict[col]
            survey_data_value_labels[col] = survey_data_value_labels[col].apply(
                lambda x: category_dict.get(x, x)
            )

    return survey_data_value_labels


def as_numeric(df, col_list):
    for col in col_list:
        try:
            df[col] = (
                pd.to_numeric(df[col], errors="ignore").fillna(9999).astype("int64")
            )
        except ValueError:
            continue

    return df