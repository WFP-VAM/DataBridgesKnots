import pandas as pd

def get_value_labels(df):
    choiceList = pd.json_normalize(df['choiceList'])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(df["name"]).dropna()
    choices = choiceList.explode('choices')

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
    choiceList = pd.json_normalize(questionnaire['choiceList'])
    choiceList = choiceList.rename(columns={"name": "choice_name"})
    choiceList = choiceList.join(questionnaire["name"]).dropna()
    choices = choiceList.explode('choices')

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
            survey_data_value_labels[col] = survey_data_value_labels[col].apply(lambda x: category_dict.get(x, x))

    return survey_data_value_labels

def as_numeric(df, col_list):

    for col in col_list:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore').fillna(9999).astype('int64')
        except ValueError:
            continue
    
    return df


