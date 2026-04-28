import streamlit as st

# Title
st.title("Gear Calculator")

# Input fields
module = st.number_input("Module", min_value=0.0, format="%.2f")
teeth = st.number_input("Teeth", min_value=1, step=1)
thickness = st.number_input("Thickness", min_value=0.0, format="%.2f")
depth_factor = st.number_input("Depth factor", min_value=0.0, format="%.2f")
bore_radius = st.number_input("Bore radius", min_value=0.0, format="%.2f")

# Button
if st.button("Calculate Gear"):
    try:
        pitch_r = (module * teeth) / 2
        outer_r = pitch_r + module
        root_r = pitch_r - (module * depth_factor)

        st.success("Calculation Successful!")

        st.write(f"**Pitch Radius:** {pitch_r:.2f}")
        st.write(f"**Outer Radius:** {outer_r:.2f}")
        st.write(f"**Root Radius:** {root_r:.2f}")

    except:
        st.error("Invalid Input!")
