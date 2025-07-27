import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import HeatMap

# --- Page Configuration ---
st.set_page_config(page_title="Climate2Cure Dashboard", layout="wide")

# --- Custom CSS Styling (New Theme) ---
st.markdown("""
    <style>
        /* Main content area styling for better readability */
        .main .block-container {
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            padding: 2rem;
            color: #FFFFFF;
        }

        /* Text colors */
        h1, h2, h3 {
            color: #64C7FF; /* A bright, techy blue */
        }
        
        .stMarkdown, .stMetric, .stDataFrame, .stSelectbox, .stDateInput {
            color: #FFFFFF;
        }

        /* Metric styling */
        .stMetric .metric-label {
            color: #A9A9A9; /* Lighter grey for metric labels */
        }
        
        .stMetric .st-ax {
             color: #FFFFFF !important;
        }

        /* Tab styling for a modern look */
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            color: #A9A9A9;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 0, 0, 0.2);
            color: #64C7FF !important;
            font-weight: bold;
            border-bottom: 2px solid #64C7FF;
        }

        /* Sidebar styling */
        .st-emotion-cache-16txtl3 {
             background-color: rgba(0, 0, 0, 0.7);
             border-right: 1px solid #64C7FF;
        }
        
        /* Plotly chart background */
        .js-plotly-plot .plotly, .js-plotly-plot .plotly-graph-div {
            background-color: transparent !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center; color: #64C7FF;'>🦠 Climate2Cure: Exploring Climate-Disease Correlation</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #64C7FF;'>", unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads and preprocesses the datasets."""
    # Load data from CSV files
    weather = pd.read_csv("weather_2020_2025.csv", parse_dates=["time"])
    disease = pd.read_csv("monthly_disease_cases_2020_2025.csv")
    
    # Coerce date columns to datetime objects, handling any errors
    weather["time"] = pd.to_datetime(weather["time"], errors="coerce")
    disease["Date"] = pd.to_datetime(disease["Date"], errors="coerce")
    
    # Create a 'YearMonth' column for merging
    weather['YearMonth'] = weather['time'].dt.to_period('M')
    disease['YearMonth'] = disease['Date'].dt.to_period('M')
    
    return weather, disease

weather_df, disease_df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

# Get unique sorted lists for dropdowns
cities = sorted(disease_df["District"].unique())
diseases = sorted(disease_df["Disease"].unique())

# Sidebar widgets
selected_city = st.sidebar.selectbox("Select City", cities)
selected_disease = st.sidebar.selectbox("Select Disease", diseases)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-06-30"))

# --- Data Filtering ---
# Filter weather data based on sidebar selections
weather_filtered = weather_df[
    (weather_df["city"] == selected_city) &
    (weather_df["time"] >= pd.to_datetime(start_date)) &
    (weather_df["time"] <= pd.to_datetime(end_date))
]

# Filter disease data based on sidebar selections
disease_filtered = disease_df[
    (disease_df["Disease"] == selected_disease) &
    (disease_df["District"].str.lower() == selected_city.lower()) &
    (disease_df["Date"] >= pd.to_datetime(start_date)) &
    (disease_df["Date"] <= pd.to_datetime(end_date))
]

# --- Tabs ---
tabs = st.tabs(["📊 Overview", "🦠 Disease Trends", "🌡️ Climate Trends",
                "📈 Correlation","📍 Map View",  "📁 Data Explorer"])

# --- Overview Tab ---
with tabs[0]:
    st.subheader(f"📊 Summary for {selected_city}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Max Temp (°C)", f"{weather_filtered['temperature_2m_max'].mean():.1f}")
        st.metric("Avg Min Temp (°C)", f"{weather_filtered['temperature_2m_min'].mean():.1f}")
    with col2:
        st.metric("Total Rainfall (mm)", f"{weather_filtered['precipitation_sum'].sum():.1f}")
        st.metric("Avg Max Humidity (%)", f"{weather_filtered['relative_humidity_2m_max'].mean():.1f}")
    with col3:
        st.metric("Total Disease Cases", f"{disease_filtered['Cases'].sum():,}")
        st.metric("Data Range", f"{start_date.strftime('%b %Y')} to {end_date.strftime('%b %Y')}")

# --- Disease Trends Tab ---
with tabs[1]:
    st.subheader("📈 Disease Trends Over Time")
    if not disease_filtered.empty:
        fig = px.bar(disease_filtered, x="Date", y="Cases",
                     title=f"{selected_disease} Cases in {selected_city}",
                     color_discrete_sequence=["#64C7FF"])
        fig.update_layout(xaxis_title="Date", yaxis_title="Number of Cases", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for {selected_disease} in {selected_city} for the selected date range.")

    st.markdown("---")
    st.subheader("🌐 Broader Disease Trends")
    
    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.line(disease_df, x="Date", y="Cases", color="Disease", title="📈 Monthly Cases per Disease (All Cities)")
        fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        city_disease = disease_df.groupby(["District", "Disease"])["Cases"].sum().reset_index()
        fig4 = px.bar(city_disease, x="District", y="Cases", color="Disease", title="🏙️ Total Cases by Disease in Each City", barmode="group")
        fig4.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)

# --- Climate Trends Tab ---
with tabs[2]:
    st.subheader(f"🌤️ Climate Variables Over Time in {selected_city}")
    fig = px.line(
        weather_filtered,
        x="time",
        y=["temperature_2m_max", "precipitation_sum", "relative_humidity_2m_max"],
        title=f"Daily Weather Trends in {selected_city}",
        labels={"value": "Value", "time": "Date", "variable": "Metric"}
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🗓️ Monthly Climate Aggregates (All Cities)")
    
    climate_monthly = weather_df.groupby(weather_df['time'].dt.to_period('M').astype(str)).agg({
        "temperature_2m_max": "mean",
        "relative_humidity_2m_max": "mean",
        "precipitation_sum": "sum"
    }).reset_index()
    climate_monthly.rename(columns={'time': 'Month'}, inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(climate_monthly, x="Month", y="temperature_2m_max", title="🌡️ Monthly Avg Max Temperature", markers=True)
        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(climate_monthly, x="Month", y="precipitation_sum", title="🌧️ Total Monthly Rainfall", color_discrete_sequence=["#2a9df4"])
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

# --- Correlation Tab ---
with tabs[3]:
    st.subheader("📊 Climate vs. Disease Correlation Analysis")
    st.info(f"This analysis correlates monthly aggregated weather data with monthly cases of **{selected_disease}** in **{selected_city}**.")

    weather_monthly_agg = weather_filtered.groupby('YearMonth').agg(
        temperature_2m_max=('temperature_2m_max', 'mean'),
        temperature_2m_min=('temperature_2m_min', 'mean'),
        precipitation_sum=('precipitation_sum', 'sum'),
        rain_sum=('rain_sum', 'sum'),
        relative_humidity_2m_max=('relative_humidity_2m_max', 'mean'),
        relative_humidity_2m_min=('relative_humidity_2m_min', 'mean'),
        windspeed_10m_max=('windspeed_10m_max', 'mean')
    ).reset_index()

    if 'YearMonth' not in disease_filtered.columns:
        disease_filtered['YearMonth'] = disease_filtered['Date'].dt.to_period('M')
        
    joined_df = pd.merge(
        weather_monthly_agg,
        disease_filtered[['YearMonth', 'Cases']],
        on='YearMonth',
        how='inner'
    )

    if not joined_df.empty:
        numeric_cols = [
            "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
            "rain_sum", "relative_humidity_2m_max", "relative_humidity_2m_min",
            "windspeed_10m_max", "Cases"
        ]
        available_cols = [col for col in numeric_cols if col in joined_df.columns]
        
        corr = joined_df[available_cols].corr()

        st.write("#### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_alpha(0) # Transparent background for the figure
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0,
                    linewidths=0.5, linecolor="black", square=True,
                    cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"}, ax=ax)
        ax.set_facecolor('none') # Transparent background for the axes
        ax.tick_params(colors='white')
        plt.title(f"Correlation Heatmap ({selected_city} - {selected_disease})", color='white', fontsize=16, weight='bold')
        plt.ylabel(ax.get_ylabel(), color='white')
        plt.xlabel(ax.get_xlabel(), color='white')
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='white')
        cbar.set_label("Correlation Coefficient", color='white')
        st.pyplot(fig)
        
        st.markdown("---")
        
        st.write("#### Climate-Disease Pairplot")
        selected_features = st.multiselect(
            "Select features for pairplot:",
            available_cols,
            default=[col for col in ["temperature_2m_max", "precipitation_sum", "relative_humidity_2m_max", "Cases"] if col in available_cols]
        )
        if len(selected_features) >= 2:
            # Set seaborn style for dark theme
            sns.set_style("darkgrid", {"axes.facecolor": ".15", "grid.color": ".2", "xtick.color": "white", "ytick.color": "white", "axes.labelcolor": "white"})
            pair_fig = sns.pairplot(joined_df[selected_features], corner=True, plot_kws={'alpha': 0.7, 'color': '#64C7FF'}, diag_kws={'color': '#64C7FF'})
            pair_fig.fig.patch.set_alpha(0)
            st.pyplot(pair_fig)
        else:
            st.warning("Please select at least two features for the pairplot.")

    else:
        st.warning("No overlapping monthly data found for the selected city, disease, and date range to perform correlation analysis.")

# --- Map View Tab ---
with tabs[4]:
    st.subheader("🗺️ Disease Intensity Heatmap")
    st.info("The map shows the total cases for each disease across all available cities for a selected month.")
    
    district_coords = {
        "Mumbai": (19.0760, 72.8777), "Delhi": (28.7041, 77.1025),
        "Bengaluru": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
        "Ahmedabad": (23.0225, 72.5714), "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639), "Pune": (18.5204, 73.8567),
        "Jaipur": (26.9124, 75.7873), "Lucknow": (26.8467, 80.9462)
    }
    
    map_data = disease_df.copy()
    map_data["Latitude"] = map_data["District"].map(lambda x: district_coords.get(x, (None, None))[0])
    map_data["Longitude"] = map_data["District"].map(lambda x: district_coords.get(x, (None, None))[1])
    map_data.dropna(subset=['Latitude', 'Longitude', 'Cases'], inplace=True)
    map_data['YearMonthStr'] = map_data['YearMonth'].astype(str)

    available_months = sorted(map_data["YearMonthStr"].unique())
    selected_month_str = st.selectbox("📅 Select Month", options=available_months, index=len(available_months)-1)

    month_df = map_data[map_data["YearMonthStr"] == selected_month_str]

    # Use a dark map tile
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB dark_matter")

    if not month_df.empty:
        HeatMap(
            data=month_df[["Latitude", "Longitude", "Cases"]].values,
            radius=25,
            max_zoom=10,
            blur=15,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
        ).add_to(m)
        
        for idx, row in month_df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='#64C7FF',
                fill=True,
                fill_color='#64C7FF',
                fill_opacity=0.7,
                popup=f"<div style='background-color: #2b2b2b; color: white; padding: 5px; border-radius: 3px;'>{row['District']}<br>{row['Disease']}: {row['Cases']} cases</div>"
            ).add_to(m)
    
    st_folium(m, width=700, height=500, use_container_width=True)

# --- Data Explorer Tab ---
with tabs[5]:
    st.subheader("📁 Raw Data Viewer")
    st.write("Explore the filtered datasets used in the dashboard.")
    
    st.write("### Weather Data (Filtered)")
    st.dataframe(weather_filtered)
    
    st.write("### Disease Data (Filtered)")
    st.dataframe(disease_filtered)
    
    if 'joined_df' in locals() and not joined_df.empty:
        csv = joined_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Combined Monthly Data as CSV",
            data=csv,
            file_name=f"climate2cure_data_{selected_city}_{selected_disease}.csv",
            mime="text/csv",
        )
