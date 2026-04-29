import streamlit as st
import math

# =======================
# 🎨 Custom CSS
# =======================
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
    }
    .sub {
        font-size: 18px;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# 🧮 Terzaghi Functions
# =======================
def bearing_factors(phi):
    phi_rad = math.radians(phi)
    
    if phi == 0:
        Nc = 5.7
        Nq = 1
        Ngamma = 0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2)))**2
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)
    
    return Nc, Nq, Ngamma


def terzaghi_qult(c, gamma, Df, B, phi):
    Nc, Nq, Ngamma = bearing_factors(phi)
    qult = c * Nc + gamma * Df * Nq + 0.5 * gamma * B * Ngamma
    return qult, Nc, Nq, Ngamma


# =======================
# 🖥️ UI
# =======================
st.markdown('<div class="title">🧱 Shallow Foundation Design</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Terzaghi Bearing Capacity Calculator</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        c = st.number_input("Cohesion, c (kPa)", value=10.0)
        phi = st.number_input("Friction angle, φ (deg)", value=30.0)
        gamma = st.number_input("Unit weight, γ (kN/m³)", value=18.0)

    with col2:
        Df = st.number_input("Depth of foundation, Df (m)", value=1.0)
        B = st.number_input("Width of footing, B (m)", value=1.5)
        FS = st.number_input("Factor of Safety", value=3.0)

    if st.button("🚀 Calculate"):
        qult, Nc, Nq, Ngamma = terzaghi_qult(c, gamma, Df, B, phi)
        qall = qult / FS

        st.success("Calculation Complete ✅")

        st.write("### 📊 Results")
        st.write(f"Ultimate Bearing Capacity (q_ult): {qult:.2f} kPa")
        st.write(f"Allowable Bearing Capacity (q_all): {qall:.2f} kPa")

        st.write("### 📐 Bearing Capacity Factors")
        st.write(f"Nc = {Nc:.2f}")
        st.write(f"Nq = {Nq:.2f}")
        st.write(f"Nγ = {Ngamma:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# =======================
# 📌 Footer
# =======================
st.markdown("""
---
👷 Developed for Geotechnical Engineering | Terzaghi Theory
""")
