import streamlit as st
import math

# 🎨 Styled input
def styled_input(label_text, key, **kwargs):
    st.markdown(f'<label style="color:#ffffff; font-family:Agency FB; font-weight:bold;">{label_text}</label>', unsafe_allow_html=True)
    return st.number_input("", key=key, **kwargs)

# 🔧 Solenoid Force Calculator
def calculate_solenoid_force(turns, current, core_area_m2, air_gap_m):
    mu_0 = 4 * math.pi * 1e-7
    B = (mu_0 * turns * current) / air_gap_m
    force = (B**2 * core_area_m2) / (2 * mu_0)
    return force

# ✈️ Radial Aircraft HP Calculator
def calculate_radial_hp(bore_mm, stroke_mm, compression_ratio, afr, ve, rpm, cylinders, boost_pressure_mpa=0):
    bore_m = bore_mm / 1000
    stroke_m = stroke_mm / 1000
    area = math.pi * (bore_m / 2)**2
    displacement_per_cylinder = area * stroke_m
    total_displacement = displacement_per_cylinder * cylinders
    intake_pressure_pa = (1 + boost_pressure_mpa) * 101325
    mass_airflow = total_displacement * rpm * ve * intake_pressure_pa / (60 * 287.05 * 300)
    fuel_mass_flow = mass_airflow / afr
    energy_per_kg_fuel = 44e6
    power_watts = fuel_mass_flow * energy_per_kg_fuel * 0.3
    power_hp = power_watts / 745.7
    return power_hp
st.markdown('<p style="color:#ffffff; font-family:Agency FB; font-weight:bold;">Choose Engine Type:</p>', unsafe_allow_html=True)
engine_type = st.radio("", ["ICE (Combustion)", "Pulse Core (Electric Solenoid)", "Radial Aircraft (Aspirated)"], key="engine_type")
stroke_length_mm = styled_input("Enter cylinder/solenoid length (in mm)", key="stroke_length_mm", min_value=1.0)
stroke_length_m = stroke_length_mm / 1000
rpm = styled_input("Engine RPM", key="rpm", min_value=0, step=100)
if engine_type == "ICE (Combustion)":
    bore_mm = styled_input("Enter piston bore (in mm)", key="bore_mm", min_value=0.0)
    pressure_mpa = styled_input("Enter peak cylinder pressure (in MPa)", key="pressure_mpa", min_value=0.0)
    radius_m = (bore_mm / 1000) / 2
    area = math.pi * radius_m**2
    pressure_pa = pressure_mpa * 1_000_000
    force_per_piston = pressure_pa * area
    total_engine_force = force_per_piston
    engine_torque = total_engine_force * stroke_length_m
    engine_hp = (engine_torque * rpm) / 5252

elif engine_type == "Pulse Core (Electric Solenoid)":
    turns = styled_input("Solenoid Turns", key="turns", min_value=1)
    current = styled_input("Current (A)", key="current", min_value=0.1)
    diameter_mm = styled_input("Solenoid Core Diameter (mm)", key="diameter_mm", min_value=0.1)
    air_gap_mm = styled_input("Air Gap (mm)", key="air_gap", min_value=0.01)
    wire_area_mm2 = styled_input("Wire Cross-Sectional Area (mm²)", key="wire_area", min_value=0.01)
    efficiency = st.slider("Enter efficiency factor", 0.0, 1.0, 0.85, key="efficiency")

    radius_m = (diameter_mm / 1000) / 2
    core_area_m2 = math.pi * radius_m**2
    air_gap_m = air_gap_mm / 1000

    raw_force = calculate_solenoid_force(turns, current, core_area_m2, air_gap_m)
    force_per_piston = raw_force * efficiency * stroke_length_m * 20
    total_engine_force = force_per_piston
    engine_torque = total_engine_force * stroke_length_m
    engine_hp = (engine_torque * rpm) / 5252

