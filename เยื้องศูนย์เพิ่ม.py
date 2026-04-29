import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# ======================
# Bearing capacity factor
# ======================
def bearing_factors(phi):
    phi_rad = math.radians(phi)

    if phi == 0:
        Nc, Nq, Ngamma = 5.7, 1, 0
    else:
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45 + phi/2)))**2
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)

    return Nc, Nq, Ngamma


# ======================
# UI
# ======================
st.title("🏗️ Eccentric Footing (Auto from Column Layout)")

st.subheader("📐 Footing Size")
B = st.number_input("Width B (m)", value=1.90)
L = st.number_input("Length L (m)", value=1.90)

st.subheader("📍 Column Positions (m)")
st.write("ใส่ตำแหน่งจากมุมซ้ายล่าง")

cols = []
loads = []

for i in range(4):
    col1, col2, col3 = st.columns(3)
    x = col1.number_input(f"x{i+1}", value=0.3*i)
    y = col2.number_input(f"y{i+1}", value=0.3*i)
    P = col3.number_input(f"P{i+1} (kN)", value=200.0)

    cols.append((x, y))
    loads.append(P)

# ======================
# Soil properties
# ======================
st.subheader("🌱 Soil Properties")

c = st.number_input("c (kPa)", value=10.0)
phi = st.number_input("phi (deg)", value=30.0)
gamma = st.number_input("gamma (kN/m³)", value=18.0)
Df = st.number_input("Df (m)", value=1.0)
FS = st.number_input("FS", value=3.0)

# ======================
# CALCULATE
# ======================
if st.button("🚀 Calculate"):

    P_total = sum(loads)

    # centroid of loads
    x_bar = sum(loads[i]*cols[i][0] for i in range(4)) / P_total
    y_bar = sum(loads[i]*cols[i][1] for i in range(4)) / P_total

    # center footing
    x_center = B / 2
    y_center = L / 2

    ex = x_center - x_bar
    ey = y_center - y_bar

    # effective dimension
    B_eff = B - 2*abs(ex)
    L_eff = L - 2*abs(ey)

    st.write("### 📊 Eccentricity")
    st.write(f"ex = {ex:.3f} m")
    st.write(f"ey = {ey:.3f} m")

    if B_eff <= 0 or L_eff <= 0:
        st.error("❌ Overturning (B' หรือ L' ≤ 0)")
    else:
        Nc, Nq, Ngamma = bearing_factors(phi)

        qult = c*Nc + gamma*Df*Nq + 0.5*gamma*B_eff*Ngamma
        qall = qult / FS
        q_actual = P_total / (B_eff * L_eff)

        st.write("### 📊 Results")
        st.write(f"B' = {B_eff:.2f} m")
        st.write(f"L' = {L_eff:.2f} m")
        st.write(f"q_ult = {qult:.2f} kPa")
        st.write(f"q_all = {qall:.2f} kPa")
        st.write(f"q_actual = {q_actual:.2f} kPa")

        if q_actual <= qall:
            st.success("✅ SAFE")
        else:
            st.error("❌ NOT SAFE")

    # ======================
    # 📈 DRAWING
    # ======================
    fig, ax = plt.subplots()

    # footing
    rect = plt.Rectangle((0,0), B, L, fill=False, linewidth=2)
    ax.add_patch(rect)

    # columns
    for (x,y) in cols:
        ax.plot(x, y, 'ro')

    # centroid
    ax.plot(x_bar, y_bar, 'bx', markersize=12, label="Load Centroid")

    # center footing
    ax.plot(x_center, y_center, 'g+', markersize=12, label="Footing Center")

    ax.set_xlim(-0.2, B+0.2)
    ax.set_ylim(-0.2, L+0.2)
    ax.set_aspect('equal')

    ax.legend()
    ax.set_title("Footing Layout")

    st.pyplot(fig)
