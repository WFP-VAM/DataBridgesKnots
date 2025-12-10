from typing import Optional, Union

import json

import pandas as pd


def get_variable_labels(
    xlsform_df: pd.DataFrame, format: str = "dict"
) -> Union[dict[str, str], str, pd.DataFrame]:
    """
    Build a mapping between variable name and variable labels from a DataBridges XLSForm and return it in
    the desired format.

    Empty labels default to the corresponding name. For duplicate names, the
    latest occurrence overrides earlier values.

    Args:
        xlsform_df (pandas.DataFrame): DataFrame with at least ``"name"`` and ``"label"`` columns.
        format (str, optional): One of ``"dict"``, ``"json"``, or ``"df"``.
        Defaults to ``"dict"``.
        - ``"dict"``: returns ``dict[str, str]``.
        - ``"json"``: returns a JSON-formatted ``str``.
        - ``"df"``: returns a ``pandas.DataFrame`` with columns
            ``["colName", "label"]``.

    Returns:
        dict | str | pandas.DataFrame: Labels mapping in the requested format.

    Raises:
        KeyError: If required columns are missing.
        ValueError: If ``format`` is not one of ``{"dict", "json", "df"}``.

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'name': ['n1', 'n2', 'n2'], 'label': ['L1', '', 'L2']})
        >>> get_variable_labels(df, 'dict')
        {'n1': 'L1', 'n2': 'L2'}
        >>> get_variable_labels(df, 'df')
        colName label
        0      n1    L1
        1      n2    L2
    """
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
    if format == "json":
        return json.dumps(labels_dict, indent=4)
    elif format == "df":
        df = pd.DataFrame(list(labels_dict.items()), columns=["colName", "label"])
        return df

    return labels_dict


def get_choice_labels(
    xlsform_df: pd.DataFrame, format: str = "dict"
) -> Union[dict[str, str], str, pd.DataFrame]:
    """
    Build a mapping from each XLSForm question ``name`` to its choice value labels,
    and return it as a dictionary, JSON string, or DataFrame.

    The function expects an input DataFrame with:
      - a column ``"name"`` for the question (field) names, and
      - a column ``"choiceList"`` whose rows contain a structure with a ``"choices"`` list.
        Each item in ``choices`` is a dict with ``"name"`` (the choice value/code)
        and ``"label"`` (the human-readable label).

    Duplicate question names are merged, with later entries updating earlier ones.

    Args:
        xlsform_df (pandas.DataFrame): Input DataFrame containing at least the columns
            ``"name"`` and ``"choiceList"``. Each ``choiceList`` entry should include
            a ``"choices"`` list of dicts with keys ``"name"`` and ``"label"``.
        format (str, optional): Output format; one of ``"dict"``, ``"json"``, or ``"df"``.
            Defaults to ``"dict"``.
            - ``"dict"``: returns ``dict[str, dict[str, str]]`` mapping question name to
              a dict of ``choice_name`` → ``choice_label``.
            - ``"json"``: returns a JSON-formatted ``str`` of the above mapping.
            - ``"df"``: returns a ``pandas.DataFrame`` with columns ``["colName", "label"]``,
              where ``"label"`` contains the nested dict of choice labels for each question.

    Raises:
        KeyError: If required columns (e.g., ``"name"``, ``"choiceList"``) or keys within
            ``choiceList`` (e.g., ``"choices"``, ``"name"``, ``"label"``) are missing.
        ValueError: If ``format`` is not one of ``{"dict", "json", "df"}``.

    Returns:
        dict[str, dict[str, str]] | str | pandas.DataFrame:
            Labels mapping in the requested format.

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     "name": ["q1", "q2"],
        ...     "choiceList": [
        ...         {"choices": [{"name": "yes", "label": "Yes"}, {"name": "no", "label": "No"}]},
        ...         {"choices": [{"name": "a", "label": "Option A"}, {"name": "b", "label": "Option B"}]}
        ...     ]
        ... })
        >>> get_choice_labels(df, format="dict")
        {'q1': {'yes': 'Yes', 'no': 'No'}, 'q2': {'a': 'Option A', 'b': 'Option B'}}
        >>> print(get_choice_labels(df, format="json"))
        >>> get_choice_labels(df, format="df")
    """

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

    if format == "json":
        return json.dumps(categories_dict, indent=4)
    elif format == "df":
        df = pd.DataFrame(list(categories_dict.items()), columns=["name", "choiceLabels"])
        return df

    return categories_dict


# Map values if int
def map_value_labels(survey_df: pd.DataFrame, xlsform_df: pd.DataFrame) -> pd.DataFrame:
    """
    Map numerical choice values to human-readable labels based on XLSForm choices to a DataFrame.


    Args:
      survey_df (pandas.DataFrame): The survey data with coded values.
      xlsform_df (pandas.DataFrame): DataFrame containing ``"name"`` and
        ``"choiceList"``. Each ``choiceList`` entry includes a ``"choices"`` list
        of dicts with keys ``"name"`` (code) and ``"label"`` (display text).


    Raises:
      KeyError: If required columns (``"name"``, ``"choiceList"``) or keys in
        the choices (``"name"``, ``"label"``) are missing.

    Example:
      >>> import pandas as pd
      >>> survey = pd.DataFrame({"q1": ["yes", "no"], "q2": ["a", "b"]})
      >>> xls = pd.DataFrame({
      ...   "name": ["q1", "q2"],
      ...   "choiceList": [
      ...     {"choices": [{"name": "yes", "label": "Yes"}, {"name": "no", "label": "No"}]},
      ...     {"choices": [{"name": "a", "label": "Option A"}, {"name": "b", "label": "Option B"}]}
      ...   ]
      ... })
      >>> map_value_labels(survey, xls)

    Returns:
      pandas.DataFrame: A copy of ``survey_df`` where columns present in the
      XLSForm mapping have codes replaced by labels.
    """

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
