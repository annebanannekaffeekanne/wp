import pytest
import pandas as pd
from methods import add_patient, delete_patient, update
# test add_patient
@pytest.fixture(scope="module")
def df():
    return pd.read_csv('/Users/anne/PycharmProjects/ep_project/data/updated_breast_cancer_train.csv')

def test_add_patient(df):
    # Initial row count
    initial_row_count = len(df)

    # New patient data
    new_patient_data = {
        "diagnosis": -1,
        "radius_mean": 14,
        "texture_mean": 14,
        "perimeter_mean": 100,
        "area_mean": 2,
        "smoothness_mean": 700,
        "compactness_mean": 0.1,
        "concavity_mean": 0.1,
        "concave points_mean": 0.3,
        "symmetry_mean": 0.1,
        "fractal_dimension_mean": 0.2,
        "radius_se": 0.05,
        "texture_se": 0.3,
        "perimeter_se": 0.5,
        "area_se": 2,
        "smoothness_se": 45,
        "compactness_se": 0.005,
        "concavity_se": 0.03,
        "concave points_se": 0.03,
        "symmetry_se": 0.05,
        "fractal_dimension_se": 0.02,
        "radius_worst": 0.02,
        "texture_worst": 0.003,
        "perimeter_worst": 19,
        "area_worst": 17,
        "smoothness_worst": 130,
        "compactness_worst": 1500,
        "concavity_worst": 0.2,
        "concave points_worst": 0.4,
        "symmetry_worst": 0.3,
        "fractal_dimension_worst": 0.1,
        "Name": "Annika Haschko",
        "Age": 20
    }

    # Add patient
    new_df = add_patient(new_patient_data)

    # Check if the patient was added correctly
    assert len(new_df) == initial_row_count + 1  # One additional row should be added
    assert new_df["Name"].iloc[-1] == "Annika Haschko"  # Check if the last row contains the new patient's data
    assert new_df["Age"].iloc[-1] == 20
    assert new_df["diagnosis"].iloc[-1] == -1
    assert new_df["radius_mean"].iloc[-1] == 14
    assert new_df["texture_mean"].iloc[-1] == 14
    assert new_df["perimeter_mean"].iloc[-1] == 100
    assert new_df["area_mean"].iloc[-1] == 2
    assert new_df["smoothness_mean"].iloc[-1] == 700
    assert new_df["compactness_mean"].iloc[-1] == 0.1
    assert new_df["concavity_mean"].iloc[-1] == 0.1
    assert new_df["concave points_mean"].iloc[-1] == 0.3
    assert new_df["symmetry_mean"].iloc[-1] == 0.1
    assert new_df["fractal_dimension_mean"].iloc[-1] == 0.2
    assert new_df["radius_se"].iloc[-1] == 0.05
    assert new_df["texture_se"].iloc[-1] == 0.3
    assert new_df["perimeter_se"].iloc[-1] == 0.5
    assert new_df["area_se"].iloc[-1] == 2
    assert new_df["smoothness_se"].iloc[-1] == 45
    assert new_df["compactness_se"].iloc[-1] == 0.005
    assert new_df["concavity_se"].iloc[-1] == 0.03
    assert new_df["concave points_se"].iloc[-1] == 0.03
    assert new_df["symmetry_se"].iloc[-1] == 0.05
    assert new_df["fractal_dimension_se"].iloc[-1] == 0.02
    assert new_df["radius_worst"].iloc[-1] == 0.02
    assert new_df["texture_worst"].iloc[-1] == 0.003
    assert new_df["perimeter_worst"].iloc[-1] == 19
    assert new_df["area_worst"].iloc[-1] == 17
    assert new_df["smoothness_worst"].iloc[-1] == 130
    assert new_df["compactness_worst"].iloc[-1] == 1500
    assert new_df["concavity_worst"].iloc[-1] == 0.2
    assert new_df["concave points_worst"].iloc[-1] == 0.4
    assert new_df["symmetry_worst"].iloc[-1] == 0.3
    assert new_df["fractal_dimension_worst"].iloc[-1] == 0.1





