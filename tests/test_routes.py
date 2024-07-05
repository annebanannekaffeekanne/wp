from flask import Flask, render_template, request, redirect, url_for, abort, make_response
import methods
import routes
import pytest
from shared import app
import pytest
from shared import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
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
    response = client.get("/patients/1")
    assert response.status_code == 200

def test_delete_patient_route(client):
    response = client.get("/delete/1")
    assert response.status_code == 302

def test_edit_patient_route_post(client):
    response = client.post("/edit/1", data={"name": "Test Name"})
    assert response.status_code == 302

def test_data_analysis_route(client):
    response = client.get("/data_analysis")
    assert response.status_code == 200
