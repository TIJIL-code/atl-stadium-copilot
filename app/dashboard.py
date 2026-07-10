import streamlit as st
import requests
import json

try:
    from agent import get_ops_agent
except ImportError:
    try:
        from app.agent import get_ops_agent
    except ImportError:
        get_ops_agent = None

st.set_page_config(
    page_title="World Cup 2026 Operations Console",
    page_icon="🏟️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0b1d12; color: #ffffff; }
    .tactical-box {
        background-color: #142a1c;
        border: 1px solid #1f402b;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .metric-val { font-size: 24px; font-weight: bold; color: #00ff88; }
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏟️ Atlanta Stadium Command Center — FIFA 2026 Ops")
st.markdown("---")

try:
    gate_data = requests.get("http://127.0.0.1:8000/api/v1/gates", timeout=1.5).json()
except Exception:
    gate_data = [
        {"gate": "Gate A (North)", "status": "NORMAL", "flow_rate": "42/min"},
        {"gate": "Gate C (South)", "status": "SLOW", "flow_rate": "18/min"},
        {"gate": "Gate G (West)", "status": "CRITICAL", "flow_rate": "89/min"}
    ]

try:
    transit_data = requests.get("http://127.0.0.1:8000/api/v1/transit", timeout=1.5).json()
except Exception:
    transit_data = {"marta_status": "CONGESTED", "capacity_utilization": "96%"}

try:
    weather_data = requests.get("http://127.0.0.1:8000/api/v1/weather", timeout=1.5).json()
except Exception:
    weather_data = {"roof_state": "OPEN", "lightning_distance_miles": 6.5}

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🖥️ Real-Time Telemetry Matrix")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class='tactical-box'>
                <span style='font-size: 14px;'>🌌 <b>MARTA Status</b></span><br/>
                <p class='metric-val' style='margin: 5px 0 0 0;'>{transit_data['marta_status']} ({transit_data['capacity_utilization']})</p>
            </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
            <div class='tactical-box'>
                <span style='font-size: 14px;'>🏟️ <b>Retractable Roof</b></span><br/>
                <p class='metric-val' style='margin: 5px 0 0 0;'>{weather_data['roof_state']}</p>
            </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
            <div class='tactical-box'>
                <span style='font-size: 14px;'>⚡ <b>Lightning Detection</b></span><br/>
                <p class='metric-val' style='margin: 5px 0 0 0;'>{weather_data['lightning_distance_miles']} Miles Out</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🌐 3D Digital Twin Bowl Grid")
    
    # Fully self-contained 3D Cyber-Stadium Wireframe Core
    st.components.v1.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body { margin: 0; overflow: hidden; background-color: #142a1c; }
            canvas { width: 100%; height: 100%; display: block; }
        </style>
    </head>
    <body>
        <script>
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x142a1c);

            const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 45, 85);
            camera.lookAt(0, 0, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            const stadiumGroup = new THREE.Group();

            // Create a glowing neon green wireframe material
            const wireMaterial = new THREE.MeshBasicMaterial({
                color: 0x00ff88,
                wireframe: true,
                transparent: true,
                opacity: 0.8
            });

            // Outer Stadium Structural Bowl Cylinders
            for (let i = 0; i < 4; i++) {
                const radius = 30 + (i * 6);
                const height = 4 + (i * 5);
                const geo = new THREE.CylinderGeometry(radius, radius - 2, height, 32, 2, true);
                const ring = new THREE.Mesh(geo, wireMaterial);
                ring.position.y = height / 2;
                stadiumGroup.add(ring);
            }

            // Inner Pitch Outline
            const pitchGeo = new THREE.PlaneGeometry(42, 26, 4, 4);
            const pitchMaterial = new THREE.MeshBasicMaterial({ color: 0x00aa55, wireframe: true });
            const pitch = new THREE.Mesh(pitchGeo, pitchMaterial);
            pitch.rotation.x = -Math.PI / 2;
            pitch.position.y = 0.1;
            stadiumGroup.add(pitch);

            // Roof Ring Girder
            const roofGeo = new THREE.TorusGeometry(50, 1.5, 8, 48);
            const roof = new THREE.Mesh(roofGeo, wireMaterial);
            roof.rotation.x = Math.PI / 2;
            roof.position.y = 22;
            stadiumGroup.add(roof);

            scene.add(stadiumGroup);

            // Subtle rotation animation to look like an active digital twin
            function animate() {
                requestAnimationFrame(animate);
                stadiumGroup.rotation.y += 0.003;
                renderer.render(scene, camera);
            }

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            animate();
        </script>
    </body>
    </html>
    """, height=520)
with col2:
    st.markdown("### 🚪 Gate Flow Metrics")
    for gate in gate_data:
        status_color = "🟢" if gate['status'] == "NORMAL" else "🟡" if gate['status'] == "SLOW" else "🔴"
        st.markdown(f"""
            <div class='tactical-box' style='padding: 12px; margin-bottom: 10px;'>
                {status_color} <b>{gate['gate']}</b><br/>
                Status: {gate['status']} | Flow Rate: {gate['flow_rate']}
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🤖 Operations Control Copilot")

user_input = st.text_input("Issue tactical directive or query to the Operations Copilot:", placeholder="e.g., Lightning is 6.5 miles out, check safety protocols...")

if user_input:
    if get_ops_agent is None:
        st.error("❌ Configuration Error: Could not locate your `get_ops_agent` core engine inside agent.py.")
    else:
        with st.spinner("Compiling tactical directives..."):
            try:
                if "agent_core" not in st.session_state:
                    st.session_state.agent_core = get_ops_agent()
                
                response = st.session_state.agent_core.invoke({"input": user_input})
                
                st.markdown("<div class='tactical-box'>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #00ff88; margin-top: 0;'>📋 Copilot Tactical Action Directive</h3>", unsafe_allow_html=True)
                
                output_data = response.get("output", "")
                if isinstance(output_data, list) and len(output_data) > 0:
                    clean_text = output_data[0].get("text", str(output_data))
                elif isinstance(output_data, dict):
                    clean_text = output_data.get("text", str(output_data))
                else:
                    clean_text = str(output_data)
                    
                st.markdown(clean_text)
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                if "quota" in str(e).lower() or "429" in str(e) or "404" in str(e):
                    st.warning("⚠️ **Tactical Core Overloaded:** Rate limit / API quota exceeded. Standing by for backend cool-down period. (Mock fallback metrics are still active above!)")
                else:
                    st.error(f"❌ Execution Error: {e}")