elif engine_type == "Radial Aircraft (Aspirated)":
    bore_mm = styled_input("Cylinder Bore (mm)", key="radial_bore", min_value=0.0)
    stroke_mm = styled_input("Stroke Length (mm)", key="radial_stroke", min_value=0.0)
    compression_ratio = styled_input("Compression Ratio", key="compression_ratio", min_value=1.0)
    afr = styled_input("Air-Fuel Ratio", key="afr", min_value=1.0)
    ve = st.slider("Volumetric Efficiency", 0.0, 1.0, 0.85, key="ve")
    boost_pressure_mpa = styled_input("Boost Pressure (MPa)", key="boost_pressure", min_value=0.0)
    cylinders = styled_input("Number of Cylinders", key="radial_cylinders", min_value=1, step=1)

    engine_hp = calculate_radial_hp(bore_mm, stroke_mm, compression_ratio, afr, ve, rpm, cylinders, boost_pressure_mpa)
    engine_torque = (engine_hp * 5252) / rpm
    force_per_piston = 0
    total_engine_force = 0
total_pistons = styled_input("Total number of pistons", key="total_pistons", min_value=1, step=1)
firing_pistons = styled_input("Number of pistons firing at once", key="firing_pistons", min_value=1, step=1)
crank_radius = styled_input("Crank radius (in meters)", key="crank_radius", min_value=0.0)

num_gears = styled_input("Number of gears", key="num_gears", min_value=1, step=1)
gear_ratios = {}
for i in range(1, int(num_gears) + 1):
    gear_ratios[f"Gear {i}"] = styled_input(f"Gear {i} ratio", key=f"gear_{i}", min_value=0.1)

final_drive_ratio = styled_input("Final drive ratio", key="final_drive_ratio", min_value=0.1)
tire_diameter_m = styled_input("Tire diameter (in meters)", key="tire_diameter", min_value=0.1)
gearbox_output = {}
for gear, ratio in gear_ratios.items():
    gearbox_torque = engine_torque * ratio
    wheel_torque = gearbox_torque * final_drive_ratio
    gearbox_output[gear] = {
        "gearbox_torque": gearbox_torque,
        "wheel_torque": wheel_torque
    }

gear_1_ratio = list(gear_ratios.values())[0]
wheel_rpm = rpm / (gear_1_ratio * final_drive_ratio)
tire_circumference = math.pi * tire_diameter_m
speed_mps = (wheel_rpm * tire_circumference) / 60
speed_kph = speed_mps * 3.6
# 🎬 HUD Output
st.markdown('<div class="hud-container">', unsafe_allow_html=True)

# 🧩 Engine Configuration
st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🧩 Engine Configuration</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Total Pistons: {total_pistons}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Pistons Firing per Cycle: {firing_pistons}</p>', unsafe_allow_html=True)

if engine_type != "Radial Aircraft (Aspirated)":
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Force per Piston: {force_per_piston:.2f} N</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Total Engine Force: {total_engine_force:.2f} N</p>', unsafe_allow_html=True)

# 🔧 Torque & Horsepower
st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🔧 Torque & Horsepower</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Engine Torque: {engine_torque:.2f} Nm</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Horsepower @ {rpm} RPM: {engine_hp:.2f} HP</p>', unsafe_allow_html=True)

# ⚙️ Gearbox & Wheel Torque
st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">⚙️ Gearbox & Wheel Torque</h2>', unsafe_allow_html=True)
for gear, values in gearbox_output.items():
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">{gear}: Gearbox Torque = {values["gearbox_torque"]:.2f} Nm | Wheel Torque = {values["wheel_torque"]:.2f} Nm</p>', unsafe_allow_html=True)

# 🏎️ Speed Output
st.markdown('<h2 style="font-family:Agency FB; font-weight:bold; color:#ffffff;">🏎️ Estimated Speed in Gear 1</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Wheel RPM: {wheel_rpm:.2f}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Speed: {speed_mps:.2f} m/s ({speed_kph:.2f} km/h)</p>', unsafe_allow_html=True)

if engine_type != "Radial Aircraft (Aspirated)":
    st.markdown(f'<p style="font-family:Agency FB; font-weight:bold; color:#ffffff;">Powered by Total Engine Force: {total_engine_force:.2f} N from {total_pistons} pistons</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
