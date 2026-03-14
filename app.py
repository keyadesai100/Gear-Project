import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Team Gear Project", layout="wide")

# --- MATH LOGIC ---
def create_gear_data(teeth, module, thickness, d_factor, bore_r):
    pitch_r = (module * teeth) / 2
    outer_r = pitch_r + module
    root_r = pitch_r - (module * d_factor)
    
    x_o, y_o = [], []
    # 1. Generate Outer Points
    for i in range(teeth):
        for step in range(4):
            angle = (i + step/4) * (2 * np.pi / teeth)
            r = outer_r if (step == 1 or step == 2) else root_r
            x_o.append(r * np.cos(angle))
            y_o.append(r * np.sin(angle))
    
    # CRITICAL FIX: Add the first point to the end to close the circle
    x_o.append(x_o[0])
    y_o.append(y_o[0])
    x_o = np.array(x_o)
    y_o = np.array(y_o)
    
    # 2. Generate Inner Bore (aligned with outer points)
    theta = np.linspace(0, 2*np.pi, len(x_o))
    x_i = bore_r * np.cos(theta)
    y_i = bore_r * np.sin(theta)
    
    # 3. Create Triangle Indices
    n_pts = len(x_o)
    I, J, K = [], [], []
    for s in range(n_pts - 1):
        # Two triangles per segment to bridge the gap
        I.extend([s, s+1])
        J.extend([s+1, s+n_pts+1])
        k_val = s + n_pts
        K.extend([k_val, k_val])
        
    return x_o, y_o, x_i, y_i, I, J, K, pitch_r

# --- UI SIDEBAR ---
st.sidebar.header("Settings")
m = st.sidebar.number_input("Module", 0.5, 10.0, 2.0)
n = st.sidebar.slider("Teeth", 8, 100, 24)
h = st.sidebar.slider("Thickness", 2, 100, 15)
df = st.sidebar.slider("Depth Factor", 1.0, 2.0, 1.25)
br = st.sidebar.slider("Bore Radius", 1.0, 50.0, 10.0)
color = st.sidebar.color_picker("Gear Color", "#0077ff")

# --- RENDER LOGIC ---
st.title("Mechanical 3D Gear Designer")

# Safety check: Bore cannot be bigger than root radius
root_limit = (m * n / 2) - (m * df)
if br >= root_limit:
    st.error(f"❌ Bore Radius ({br}) is too large! Max allowed: {root_limit:.2f}")
else:
    x_o, y_o, x_i, y_i, I, J, K, p_r = create_gear_data(n, m, h, df, br)

    fig = go.Figure()

    # Top Face
    fig.add_trace(go.Mesh3d(x=np.append(x_o, x_i), y=np.append(y_o, y_i), z=[h]*(len(x_o)*2),
                           i=I, j=J, k=K, color=color, opacity=1))
    # Bottom Face
    fig.add_trace(go.Mesh3d(x=np.append(x_o, x_i), y=np.append(y_o, y_i), z=[0]*(len(x_o)*2),
                           i=I, j=J, k=K, color=color, opacity=1))
    
    # Outer Walls
    fig.add_trace(go.Surface(x=[x_o, x_o], y=[y_o, y_o], z=[np.zeros(len(x_o)), np.full(len(x_o), h)], 
                             showscale=False, colorscale=[[0, color], [1, color]]))
    
    # Inner Walls
    fig.add_trace(go.Surface(x=[x_i, x_i], y=[y_i, y_i], z=[np.zeros(len(x_i)), np.full(len(x_i), h)], 
                             showscale=False, colorscale=[[0, "#222"], [1, "#222"]]))

    fig.update_layout(scene=dict(aspectmode='data', 
                                xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                      height=700, margin=dict(r=0, l=0, b=0, t=0))

    st.plotly_chart(fig, use_container_width=True)
    st.metric("Pitch Diameter", f"{p_r * 2:.2f} mm")
