
import streamlit as st
from PIL import Image

# --- Branding Colors and Fonts ---
PRIMARY_COLOR = "#17E0A7"
TEXT_COLOR = "#30322F"

# --- Media Type to Porosity Mapping ---
MEDIA_POROSITY = {
    "Coarse Graded Aggregate": 0.30,
    "Hydrorock": 0.94,
    "Geocellular": 0.95,
}

# --- Required Volume Lookup Table (Runoff Area -> Volume) ---
REQUIRED_VOLUME_LOOKUP = [
    (10, 1.5), (20, 3.2), (30, 4.8), (40, 6.4), (50, 8.0),
    (60, 9.6), (70, 11.3), (80, 12.9), (90, 14.5), (100, 16.1),
    (110, 17.8), (120, 19.4), (130, 21.0), (140, 22.6), (150, 24.2),
    (160, 25.9), (170, 27.5), (180, 29.1), (190, 30.7), (200, 32.3)
]

def get_required_volume(runoff_area):
    for area, volume in REQUIRED_VOLUME_LOOKUP:
        if runoff_area <= area:
            return volume
    return REQUIRED_VOLUME_LOOKUP[-1][1]  # Return max if above range

# --- App Layout ---
st.set_page_config(page_title="Retrofit SuDS Calculator", layout="centered")
st.title("Retrofit SuDS Raingarden Calculator")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Raingarden Area (m²)", min_value=0.0, value=10.0, step=0.1)
    media = st.selectbox("Media Type", list(MEDIA_POROSITY.keys()))

with col2:
    runoff_area = st.number_input("Impermeable Area Draining to Garden (m²)", min_value=0.0, value=20.0, step=0.1)
    depth = st.number_input("Depth of Raingarden (m)", min_value=0.0, value=1.5, step=0.1)

# --- Calculations ---
porosity = MEDIA_POROSITY.get(media, 0.3)
required_volume = get_required_volume(runoff_area)
provided_volume = porosity * depth * area

area_check = "Pass" if area >= 0.1 * runoff_area else "Fail"
volume_check = "Pass" if provided_volume >= required_volume else "Fail"

# --- Results ---
st.markdown("### Results")

st.metric("Required Volume (m³)", f"{required_volume:.2f}")
st.metric("Provided Volume (m³)", f"{provided_volume:.2f}")
st.metric("Minimum Area Check", area_check)
st.metric("Storage Volume Check", volume_check)

# --- Branding ---
st.markdown("---")
st.markdown("""
<div style='text-align:center;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/City_of_London_CoA.svg/1200px-City_of_London_CoA.svg.png' width='80'/>
    <p style='font-family:Montserrat; color:#30322F; font-size: 14px;'>Built by Enginuity for the City of London</p>
</div>
""", unsafe_allow_html=True)
