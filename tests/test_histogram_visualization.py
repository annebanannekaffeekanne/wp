import pytest
import pandas as pd
from methods import plot_histograms, plot_piechart

@pytest.fixture(scope="module")
def setup_dataframe():
    df = pd.read_csv('/Users/anne/PycharmProjects/ep_project/data/updated_breast_cancer_train.csv')
    return df

def test_plot_histograms(setup_dataframe):
    df = setup_dataframe.copy()
    # randomly select features
    selected_features = df.columns[1:-3]
    plots = plot_histograms(df, selected_features)

    # Check if plots were generated
    assert len(plots) == len(selected_features)

def test_plot_histograms2(setup_dataframe):
    df = setup_dataframe.copy()
    # randomly select features
    selected_features = df.columns[:-1]
    plots = plot_histograms(df, selected_features)

    # Check if plots were generated
    assert len(plots) == len(selected_features)

def test_plot_histograms3(setup_dataframe):
    df = setup_dataframe.copy()
    # randomly select features
    selected_features = df.columns[3:-3]
    plots = plot_histograms(df, selected_features)

    # Check if plots were generated
    assert len(plots) == len(selected_features)
