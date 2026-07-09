from fastapi import FastAPI
import random

app = FastAPI(title="Atlanta Stadium Real-Time Telemetry API")

@app.get("/api/v1/gates")
def get_gate_status():
    return {
        "Gate A (Concourse NW)": {"status": "Normal", "flow_rate_per_min": random.randint(30, 50), "wait_time_mins": 5},
        "Gate T (Concourse SW)": {"status": "Normal", "flow_rate_per_min": random.randint(20, 40), "wait_time_mins": 4},
        "Gate G (West Egress)": {"status": "CRITICAL_CONGESTION", "flow_rate_per_min": random.randint(180, 220), "wait_time_mins": 35}
    }

@app.get("/api/v1/transit")
def get_marta_status():
    return {
        "Vine City Station (Blue/Green Line)": {"capacity_utilization": "96%", "status": "HOLD_ENTRY_ACTIVE", "next_train_mins": 3},
        "GWCC / CNN Center Station": {"capacity_utilization": "62%", "status": "CLEAR", "next_train_mins": 5}
    }

@app.get("/api/v1/weather")
def get_stadium_weather():
    return {
        "current_condition": "Thunderstorms",
        "lightning_detected_radius_miles": 6.5,
        "wind_speed_mph": 22,
        "roof_state": "OPEN"
    }