import pytest
from shared import app
import methods


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_patient_list_route(client):
    response = client.get("/patients")
    assert response.status_code == 200

def test_add_patient_route(client):
    response = client.get("/add_patient")
    assert response.status_code == 200

def test_patient_detail_route(client):
    # valid patient ID
    response = client.get("/patients/1")
    assert response.status_code == 200

    # invalid patient ID
    response = client.get("/patients/99999")
    assert response.status_code == 404

def test_delete_patient_route(client):
    response = client.get("/delete/1")
    # redirect after deletion
    assert response.status_code == 302

    # delete a non-existing patient
    response = client.get("/delete/99999")
    assert response.status_code == 404