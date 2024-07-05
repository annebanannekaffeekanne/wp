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
    # Mock für methods.delete_patient, um erfolgreiches Löschen zu simulieren
    with patch('methods.delete_patient', return_value=True):
        # GET-Anfrage an die delete-Patientenroute
        response = client.get("/delete/1")

        # Überprüfen, dass der Statuscode 302 ist (Redirect)
        assert response.status_code == 302
        # Überprüfen, dass die Weiterleitung zur Patientenliste erfolgt
        assert response.headers["Location"] == "/patients"


def test_delete_patient_not_found(client):
    # Mock für methods.delete_patient, um nicht gefundene Patienten zu simulieren
    with patch('methods.delete_patient', return_value=False):
        # GET-Anfrage an die delete-Patientenroute für einen nicht vorhandenen Patienten
        response = client.get("/delete/999")

        # Überprüfen, dass der Statuscode 404 ist (Not Found)
        assert response.status_code == 404
