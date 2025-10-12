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
        color: #ff4b4b;
        text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b;
        font-family: 'Agency FB', sans-serif;
    }
    .stApp {
        color: #e0e0e0;
        text-shadow: 0 0 5px #ffffff;
        font-family: 'Agency FB', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #1c1c1c;
        font-family: 'Agency FB', sans-serif;
        color: #ff4b4b;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Agency FB', sans-serif;
        color: #ff4b4b;
    }
    label, .markdown-text-container {
        font-family: 'Agency FB', sans-serif;
        color: #e0e0e0;
    }
    </style>
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

set_background("m3_back.jpg")

# 🎨 Font-controlled input label helper
def styled_input(label_text, key, **kwargs):
    st.markdown(f'<label style="font-family:Agency FB; color:#ff4b4b;">{label_text}</label>', unsafe_allow_html=True)
    return st.number_input("", key=key, **kwargs)

# 🎬 Title
st.markdown('<h1 style="font-family:Agency FB; color:#ff4b4b;">🔧 SAM RAZOR PULSE CORE Torque Simulator</h1>', unsafe_allow_html=True)

# 🎮 Engine Type Selection
st.markdown('<label style="font-family:Agency FB; color:#ff4b4b;">Choose Engine Type:</label>', unsafe_allow_html=True)
engine_type = st.radio("", ["ICE (Combustion)", "Pulse Core (Electric Solenoid)"], key="engine_type")

# 🔍 Force Input (per piston only)
if engine_type == "ICE (Combustion)":
    bore_mm = styled_input("Enter piston bore (in mm)", key="bore_mm", min_value=0.0)
    pressure_mpa = styled_input("Enter peak cylinder pressure (in MPa)", key="pressure_mpa", min_value=0.0)
    radius_m = (bore_mm / 1000) / 2
    area = math.pi * radius_m**2
    pressure_pa = pressure_mpa * 1_000_000
    force_per_piston = pressure_pa * area
else:
    solenoid_force = styled_input("Enter solenoid force (in Newtons)", key="solenoid_force", min_value=0.0)
    efficiency = st.slider("Enter efficiency factor", 0.0, 1.0, 0.85, key="efficiency")
    force_per_piston = solenoid_force * efficiency

# 🧩 Engine Geometry
total_pistons = styled_input("Total number of pistons", key="total_pistons", min_value=1, step=1)
firing_pistons = styled_input("Number of pistons firing at once", key="firing_pistons", min_value=1, step=1)
crank_radius = styled_input("Crank radius (in meters)", key="crank_radius", min_value=0.0)
rpm = styled_input("Engine RPM", key="rpm", min_value=0, step=100)

# ⚙️ Gear Ratios Input
num_gears = styled_input("Number of gears", key="num_gears", min_value=1, step=1)
gear_ratios = {}
for i in range(1, int(num_gears) + 1):
    gear_ratios[f"Gear {i}"] = styled_input(f"Gear {i} ratio", key=f"gear_{i}", min_value=0.1)

# 🔁 Final Drive Ratio
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

# 🎬 Output Display
st.markdown('<h2 style="font-family:Agency FB; color:#ff4b4b;">🧩 Engine Configuration</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Total Pistons: {total_pistons}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Pistons Firing per Cycle: {firing_pistons}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Force per Piston: {force_per_piston:.2f} N</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Total Engine Force: {total_engine_force:.2f} N</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; color:#ff4b4b;">🔧 Torque & Horsepower</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Engine Torque: {engine_torque:.2f} Nm</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Horsepower @ {rpm} RPM: {engine_hp:.2f} HP</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; color:#ff4b4b;">⚙️ Gearbox & Wheel Torque</h2>', unsafe_allow_html=True)
for gear, values in gearbox_output.items():
    st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">{gear}: Gearbox Torque = {values["gearbox_torque"]:.2f} Nm | Wheel Torque = {values["wheel_torque"]:.2f} Nm</p>', unsafe_allow_html=True)

st.markdown('<h2 style="font-family:Agency FB; color:#ff4b4b;">🏎️ Estimated Speed in Gear 1</h2>', unsafe_allow_html=True)

st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Wheel RPM: {wheel_rpm:.2f}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Speed: {speed_mps:.2f} m/s ({speed_kph:.2f} km/h)</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; color:#e0e0e0;">Powered by Total Engine Force: {total_engine_force:.2f} N from {total_pistons} pistons</p>', unsafe_allow_html=True)

