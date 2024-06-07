import pandas as pd

def get_value_labels(df):
    choiceList = pd.json_normalize(df['choiceList']).dropna()
    choices = choiceList.explode('choices')

    categories_dict = dict()
    for _, row in choices.iterrows():
        name = row["name"]
        choice = row["choices"]
        if name in categories_dict:
            categories_dict[name].update({choice["name"]: choice["label"]})
        else:
            categories_dict[name] = {choice["name"]: choice["label"]}
    return categories_dict


def map_value_labels(survey_data, questionnaire):
    choiceList = pd.json_normalize(questionnaire['choiceList']).dropna()
    choices = choiceList.explode('choices')

    categories_dict = dict()
    for _, row in choices.iterrows():
        name = row["name"]
        choice = row["choices"]
        if name in categories_dict:
            categories_dict[name].update({choice["name"]: choice["label"]})
        else:
            categories_dict[name] = {choice["name"]: choice["label"]}

    # Map the categories to survey_data
    survey_data_value_labels = survey_data.copy()
    for col in survey_data_value_labels.columns:
        if col in categories_dict:
            category_dict = categories_dict[col]
            survey_data_value_labels[col] = survey_data_value_labels[col].apply(lambda x: category_dict.get(str(x), x))

    return survey_data_value_labels