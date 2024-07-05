from flask import Flask, render_template, request, redirect, url_for, abort, make_response
import methods
import routes
import pytest
from shared import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_delete_patient_success(client):
    # mock for methods.delete_patient, to simulate successful deletion
    with patch('methods.delete_patient', return_value=True):
        # GET request to delete_patient-route
        response = client.get("/delete/1")
        # check status and if redirection worked
        assert response.status_code == 302
        assert response.headers["Location"] == "/patients"


def test_delete_patient_not_found(client):
    # mock for methods.delete_patient, to simulate patients which are not found
    with patch('methods.delete_patient', return_value=False):
        # GET-request to delete_patient-route for non-existing patient
        response = client.get("/delete/999")

        # check status and if redirection worked
        assert response.status_code == 404
