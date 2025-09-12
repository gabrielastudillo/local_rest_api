from fastapi.testclient import TestClient
from app import app, API_KEY

client = TestClient(app)
H = {"x-api-key": API_KEY}

def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.text == "ok"

def test_need_key():
    r = client.get("/api/v1/telemetry")
    assert r.status_code == 401

def test_telemetry_ok(monkeypatch):
    # monkeypatch device calls so tests don't need hardware
    from app import read_pot_voltage, button_pressed, led_state
    monkeypatch.setattr("app.read_pot_voltage", lambda: 1.234)
    monkeypatch.setattr("app.button_pressed", lambda: False)
    monkeypatch.setattr("app.led_state", lambda: True)

    r = client.get("/api/v1/telemetry", headers=H)
    assert r.status_code == 200
    j = r.json()
    assert 0.0 <= j["pot_v"] <= 3.3
    assert j["button"] in [True, False]
    assert j["led"] in [True, False]
