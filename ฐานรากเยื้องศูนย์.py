import streamlit as st
import math

# =======================
# 🎨 CSS STYLE
# =======================
st.markdown("""
<style>
.main {
    background-color: #eef2f7;
}
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #1f3c88;
}
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 25px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}
.result {
    background: #f0f9ff;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# 🧮 FUNCTION
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


def terzaghi(c, gamma, Df, B_eff, phi):
    Nc, Nq, Ngamma = bearing_factors(phi)
    qult = c*Nc + gamma*Df*Nq + 0.5*gamma*B_eff*Ngamma
    return qult, Nc, Nq, Ngamma


# =======================
# 🖥️ UI
# =======================
st.markdown('<div class="title">🏗️ Eccentric Footing Design</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Terzaghi Bearing Capacity with Effective Area Method</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    c = st.number_input("Cohesion, c (kPa)", 0.0, 1000.0, 10.0)
    phi = st.number_input("Friction angle φ (deg)", 0.0, 50.0, 30.0)
    gamma = st.number_input("Unit weight γ (kN/m³)", 10.0, 25.0, 18.0)
    Df = st.number_input("Depth Df (m)", 0.0, 10.0, 1.0)

with col2:
    B = st.number_input("Footing width B (m)", 0.1, 10.0, 2.0)
    L = st.number_input("Footing length L (m)", 0.1, 10.0, 3.0)
    ex = st.number_input("Eccentricity ex (m)", 0.0, 5.0, 0.2)
    ey = st.number_input("Eccentricity ey (m)", 0.0, 5.0, 0.0)

P = st.number_input("Axial Load P (kN)", 0.0, 100000.0, 500.0)
FS = st.number_input("Factor of Safety", 1.0, 5.0, 3.0)

if st.button("🚀 Calculate"):

    B_eff = B - 2*ex
    L_eff = L - 2*ey

    if B_eff <= 0 or L_eff <= 0:
        st.error("❌ Eccentricity too large! Foundation will overturn.")
    else:
        qult, Nc, Nq, Ngamma = terzaghi(c, gamma, Df, B_eff, phi)
        qall = qult / FS
        q_actual = P / (B_eff * L_eff)

        st.markdown('<div class="result">', unsafe_allow_html=True)

        st.write("### 📊 Results")
        st.write(f"Effective Width B' = {B_eff:.2f} m")
        st.write(f"Effective Length L' = {L_eff:.2f} m")

        st.write(f"Ultimate Bearing Capacity q_ult = {qult:.2f} kPa")
        st.write(f"Allowable Bearing Capacity q_all = {qall:.2f} kPa")
        st.write(f"Applied Pressure q_actual = {q_actual:.2f} kPa")

        if q_actual <= qall:
            st.success("✅ SAFE DESIGN")
        else:
            st.error("❌ NOT SAFE")

        st.write("### 📐 Bearing Factors")
        st.write(f"Nc = {Nc:.2f}, Nq = {Nq:.2f}, Nγ = {Ngamma:.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =======================
# Footer
# =======================
st.markdown("""
---
👷 Geotechnical Design Tool | Terzaghi Method | Eccentric Footing
""")
