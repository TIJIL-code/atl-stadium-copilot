import streamlit as st
from agent import get_ops_agent
import requests

st.set_page_config(page_title="ATL Stadium Ops Center", layout="wide")
st.title("⚽ Atlanta Stadium Command Copilot (FIFA 2026)")

st.sidebar.header("🔴 Live Telemetry Dashboard")
try:
    gates = requests.get("http://127.0.0.1:8000/api/v1/gates").json()
    transit = requests.get("http://127.0.0.1:8000/api/v1/transit").json()
    weather = requests.get("http://127.0.0.1:8000/api/v1/weather").json()
    
    st.sidebar.subheader("Gate Management")
    for g, metrics in gates.items():
        st.sidebar.write(f"**{g}**: {metrics['wait_time_mins']} min wait ({metrics['status']})")
        
    st.sidebar.subheader("MARTA Rail")
    for s, metrics in transit.items():
        st.sidebar.write(f"**{s}**: {metrics['capacity_utilization']} cap ({metrics['status']})")
        
    st.sidebar.subheader("Roof & Environment")
    st.sidebar.write(f"Roof Status: **{weather['roof_state']}**")
    st.sidebar.write(f"Lightning: **{weather['lightning_detected_radius_miles']} miles out**")
except Exception:
    st.sidebar.error("Telemetry API offline. Run `uvicorn stadium_api:app` first.")

st.subheader("Interactive Operational Directives")
user_input = st.text_input(
    "Ask the Copilot for an operational assessment:", 
    placeholder="e.g., 'We have an ongoing crowd crunch on the west exit, what is the action plan?'"
)

if user_input:
    with st.spinner("Analyzing operational systems..."):
        agent_executor = get_ops_agent()
        response = agent_executor.invoke({"input": user_input})
        st.markdown("### 📋 Copilot Tactical Action Directive")
        st.write(response["output"])