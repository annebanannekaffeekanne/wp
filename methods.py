import pandas as pd
import numpy as np
import io
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

df = pd.read_csv("/Users/anne/PycharmProjects/ep_project/data/updated_breast_cancer_train.csv")
df["ID"] = range(1, len(df)+1)
page_size = 50

def get_data(page=0):
    return df.iloc[page*page_size:(page+1)*page_size].to_dict('records')


def get_last_page():
    return len(df) // page_size


def get_patient(patient_id):
    return df.loc[df['ID'] == int(patient_id)].to_dict("records")[0]


def delete_patient(patient_id):
    global df
    index = df[df['ID'] == int(patient_id)].index
    if index.any():
        df = df.drop(index)
        return True
    else:
        return False

def update(values):
    global df
    index = df[df['ID'] == int(values['ID'])].index
    if index.any():
        for key, value in values.items():
            df.loc[index, key] = pd.Series(value).astype(df[key].dtype).item()
        return True
    return False


def get_features():
    features = df.columns[:-3].tolist()
    return features

def select_features(selected_features):
    selected_feature_df = df[selected_features + ['diagnosis']]
    return selected_feature_df


def plot_histograms(selected_feature_df, selected_features):
    plots = []
    for feature in selected_features:
        plt.figure(figsize=(8, 6))
        sns.histplot(data=selected_feature_df, x=feature, hue="diagnosis", element="step", stat="density",
                     common_norm=False)
        plt.xlabel(feature)

        # Um die Plot-Daten in Bytes zu konvertieren und später im HTML zu rendern
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plots.append(base64.b64encode(img.getvalue()).decode())
        plt.close()

    return plots

def data_for_piechart():
    count_classes = df["diagnosis"].value_counts()
    labels = ["Class -1", "Class 1"]
    sizes = [count_classes.get(-1, 0), count_classes.get(1, 0)]
    return labels, sizes

def plot_piechart():
    count_classes = df["diagnosis"].value_counts()
    labels = ["Class -1", "Class 1"]
    sizes = [count_classes.get(-1, 0), count_classes.get(1, 0)]

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Class Distribution")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return chart_url