import pandas as pd
import numpy as np
import io
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

# load dataframe
df = pd.read_csv("/Users/anne/PycharmProjects/ep_project/data/updated_breast_cancer_train.csv")
# add ID for every row of dataframe
df["ID"] = range(1, len(df)+1)
# set page size (how many rows of df on one size -> pagination)
page_size = 50

# used for pagination: select as many rows as page_size indicates based on actual page
# convert to dictionairies
def get_data(page=0):
    return df.iloc[page*page_size:(page+1)*page_size].to_dict('records')

# calculate number of complete pages
def get_last_page():
    return len(df) // page_size

# extract a specific row based on the ID
# convert to dictionaries for further processing
def get_patient(patient_id):
    return df.loc[df['ID'] == int(patient_id)].to_dict("records")[0]


def delete_patient(patient_id):
    # declare df as global variable so that df-changes are visible outside the lokal function
    global df
    # find row indice, which have the same ID as int(patient)
    index = df[df['ID'] == int(patient_id)].index
    # when at least a row fits this condition...
    if not index.empty:
        #... delete the row with corresponding index
        df = df.drop(index)
        df = df.reset_index(drop=True)
        return True
    # no row found that fits this condition
    else:
        return False

def update(values):
    # declare df as global variable so that df-changes are visible outside the lokal function
    global df
    # finds row-indices, which have the same ID as int(patient)
    patient_id = int(values['ID'])
    index = df[df['ID'] == patient_id].index
    # when at least one row fits this condition
    if not index.empty:
        # iterate over each key-value pair of the dictionairy (key = column-name; value = new value)
        for key, value in values.items():
            # choose specific cell on the position (index, key)
            # and add new value on this position (same datatype!)
            df.loc[index, key] = value
        return True
    return False


def get_value_ranges():
    # get min and max of each column
    value_ranges = df.describe().loc[['min', 'max']]
    # extract the minimums
    min_values = value_ranges.loc['min'].to_dict()
    # extract the maximums
    max_values = value_ranges.loc['max'].to_dict()
    return min_values, max_values


def get_features():
    # features are located in all columns except the first and last three
    # make a list for each feature
    features = df.columns[1:-3].tolist()
    return features

# second 'get_features' for the add route --> different features necessary
def get_features2():
    # features are located in all columns except the last three
    # make a list for each feature
    features2 = df.columns[:-3].tolist()
    return features2



def select_features(selected_features):
    # create a new df only with the selected features and the column 'diagnosis'
    selected_feature_df = df[selected_features + ['diagnosis']]
    return selected_feature_df


def plot_histograms(selected_feature_df, selected_features):
    # create empty list for plots
    plots = []
    # iterate over the selected features
    for feature in selected_features:
        # create figure
        plt.figure(figsize=(8, 6))
        # plot histogram of the selected feature
        sns.histplot(data=selected_feature_df, x=feature, hue="diagnosis", element="step",
                     common_norm=True)
        plt.xlabel(feature)

        # create bytes IO object, that saves the image in memory
        img = io.BytesIO()
        # save image as png
        plt.savefig(img, format='png')
        # read content of bytes io object and convert base64 coded bytestring into normal python string
        # adds string to list
        plots.append(base64.b64encode(img.getvalue()).decode())
        # close plot and empty memory
        plt.close()
    return plots



def plot_piechart():
    # count the values of the column 'diagnosis'
    count_classes = df["diagnosis"].value_counts()
    # set labels
    labels = ["malignant", "benign"]
    # separate the classes of the 'count classes' variable and save in sizes
    sizes = [count_classes.get(-1, 0), count_classes.get(1, 0)]
    # first segment of piechart is pulled out
    explode = (0.1, 0)

    # createfigure
    plt.figure(figsize=(7, 7))
    # create pie chart
    plt.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=140)
    plt.title("Class Distribution")

    # create bytes IO object, that saves the image in memory
    img = io.BytesIO()
    # save image as png
    plt.savefig(img, format="png")
    # read data of io objects from the beginning
    img.seek(0)
    # read content of bytes io object and convert base64 coded bytestring into normal python string
    # speichert den string als url
    chart_url = base64.b64encode(img.getvalue()).decode('utf-8')
    # close plot and empty memory
    plt.close()
    return chart_url

def add_patient(new_patient_data):
    global df
    # generate new ID
    new_patient_data["ID"] = df["ID"].max() + 1
    #create new df
    new_patient_df = pd.DataFrame([new_patient_data])
    # add new df to original df
    df = pd.concat([df, new_patient_df], ignore_index=True)
    return df

