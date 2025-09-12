# local_rest_api

## Run the server (on the Pi):
pip install -r requirements.txt
export API_KEY=devkey
uvicorn app:app --host 0.0.0.0 --port 8000

## Test with curl (from laptop on same LAN):
### Health
curl http://pi.local:8000/api/v1/health

# Read telemetry
curl -H "x-api-key: devkey" http://pi.local:8000/api/v1/telemetry

# Turn LED on/off
curl -X POST -H "Content-Type: application/json" -H "x-api-key: devkey" \
  -d '{"state":true}' http://pi.local:8000/api/v1/led

curl -X POST -H "Content-Type: application/json" -H "x-api-key: devkey" \
  -d '{"state":false}' http://pi.local:8000/api/v1/led

# Buzz
curl -X POST -H "Content-Type: application/json" -H "x-api-key: devkey" \
  -d '{"ms":300}' http://pi.local:8000/api/v1/buzzer

