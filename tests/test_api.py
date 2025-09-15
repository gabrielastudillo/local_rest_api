"""
Starter test file for IoT REST API.
Tasks:
1. Write a test for /health
2. Write a test for /telemetry WITHOUT API key (should return 401)
3. Write a test for /telemetry WITH API key (should return JSON)
"""

import pytest
from fastapi.testclient import TestClient
from app import app, API_KEY

client = TestClient(app)
HEADERS = {"x-api-key": API_KEY}

def test_health():
    # TODO: call GET /health and check response code and content
    # Hint: r = client.get("/api/v1/health")
    pass

def test_unauthorized():
    # TODO: call GET /telemetry WITHOUT headers
    # Expect status_code == 401
    pass

def test_telemetry_with_key(monkeypatch):
    #from app import
    # TODO: monkeypatch sensor functions so test doesn't require real hardware
    # Hint: monkeypatch.setattr("app.read_pot_voltage", lambda: 1.23)
    # Then GET /telemetry with HEADERS
    pass
