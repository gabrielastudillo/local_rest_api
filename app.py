import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, conint, confloat
from dotenv import load_dotenv
from datetime import datetime, timezone
from typing import Optional
from devices import read_pot_voltage, led_set, led_state, buzzer_pulse, button_pressed

load_dotenv()
API_KEY = os.getenv("API_KEY", "devkey")  # simple classroom auth

app = FastAPI(title="Pi IoT API", version="1.0.0")

# --- very simple API key dependency (optional but useful) ---
def require_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")

# ---------- Schemas ----------
class CmdLED(BaseModel):
    state: bool

class CmdBuzzer(BaseModel):
    ms: Optional[conint(ge=50, le=2000)] = 200

class Telemetry(BaseModel):
    ts: str
    pot_v: confloat(ge=0.0, le=3.3)
    button: bool
    led: bool

# ---------- Routes ----------
@app.get("/api/v1/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.get("/api/v1/telemetry", response_model=Telemetry, dependencies=[Depends(require_key)])
def get_telemetry():
    try:
        return Telemetry(
            ts=datetime.now(timezone.utc).isoformat(),
            pot_v=read_pot_voltage(),
            button=button_pressed(),
            led=led_state(),
        )
    except Exception as e:
        raise HTTPException(500, f"telemetry error: {e}")

@app.post("/api/v1/led", dependencies=[Depends(require_key)])
def post_led(cmd: CmdLED):
    try:
        led_set(cmd.state)
        return {"ok": True, "led": led_state()}
    except Exception as e:
        raise HTTPException(500, f"led error: {e}")

@app.post("/api/v1/buzzer", dependencies=[Depends(require_key)])
def post_buzzer(cmd: CmdBuzzer):
    try:
        buzzer_pulse(cmd.ms / 1000.0)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(500, f"buzzer error: {e}")

# ---------- Optional: Server-Sent Events for button events ----------
@app.get("/api/v1/events/button")
async def sse_button(request: Request):
    # Minimal SSE stream. Use with: curl -N -H "x-api-key: devkey" http://pi:8000/api/v1/events/button
    async def event_gen():
        last_state = None
        while True:
            if await request.is_disconnected():
                break
            state = button_pressed()
            if state != last_state:
                yield f"data: { {'ts': datetime.now(timezone.utc).isoformat(), 'button': state} }\n\n"
                last_state = state
            # simple pacing
            await asyncio.sleep(0.05)

    import asyncio
    return PlainTextResponse(event_gen(), media_type="text/event-stream")
