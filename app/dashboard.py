import streamlit as st
from agent import get_ops_agent
import requests
import urllib.parse

st.set_page_config(page_title="ATL Stadium Ops Center", layout="wide")

st.markdown("""
    <style>
        /* Overall Base Theme App Background */
        .stApp { background-color: #06140c !important; color: #d1e7dd !important; }
        
        /* Sidebar Border Mapping */
        section[data-testid="stSidebar"] { background-color: #030d07 !important; border-right: 1px solid #1a5c38; }
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] strong { color: #a3cfbb !important; }
        
        /* Monospace Tactical Headers */
        h1, h2, h3, h4, h5, h6, label, p { color: #d1e7dd !important; font-family: 'Courier New', Courier, monospace !important; }
        
        /* Input Box Adjustments */
        div[data-testid="stTextInput"] input {
            background-color: #0c2416 !important; color: #f7d547 !important;
            border: 1px solid #1a5c38 !important; font-family: 'Courier New', Courier, monospace !important;
        }
        div[data-testid="stTextInput"] input:focus { border: 1px solid #f7d547 !important; box-shadow: 0 0 5px #f7d547 !important; }
        
        /* Blended Dashboard Cards */
        .analytics-card {
            background-color: #081d11; 
            padding: 18px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Copilot Content Container */
        .tactical-box {
            background-color: #0a1f13; border: 1px solid #e35d5d; border-left: 5px solid #f7d547;
            padding: 20px; border-radius: 8px; font-family: 'Courier New', Courier, monospace;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center; color: #f7d547; font-weight: bold;'>⚡ Atlanta Stadium Command Copilot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3cfbb;'>FIFA World Cup 2026 — Integrated Tactical Operations Console</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px solid #1a5c38;'>", unsafe_allow_html=True)

# Live Telemetry Data
try:
    gates = requests.get("http://127.0.0.1:8000/api/v1/gates").json()
    transit = requests.get("http://127.0.0.1:8000/api/v1/transit").json()
    weather = requests.get("http://127.0.0.1:8000/api/v1/weather").json()
    api_online = True
except Exception:
    api_online = False

if api_online:
    col_visual, col_metrics = st.columns([2.2, 1.8])

    with col_visual:
        st.markdown("<h3 style='color: #a3cfbb;'>🏟️ Live Interactive 3D Digital Twin</h3>", unsafe_allow_html=True)
        
        threejs_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <style>
                body { margin: 0; overflow: hidden; background-color: #06140c; }
                #canvas-container { width: 100vw; height: 100vh; }
            </style>
        </head>
        <body>
            <div id="canvas-container"></div>
            <script>
                const container = document.getElementById('canvas-container');
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x06140c);
                
                const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
                camera.position.set(0, 22, 32);
                camera.lookAt(0, 0, 0);

                const renderer = new THREE.WebGLRenderer({ antialias: true });
                renderer.setSize(window.innerWidth, window.innerHeight);
                container.appendChild(renderer.domElement);

                const stadiumGroup = new THREE.Group();

                // 1. THE FIELD/PITCH
                const pitchGeo = new THREE.PlaneGeometry(18, 11);
                const pitchMat = new THREE.MeshBasicMaterial({ color: 0x1a5c38, wireframe: true, side: THREE.DoubleSide });
                const pitch = new THREE.Mesh(pitchGeo, pitchMat);
                pitch.rotation.x = Math.PI / 2;
                pitch.position.y = -2.9;
                stadiumGroup.add(pitch);

                // 2. LOWER BOWL SEATING
                const lowerBowlGeo = new THREE.CylinderGeometry(12, 10, 3, 32, 3, true);
                const lowerBowlMat = new THREE.MeshBasicMaterial({ color: 0xa3cfbb, wireframe: true, transparent: true, opacity: 0.6 });
                const lowerBowl = new THREE.Mesh(lowerBowlGeo, lowerBowlMat);
                lowerBowl.position.y = -1.5;
                stadiumGroup.add(lowerBowl);

                // 3. UPPER BOWL GRANDSTANDS
                const upperBowlGeo = new THREE.CylinderGeometry(16, 13, 4, 32, 4, true);
                const upperBowlMat = new THREE.MeshBasicMaterial({ color: 0xf7d547, wireframe: true, transparent: true, opacity: 0.7 });
                const upperBowl = new THREE.Mesh(upperBowlGeo, upperBowlMat);
                upperBowl.position.y = 1.5;
                stadiumGroup.add(upperBowl);

                // 4. OUTER FACADE WALLS
                const facadeGeo = new THREE.CylinderGeometry(17, 17, 8, 16, 2, true);
                const facadeMat = new THREE.MeshBasicMaterial({ color: 0xe35d5d, wireframe: true, transparent: true, opacity: 0.4 });
                const facade = new THREE.Mesh(facadeGeo, facadeMat);
                facade.position.y = 1;
                stadiumGroup.add(facade);

                scene.add(stadiumGroup);

                // Grid ground coordinates
                const gridHelper = new THREE.GridHelper(60, 30, 0x1a5c38, 0x0c2416);
                gridHelper.position.y = -3;
                scene.add(gridHelper);

                let isDragging = false;
                let previousMousePosition = { x: 0, y: 0 };

                window.addEventListener('mousedown', (e) => { isDragging = true; });
                window.addEventListener('mousemove', (e) => {
                    if (isDragging) {
                        const deltaMove = { x: e.offsetX - previousMousePosition.x, y: e.offsetY - previousMousePosition.y };
                        stadiumGroup.rotation.y += deltaMove.x * 0.007;
                        stadiumGroup.rotation.x += deltaMove.y * 0.007;
                    }
                    previousMousePosition = { x: e.offsetX, y: e.offsetY };
                });
                window.addEventListener('mouseup', (e) => { isDragging = false; });

                function animate() {
                    requestAnimationFrame(animate);
                    if (!isDragging) {
                        stadiumGroup.rotation.y += 0.003;
                    }
                    renderer.render(scene, camera);
                }
                animate();
            </script>
        </body>
        </html>
        """
        
        encoded_html = urllib.parse.quote(threejs_html)
        st.iframe(src=f"data:text/html;charset=utf-8,{encoded_html}", height=480)

    with col_metrics:
        st.markdown("<h3 style='color: #a3cfbb;'>📊 Infrastructure Matrix Status</h3>", unsafe_allow_html=True)
        
        gate_g_data = next((metrics for name, metrics in gates.items() if "Gate G" in name), {"status": "UNKNOWN", "wait_time_mins": 0})
        vine_city_data = next((metrics for name, metrics in transit.items() if "Vine City" in name), {"status": "UNKNOWN", "capacity_utilization": "0%"})

        # Card 1: Gate Flow
        st.markdown(f"""
        <div class="analytics-card" style="border-left: 5px solid #e35d5d;">
            <h4 style="margin: 0; color: #d1e7dd;">Gate Logistical Flow</h4>
            <p style="margin: 5px 0 0 0; font-size: 14px;"><b>Gate G Target:</b> <span style="color: #e35d5d;">{gate_g_data['status']}</span></p>
            <p style="margin: 2px 0 0 0; font-size: 22px; font-weight: bold; color: #e35d5d;">{gate_g_data['wait_time_mins']} min wait</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2: Transit Utilization
        st.markdown(f"""
        <div class="analytics-card" style="border-left: 5px solid #f7d547;">
            <h4 style="margin: 0; color: #d1e7dd;">Mass Transit Utilization</h4>
            <p style="margin: 5px 0 0 0; font-size: 14px;"><b>Vine City MARTA:</b> <span style="color: #f7d547;">{vine_city_data['status']}</span></p>
            <p style="margin: 2px 0 0 0; font-size: 22px; font-weight: bold; color: #f7d547;">{vine_city_data['capacity_utilization']} Capacity</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3: Environmental Status
        st.markdown(f"""
        <div class="analytics-card" style="border-left: 5px solid #a3cfbb;">
            <h4 style="margin: 0; color: #d1e7dd;">Environmental Sensors</h4>
            <p style="margin: 5px 0 0 0; font-size: 14px;"><b>Retractable Roof:</b> <span style="color: #a3cfbb;">{weather['roof_state']}</span></p>
            <p style="margin: 2px 0 0 0; font-size: 22px; font-weight: bold; color: #a3cfbb;">⚡ Lightning: {weather['lightning_detected_radius_miles']} mi out</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px solid #1a5c38;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #a3cfbb;'>🤖 Response Protocol Logic Unit</h3>", unsafe_allow_html=True)
    user_input = st.text_input(
        "ASK COPILOT YOUR QUERY:", 
        placeholder="e.g., 'Give me an immediate operational assessment.'"
    )

    if user_input:
        with st.spinner("Compiling tactical directives..."):
            if "agent_core" not in st.session_state:
                st.session_state.agent_core = get_ops_agent()
            
            response = st.session_state.agent_core.invoke({"input": user_input})
            
            st.markdown("<div class='tactical-box'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #e35d5d; margin-top: 0;'>📋 Copilot Tactical Action Directive</h3>", unsafe_allow_html=True)
            
            output_data = response.get("output", "")
            if isinstance(output_data, list) and len(output_data) > 0:
                clean_text = output_data[0].get("text", str(output_data))
            elif isinstance(output_data, dict):
                clean_text = output_data.get("text", str(output_data))
            else:
                clean_text = str(output_data)
                
            st.markdown(clean_text)
            st.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='background-color: #1a5c38; color: #d1e7dd; padding: 10px; border-radius: 5px; text-align: center; font-family: monospace;'>
            <b>📡 RADAR SYSTEM ACTIVE</b>
        </div>
        """, unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    st.sidebar.subheader("🟢 Gate Feeds")
    for g, metrics in gates.items():
        color_tag = "#e35d5d" if "CRITICAL" in metrics['status'] else "#a3cfbb"
        st.sidebar.markdown(f"**{g}**: {metrics['wait_time_mins']} min wait (<span style='color: {color_tag};'>{metrics['status']}</span>)", unsafe_allow_html=True)
        
    st.sidebar.subheader("🟡 MARTA Subsystems")
    for s, metrics in transit.items():
        color_tag = "#f7d547" if "HOLD" in metrics['status'] else "#a3cfbb"
        st.sidebar.markdown(f"**{s}**: {metrics['capacity_utilization']} capacity (<span style='color: {color_tag};'>{metrics['status']}</span>)", unsafe_allow_html=True)
