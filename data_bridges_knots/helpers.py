from typing import Dict, Optional

import json
from pathlib import Path

import pandas as pd


def get_value_labels(df):
    choiceList = pd.json_normalize(df["choiceList"])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(df["name"]).dropna()
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


def get_column_labels(df):
    labels_dict = {}

    for _, row in df.iterrows():
        name = row["name"]
        label = row["label"]
        if name in labels_dict:
            labels_dict[name].update(label)
        elif label == "":
            labels_dict[name] = name
        else:
            labels_dict[name] = label
    return labels_dict


# Map values if int
def map_value_labels(survey_data, questionnaire):
    survey_data = survey_data.convert_dtypes()
    choiceList = pd.json_normalize(questionnaire["choiceList"])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(questionnaire["name"]).dropna()
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

# Cache return value from _load_country_codes() into global variable
codes_mapping = None

def _load_country_codes() -> Dict[str, int]:
    """Load country codes mapping from JSON file.

    Returns:
        Dict[str, int]: Mapping of ISO3 codes to ADM0 codes

    Examples:
        >>> codes = _load_country_codes()
        >>> isinstance(codes, dict)
        True
    """
    global codes_mapping
    if codes_mapping is None:
        try:
            json_path = Path(__file__).parent / "country_list.json"
            with open(json_path, "r", encoding="utf-8") as f:
                country_list = json.load(f)

            codes_mapping = {
                country["iso3Alpha3"]: country["adm0Code"]
                for country in country_list
                if country.get("adm0Code") is not None
                and country.get("iso3Alpha3") is not None
            }
        except FileNotFoundError:
            raise FileNotFoundError(f"Country list file not found at {json_path}")

    return codes_mapping

def get_adm0_code(country_iso3: str) -> Optional[int]:
    """Get ADM0 code for a given ISO3 country code.

    Args:
        iso3 (str): ISO3 country code (e.g. 'AFG' for Afghanistan)

    Returns:
        Optional[int]: ADM0 code if found, None if not found

    Examples:
        >>> code = get_code("ETH")  # Ethiopia
        >>> isinstance(code, int)
        True
        >>> get_code("XXX") is None  # Invalid code
        True
    """

    if not isinstance(country_iso3, str):
        raise TypeError("iso3 must be a string")

    codes = _load_country_codes()
    return codes.get(country_iso3.upper())
