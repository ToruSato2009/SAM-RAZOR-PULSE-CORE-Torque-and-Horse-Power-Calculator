import streamlit as st
import base64
import math

# 🔥 Inject custom UI styling
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
        transition: all 0.3s ease-in-out;
        font-family: 'Agency FB', sans-serif;
    }
    div.stButton > button:hover {
        background-color: #ff1c1c;
        transform: scale(1.05);
        box-shadow: 0 0 10px #ff4b4b;
    }
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Agency FB', sans-serif;
        font-weight: bold;
    }
    .stApp {
        font-family: 'Agency FB', sans-serif;
        font-weight: bold;
        color: #ffffff;
    }
    label, .markdown-text-container {
        font-family: 'Agency FB', sans-serif;
        font-weight: bold;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #1c1c1c;
        font-family: 'Agency FB', sans-serif;
        color: #ffffff;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Agency FB', sans-serif;
        color: #ffffff;
    }
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.4);
        z-index: 0;
    }
    .hud-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 12px;
        z-index: 1;
        position: relative;
    }
    </style>
    <div class="overlay"></div>
""", unsafe_allow_html=True)

# 🔧 Set background image
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("SAM.png")

# 🎨 Styled input
def styled_input(label_text, key, **kwargs):
    st.markdown(f'<label style="color:#ffffff; font-family:Agency FB; font-weight:bold;">{label_text}</label>', unsafe_allow_html=True)
    return st.number_input("", key=key, **kwargs)

# 🎬 Title
st.markdown('<h1>🔧 SAM RAZOR PULSE CORE Torque Simulator</h1>', unsafe_allow_html=True)

# 🔍 Force Calculation Function
def calculate_solenoid_force(turns, current, core_area_m2, air_gap_m):
    mu_0 = 4 * math.pi * 1e-7
    B = (mu_0 * turns * current) / air_gap_m
    force = (B**2 * core_area_m2) / (2 * mu_0)
    return force

# 🎮 Engine Type
st.markdown('<label style="color:#ffffff; font-family:Agency FB; font-weight:bold;">Choose Engine Type:</label>', unsafe_allow_html=True)
engine_type = st.radio("", ["ICE (Combustion)", "Pulse Core (Electric Solenoid)"], key="engine_type")

# 🔍 Force Input
if engine_type == "ICE (Combustion)":
    bore_mm = styled_input("Enter piston bore (in mm)", key="bore_mm", min_value=0.0)
    pressure_mpa = styled_input("Enter peak cylinder pressure (in MPa)", key="pressure_mpa", min_value=0.0)
    radius_m = (bore_mm / 1000) / 2
    area = math.pi * radius_m**2
    pressure_pa = pressure_mpa * 1_000_000
    force_per_piston = pressure_pa * area
else:
    turns = styled_input("Solenoid Turns", key="turns", min_value=1)
    current = styled_input("Current (A)", key="current", min_value=0.1)
    core_area_cm2 = styled_input("Core Area (cm²)", key="core_area", min_value=0.01)
    air_gap_mm = styled_input("Air Gap (mm)", key="air_gap", min_value=0.01)
    efficiency = st.slider("Enter efficiency factor", 0.0, 1.0, 0.85, key="efficiency")

    core_area_m2 = core_area_cm2 / 10000
    air_gap_m = air_gap_mm / 1000
    raw_force = calculate_solenoid_force(turns, current, core_area_m2, air_gap_m)
    force_per_piston = raw_force * efficiency

    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Calculated Solenoid Force (before efficiency): {raw_force:.2f} N</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Effective Force per Piston: {force_per_piston:.2f} N</p>', unsafe_allow_html=True)

# 🧩 Engine Geometry
total_pistons = styled_input("Total number of pistons", key="total_pistons", min_value=1, step=1)
firing_pistons = styled_input("Number of pistons firing at once", key="firing_pistons", min_value=1, step=1)
crank_radius = styled_input("Crank radius (in meters)", key="crank_radius", min_value=0.0)
rpm = styled_input("Engine RPM", key="rpm", min_value=0, step=100)

# ⚙️ Gear Ratios
num_gears = styled_input("Number of gears", key="num_gears", min_value=1, step=1)
gear_ratios = {}
for i in range(1, int(num_gears) + 1):
    gear_ratios[f"Gear {i}"] = styled_input(f"Gear {i} ratio", key=f"gear_{i}", min_value=0.1)

# 🔁 Final Drive
final_drive_ratio = styled_input("Final drive ratio", key="final_drive_ratio", min_value=0.1)

# 🛞 Tire Specs
tire_diameter_m = styled_input("Tire diameter (in meters)", key="tire_diameter", min_value=0.1)

# 🧮 Calculations
total_engine_force = force_per_piston * total_pistons
engine_torque = total_engine_force * crank_radius
engine_hp = (engine_torque * rpm) / 5252

# ⚙️ Gearbox Output
gearbox_output = {}
for gear, ratio in gear_ratios.items():
    gearbox_torque = engine_torque * ratio
    wheel_torque = gearbox_torque * final_drive_ratio
    gearbox_output[gear] = {
        "gearbox_torque": gearbox_torque,
        "wheel_torque": wheel_torque
    }

# 🚀 Speed Output
gear_1_ratio = list(gear_ratios.values())[0]
wheel_rpm = rpm / (gear_1_ratio * final_drive_ratio)
tire_circumference = math.pi * tire_diameter_m
speed_mps = (wheel_rpm * tire_circumference) / 60
speed_kph = speed_mps * 3.6
# 🎬 HUD Output
st.markdown('<div class="hud-container">', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🧩 Engine Configuration</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Total Pistons: {total_pistons}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Pistons Firing per Cycle: {firing_pistons}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Force per Piston: {force_per_piston:.2f} N</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Total Engine Force: {total_engine_force:.2f} N</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🔧 Torque & Horsepower</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Engine Torque: {engine_torque:.2f} Nm</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Horsepower @ {rpm} RPM: {engine_hp:.2f} HP</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">⚙️ Gearbox & Wheel Torque</h2>', unsafe_allow_html=True)
for gear, values in gearbox_output.items():
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">{gear}: Gearbox Torque = {values["gearbox_torque"]:.2f} Nm | Wheel Torque = {values["wheel_torque"]:.2f} Nm</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🏎️ Estimated Speed in Gear 1</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Wheel RPM: {wheel_rpm:.2f}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Speed: {speed_mps:.2f} m/s ({speed_kph:.2f} km/h)</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Powered by Total Engine Force: {total_engine_force:.2f} N from {total_pistons} pistons</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)





