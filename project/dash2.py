import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Climate2Cure Dashboard", layout="wide")
st.markdown("""
    <style>
        /* Set background */
        .stApp {
            background: linear-gradient(to right, #dfe9f3, #ffffff);
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #2a4d69;
        }
        .metric-label {
            color: #4b6cb7;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f0f4f7;
            border-radius: 8px 8px 0 0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4b6cb7 !important;
            color: white !important;
            font-weight: bold;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2a4d69;'>🦠 Climate2Cure: Exploring Climate-Disease Correlation</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #4b6cb7;'>", unsafe_allow_html=True)

# Load datasets
@st.cache_data
def load_data():
    weather = pd.read_csv("weather_2020_2025.csv", parse_dates=["time"])
    disease = pd.read_csv("monthly_disease_cases_2020_2025.csv")
    return weather, disease

weather_df, disease_df = load_data()
weather_df["time"] = pd.to_datetime(weather_df["time"], errors="coerce")
disease_df["Date"] = pd.to_datetime(disease_df["Date"], errors="coerce")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
st.sidebar.markdown("## 🛠️ Filter Options")
st.sidebar.markdown("Refine data by selecting below parameters.")

cities = sorted(weather_df["city"].unique())
diseases = sorted(disease_df["Disease"].unique())

selected_city = st.sidebar.selectbox("Select City", cities)
selected_disease = st.sidebar.selectbox("Select Disease", diseases)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-06-30"))

# Filtered Data
weather_filtered = weather_df[
    (weather_df["city"] == selected_city) &
    (weather_df["time"] >= pd.to_datetime(start_date)) &
    (weather_df["time"] <= pd.to_datetime(end_date))
]

disease_filtered = disease_df[
    (disease_df["Disease"] == selected_disease) &
    (disease_df["District"].str.lower() == selected_city.lower())
]

# --- Tabs ---
tabs = st.tabs(["📊 Overview", "🦠 Disease Trends", "🌡️ Climate Trends",
                "📈 Correlation","📍 Map View",  "📁 Data Explorer"])

# --- Overview ---
with tabs[0]:
    st.subheader("📊 Summary Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Max Temp (°C)", f"{weather_filtered['temperature_2m_max'].mean():.1f}")
        st.metric("Total Rainfall (mm)", f"{weather_filtered['precipitation_sum'].sum():.1f}")
    with col2:
        st.metric("Disease Cases Reported", disease_filtered["Cases"].sum())
        st.metric("Data Range", f"{start_date} to {end_date}")

# --- Disease Trends ---
with tabs[1]:
    st.subheader("📈 Disease Trends Over Time")
    yearly = disease_filtered.groupby("Date")["Cases"].sum().reset_index()
    fig = px.bar(yearly, x="Date", y="Cases",
                title=f"{selected_disease} Cases in {selected_city}",
                color_discrete_sequence=["#4b6cb7"])
    st.plotly_chart(fig, use_container_width=True)

    fig3 = px.line(disease_df,x="Date",y="Cases",color="Disease",title="📈 Monthly Cases per Disease")
    st.plotly_chart(fig3, use_container_width=True)

    city_disease = disease_df.groupby(["District", "Disease"])["Cases"].sum().reset_index()
    fig4 = px.bar(city_disease,x="District",y="Cases",color="Disease",title="🏙️ Total Cases by Disease in Each City",barmode="group")
    st.plotly_chart(fig4, use_container_width=True)

# --- Climate Trends ---
with tabs[2]:
    st.subheader("🌤️ Climate Variables Over Time")
    fig = px.line(
        weather_filtered,
        x="time",
        y=["temperature_2m_max", "precipitation_sum", "relative_humidity_2m_max"],
        title=f"Weather Trends in {selected_city}"
    )
    st.plotly_chart(fig, use_container_width=True)

    weather_df["Date"] = pd.to_datetime(weather_df["time"])
    weather_df["Month"] = weather_df["Date"].dt.to_period("M").astype(str)

    climate_monthly = weather_df.groupby("Month").agg({"temperature_2m_max": "mean","relative_humidity_2m_max": "mean","precipitation_sum": "sum"}).reset_index()
    fig1 = px.line(climate_monthly, x="Month", y="temperature_2m_max",title="🌡️ Monthly Avg Max Temperature (All Cities)", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(climate_monthly, x="Month", y="precipitation_sum",title="🌧️ Total Monthly Rainfall",color_discrete_sequence=["#2a9df4"])
    st.plotly_chart(fig2, use_container_width=True)


# --- Correlation ---
with tabs[3]:
    st.subheader("📊 Climate vs Disease Correlation")

    weather_filtered["Date"] = weather_filtered["time"].dt.year
    disease_filtered["Date"] = disease_filtered["Date"].dt.year
    # Define coordinates for Indian districts
    district_coords = {
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.7041, 77.1025),
        "Bengaluru": (12.9716, 77.5946),
        "Hyderabad": (17.3850, 78.4867),
        "Ahmedabad": (23.0225, 72.5714),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Pune": (18.5204, 73.8567),
        "Jaipur": (26.9124, 75.7873),
        "Lucknow": (26.8467, 80.9462)
    }
    joined = pd.merge(weather_filtered, disease_filtered, on="Date", how="inner")
    # Add Latitude and Longitude columns
    joined["Latitude"] = joined["District"].map(lambda x: district_coords.get(x, (None, None))[0])
    joined["Longitude"] = joined["District"].map(lambda x: district_coords.get(x, (None, None))[1])

    if not joined.empty:
        numeric_cols = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                        "rain_sum", "relative_humidity_2m_max", "relative_humidity_2m_min",
                        "windspeed_10m_max", "Cases"]
        available_cols = [col for col in numeric_cols if col in joined.columns]
        corr = joined[available_cols].corr()

        # Full styled heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                    linewidths=0.5, linecolor="black", square=True,
                    cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"}, ax=ax)
        ax.set_title(f"Correlation Heatmap ({selected_city} - {selected_disease})", fontsize=16, weight='bold')
        st.pyplot(fig)

        # # Correlation slider filter
        st.subheader("🔍 Filter Correlations with Disease Cases")
        corr_with_cases = corr["Cases"].drop("Cases", errors="ignore")
        threshold = st.slider("Minimum correlation with 'cases':", -1.0, 1.0, 0.3, 0.05)
        filtered_corr = corr_with_cases[abs(corr_with_cases) >= threshold]
        st.write("🧪 Variables with strong correlation to disease cases:")
        st.dataframe(filtered_corr.sort_values(ascending=False))

        # 📈 Climate-Disease Pairplot
        st.subheader("📈 Climate-Disease Pairplot")
        selected_features = st.multiselect(
        "Select features for pairplot:",
        available_cols,
        default=["temperature_2m_max", "precipitation_sum", "relative_humidity_2m_max", "Cases"]
    )
    if len(selected_features) >= 2:
        fig_pair = sns.pairplot(joined[selected_features], corner=True, plot_kws={'alpha': 0.5})
        st.pyplot(fig_pair)
    else:
        st.warning("Please select at least two features for the pairplot.")

    # Histogram
    fig_hist = px.histogram(disease_filtered, x="Cases", nbins=30,
                            title=f"Distribution of {selected_disease} Cases")
    st.plotly_chart(fig_hist, use_container_width=True)

    # Line: Temp vs Cases
    if "temperature_2m_max" in joined.columns:
        fig_line = px.line(joined, x="Date", y=["temperature_2m_max", "Cases"],
                        title="Max Temperature vs Disease Cases Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

    # Scatter: Rain vs Cases
    if "precipitation_sum" in joined.columns:
        fig_scatter = px.scatter(joined, x="precipitation_sum", y="Cases",
                                title="Precipitation vs Disease Cases",
                                trendline="ols")
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- Map View ---
with tabs[4]:
    st.subheader("🗺️ Disease Intensity Heatmap")

    # Filter data to only valid rows
    heat_df = joined[["Latitude", "Longitude", "Cases", "Date"]].dropna()
    heat_df["Cases"] = pd.to_numeric(heat_df["Cases"], errors="coerce")

    # Allow user to pick month
    selected_month = st.selectbox("📅 Select Year", sorted(joined["Date"].unique()))

    # Filter just that month
    month_df = heat_df[heat_df["Date"] == selected_month]

    # Create folium map
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB positron")

    # Add heatmap layer
    HeatMap(
        data=month_df[["Latitude", "Longitude", "Cases"]].values,
        radius=15,
        max_zoom=10,
        blur=20,
        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 0.8: 'red', 1.0: 'darkred'}
    ).add_to(m)

    # Render map in Streamlit
    st_data = st_folium(m, width=700, height=500)

# --- Data Explorer ---
with tabs[5]:
    st.subheader("📁 Raw Data Viewer")
    st.write("### Weather Data")
    st.dataframe(weather_filtered)
    st.write("### Disease Data")
    st.dataframe(disease_filtered)
    if not joined.empty:
        st.download_button("Download Combined Data as CSV", data=joined.to_csv(index=False), file_name="climate2cure_data.csv")
