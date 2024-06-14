# import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random

# methods for data analysis
def load_and_normalize_data(filepath):
    df = pd.read_csv(filepath)
    df_wout_diagnosis = df.iloc[:, 1:30]                                           # create df without class-column
    norm_df = (df_wout_diagnosis - df_wout_diagnosis.mean()) / df_wout_diagnosis.std() # normalize df
    norm_df["diagnosis"] = df["diagnosis"]                                         # add class-column to normalized df
    return norm_df

def split_data(df, validation_size=0.33):                               # split a third of original data
    norm_valid_df = df.sample(frac=validation_size).copy()              # create validation df
    norm_train_df = df.drop(norm_valid_df.index).reset_index(drop=True) # create train df without rows of validation df
    return norm_train_df, norm_valid_df

def seperate_data(df):
    X = df.iloc[:,:-1].values       # all feature-columns
    y = df.iloc[:,-1].values        # class-column
    return X, y

def get_statistics(df):
    for col, column in df.iloc[:, 1:].items():   # iterates through all columns
        max = df[col].max()                      # calculate maximum
        min = df[col].min()                      # calculate minimum
        mean = df[col].mean()                    # calculate arithmetic mean
        print(f"{col}: maximum: {max}, minimum: {min}, arithmetic mean: {mean}")
    return max, min, mean

def histogram_intersection(h1, h2):
    minimum = np.minimum(h1, h2)
    intersection = np.sum(minimum)                     # intersection of the two histograms (class 1, class -1)
    total_area = np.sum(h1) + np.sum(h2)               # area of both classes
    percentage = (2 * intersection / total_area) * 100 # percentage of intersection
    return percentage
