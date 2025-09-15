"""
Starter client for the IoT REST API.
Tasks:
1. Complete the GET request to /telemetry
2. Complete the POST request to /led
3. Handle errors (e.g., connection refused, invalid JSON)
"""

import requests, os

API = "http://localhost:8000/api/v1"   # change if running on another host
KEY = "devkey"                         # must match your API_KEY in the server
HEADERS = {"x-api-key": KEY}

def get_telemetry():
    # TODO: perform a GET request to /telemetry and print the result
    # Hint: requests.get(...)
    pass

def set_led(state: bool):
    # TODO: perform a POST request to /led with JSON body {"state": state}
    # Hint: requests.post(..., json=...)
    pass

if __name__ == "__main__":
    print("=== Telemetry ===")
    get_telemetry()

    print("=== Turn LED on ===")
    set_led(True)

    print("=== Turn LED off ===")
    set_led(False)
