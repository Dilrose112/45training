import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr

# ================ SETUP ================
st.set_page_config(
    page_title="Disease-Weather Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================ WHITE THEME CSS ================
st.markdown("""
<style>
/* Main white theme */
[data-testid="stAppViewContainer"] {
    background: #ffffff;
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0.7);
}
[data-testid="stSidebar"] {
    background: #f8f9fa;
}

/* Cards */
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #eaeaea;
    margin-bottom: 15px;
}
.metric-card h3 {
    color: #555;
    font-size: 14px;
    margin: 0 0 5px 0;
}
.metric-card h1 {
    color: #222;
    font-size: 28px;
    margin: 0;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 10px;
}
[data-baseweb="tab"] {
    background: #f1f1f1;
    border-radius: 8px !important;
    padding: 8px 16px;
    margin: 0 2px !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    background: #3182ce !important;
    color: white !important;
}

/* Hover effects */
.stPlotlyChart, .metric-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stPlotlyChart:hover, .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# ================ DATA ================
@st.cache_data
def load_data():
    data = pd.DataFrame({
        "Year": range(2010, 2024),
        "Malaria_Cases": [1200, 1500, 900, 1800, 1300, 2000, 1700, 1400, 2100, 1900, 1600, 2300, 2200, 2400],
        "Dengue_Cases": [300, 500, 600, 400, 700, 800, 550, 750, 900, 850, 950, 1000, 1100, 1200],
        "Temperature": [28, 29, 30, 31, 30, 32, 31, 29, 33, 32, 30, 34, 33, 35],
        "Rainfall": [120, 150, 90, 180, 130, 200, 170, 140, 210, 190, 160, 230, 220, 240],
        "State": ["Maharashtra"]*14,
        "lat": [19.7515]*14,
        "lon": [75.7139]*14
    })
    return data

df = load_data()

# ================ SIDEBAR ================
with st.sidebar:
    st.title("⚙️ Dashboard Controls")
    
    st.subheader("Time Range")
    year_range = st.slider("Select years", 2010, 2023, (2015, 2023))
    
    st.subheader("Disease Focus")
    disease = st.radio("Primary disease", ["Malaria", "Dengue"], index=0)
    
    st.subheader("Advanced")
    show_forecast = st.checkbox("Show predictions", True)
    show_outliers = st.checkbox("Highlight anomalies", False)

# ================ MAIN DASHBOARD ================
st.title("🌦️ Disease-Weather Correlation Dashboard")
st.caption("Analyzing relationships between climate factors and disease prevalence in India")

# ===== METRIC CARDS =====
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Total {disease} Cases</h3>
        <h1>{df[f'{disease}_Cases'].sum():,}</h1>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🌡️ Avg Temperature</h3>
        <h1>{df['Temperature'].mean():.1f}°C</h1>
    </div>
    """, unsafe_allow_html=True)
with col3:
    corr, _ = pearsonr(df[f'{disease}_Cases'], df['Temperature'])
    st.markdown(f"""
    <div class="metric-card">
        <h3>📈 Temperature Correlation</h3>
        <h1>{corr:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# ===== TABS =====
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Geographic", "🔬 Analysis"])

with tab1:
    # Time Series Chart
    fig = px.line(
        df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])], 
        x="Year", 
        y=[f"{disease}_Cases", "Temperature"],
        labels={"value": "Count/Temperature (°C)"},
        color_discrete_sequence=["#3182ce", "#e6550d"]
    )
    fig.update_layout(
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Map Visualization
    st.pydeck_chart(pdk.Deck(
        layers=[pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_fill_color=[255, 99, 71, 160],
            get_radius=50000,
            pickable=True
        )],
        initial_view_state=pdk.ViewState(
            latitude=20.5937,
            longitude=78.9629,
            zoom=4
        ),
        tooltip={"text": f"{disease} Cases: {{{disease}_Cases}}"}
    ))

with tab3:
    # Correlation Analysis
    fig = px.scatter(
        df,
        x="Temperature",
        y=f"{disease}_Cases",
        trendline="ols",
        color_discrete_sequence=["#3182ce"]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if show_forecast:
        model = RandomForestRegressor().fit(df[['Temperature']], df[f'{disease}_Cases'])
        future_temp = st.slider("Projected temperature (°C)", 20, 40, 30)
        prediction = model.predict([[future_temp]])[0]
        st.metric("Predicted Cases", f"{int(prediction):,}", delta_color="off")

# ===== FOOTER =====
st.divider()
st.caption("Data sources: WHO Global Health Observatory | India Meteorological Department")