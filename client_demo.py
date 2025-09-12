import requests, os
API = os.getenv("API_URL", "http://pi.local:8000")
KEY = os.getenv("API_KEY", "devkey")
H = {"x-api-key": KEY}

print("Telemetry:", requests.get(f"{API}/api/v1/telemetry", headers=H, timeout=3).json())
print("LED on:", requests.post(f"{API}/api/v1/led", headers=H, json={"state": True}, timeout=3).json())
print("LED off:", requests.post(f"{API}/api/v1/led", headers=H, json={"state": False}, timeout=3).json())
