import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import HeatMap
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Climate2Cure Dashboard", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1554141322-a0d3421d0793?q=80&w=2070&auto=format&fit=crop");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
        }

        .main .block-container {
            background-color: rgba(10, 25, 47, 0.8);
            border-radius: 10px;
            padding: 2rem;
            color: #E0E0E0;
            border: 1px solid #00A896;
        }

        h1, h2, h3, h4 {
            color: #00A896;
        }
        
        .stMarkdown, .stMetric, .stDataFrame, .stSelectbox, .stDateInput {
            color: #E0E0E0;
        }

        .stMetric .metric-label {
            color: #A9A9A9;
        }
        
        .stMetric .st-ax {
             color: #FFFFFF !important;
        }

        .st-emotion-cache-16txtl3 {
             background-color: rgba(10, 25, 47, 0.9);
             border-right: 1px solid #00A896;
        }
        
        .stRadio > label {
            font-size: 1.1em;
            font-weight: bold;
            color: #00A896;
        }
        
        .js-plotly-plot .plotly, .js-plotly-plot .plotly-graph-div {
            background-color: transparent !important;
        }
        
        .st-expander > summary {
            font-size: 1.1em;
            color: #00A896;
        }
        
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
            color: #00A896 !important;
            font-weight: bold;
            border-bottom: 2px solid #00A896;
        }

    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    weather = pd.read_csv("project/weather_2020_2025.csv", parse_dates=["time"])
    disease = pd.read_csv("project/monthly_disease_cases_2020_2025.csv")
    
    weather["time"] = pd.to_datetime(weather["time"], errors="coerce")
    disease["Date"] = pd.to_datetime(disease["Date"], errors="coerce")
    
    weather['YearMonth'] = weather['time'].dt.to_period('M')
    disease['YearMonth'] = disease['Date'].dt.to_period('M')
    
    disease['YearMonthStr'] = disease['YearMonth'].astype('str')
    
    return weather, disease

weather_df, disease_df = load_data()

# --- Sidebar ---
st.sidebar.title("Climate2Cure")
st.sidebar.markdown("---")

# Initialize Session State for Filters
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = sorted(disease_df["District"].unique())[0]
    st.session_state.selected_disease = sorted(disease_df["Disease"].unique())[0]
    st.session_state.start_date = pd.to_datetime("2020-01-01").date()
    st.session_state.end_date = pd.to_datetime("2025-06-30").date()

# Navigation
page = st.sidebar.radio("Navigation", ["Home", "Filter & Insights", "EDA", "Info", "Contact"])
st.sidebar.markdown("---")

# --- CONDITIONAL FILTER WIDGETS ---
if page in ["Filter & Insights", "EDA"]:
    st.sidebar.header("🔍 Analysis Filters")

    cities = sorted(disease_df["District"].unique())
    st.sidebar.selectbox("Select City", cities, key='selected_city')

    diseases = sorted(disease_df["Disease"].unique())
    st.sidebar.selectbox("Select Disease", diseases, key='selected_disease')

    st.sidebar.date_input("Start Date", value=st.session_state.start_date, key='start_date')
    st.sidebar.date_input("End Date", value=st.session_state.end_date, key='end_date')

    st.sidebar.markdown("---")
# ----------------------------------

# ----------------------------------------------------------------------
# --- Page Definitions ---
# ----------------------------------------------------------------------

# --- Home Page ---
def home_page():
    st.markdown("<h1 style='text-align: center;'>🦠 Welcome to Climate2Cure</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #E0E0E0;'>Exploring the Nexus of Climate and Public Health</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Our Mission")
    st.write("""
    The Climate2Cure initiative aims to illuminate the complex relationships between climatic conditions and the prevalence of various diseases. By providing an intuitive, data-driven platform, we empower researchers, public health officials, and curious minds to explore potential environmental factors that influence health outcomes across India.
    """)

    st.subheader("Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📈 Analyze Trends")
        st.write("Visualize disease case trends over time and compare them with fluctuating climate variables like temperature and rainfall.")
    with col2:
        st.markdown("#### 🔗 Explore Correlations")
        st.write("Use interactive heatmaps and plots to investigate statistical correlations between specific diseases and weather patterns.")
    with col3:
        st.markdown("#### 🗺️ Visualize Hotspots")
        st.write("Identify geographical hotspots of disease outbreaks with an interactive map view, updated monthly.")

    st.markdown("---")

# --- Filter & Insights Page ---
def filter_insights_page(weather_df, disease_df):
    st.markdown("<h1 style='text-align: center;'>🔍 Filter & Insights Setup</h1>", unsafe_allow_html=True)
    st.markdown("---")

    selected_city = st.session_state.selected_city
    selected_disease = st.session_state.selected_disease
    start_date_dt = pd.to_datetime(st.session_state.start_date)
    end_date_dt = pd.to_datetime(st.session_state.end_date)
    
    weather_filtered = weather_df[
        (weather_df["city"] == selected_city) &
        (weather_df["time"] >= start_date_dt) &
        (weather_df["time"] <= end_date_dt)
    ].copy()

    disease_filtered = disease_df[
        (disease_df["Disease"] == selected_disease) &
        (disease_df["District"].str.lower() == selected_city.lower()) &
        (disease_df["Date"] >= start_date_dt) &
        (disease_df["Date"] <= end_date_dt)
    ].copy()

    disease_filtered_all_cities = disease_df[
        (disease_df["Date"] >= start_date_dt) &
        (disease_df["Date"] <= end_date_dt)
    ].copy()


    weather_monthly_agg = weather_filtered.groupby('YearMonth').agg(
        temperature_2m_max=('temperature_2m_max', 'mean'),
        precipitation_sum=('precipitation_sum', 'sum'),
        relative_humidity_2m_max=('relative_humidity_2m_max', 'mean'),
        Date=('time', 'max') 
    ).reset_index()

    joined_df = pd.merge(
        weather_monthly_agg,
        disease_filtered[['YearMonth', 'Cases']], 
        on='YearMonth',
        how='inner'
    )
    
    if not joined_df.empty:
        peak_disease = joined_df.loc[joined_df['Cases'].idxmax()]
        
        corr_matrix = joined_df[['temperature_2m_max', 'precipitation_sum', 'relative_humidity_2m_max', 'Cases']].corr()
        case_corr = corr_matrix['Cases'].drop('Cases').abs()
        max_corr_var = case_corr.idxmax()
        max_corr_value = corr_matrix.loc[max_corr_var, 'Cases']
        max_corr_sign = 'Positive' if max_corr_value > 0 else 'Negative'
        max_corr_name = max_corr_var.replace('_', ' ').title()
        
        total_cases_by_city = disease_filtered_all_cities.groupby('District')['Cases'].sum().reset_index()
        total_cases_by_city['Rank'] = total_cases_by_city['Cases'].rank(ascending=False, method='min')
        city_rank_data = total_cases_by_city[total_cases_by_city['District'] == selected_city]
        city_rank = int(city_rank_data['Rank'].iloc[0]) if not city_rank_data.empty and not city_rank_data['Rank'].isna().all() else None
        total_cities = len(total_cases_by_city)
    else:
        peak_disease = None
        max_corr_value = None
        max_corr_sign = 'N/A'
        max_corr_name = 'N/A'
        city_rank = None
        total_cities = len(disease_df["District"].unique())

    expected_days = (end_date_dt - start_date_dt).days + 1
    actual_days = weather_filtered.shape[0]
    data_coverage = (actual_days / expected_days) * 100 if expected_days > 0 else 0


    # --- INSIGHTS TABS ---
    st.subheader(f"Summary for: {selected_disease} in {selected_city}")
    tabs = st.tabs(["📊 Overview", "🦠 Disease Trends", "🌡️ Climate Trends"])

    # --- Overview Tab ---
    with tabs[0]:
        st.subheader(f"📊 Key Metrics for {selected_city}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Disease Cases", f"{disease_filtered['Cases'].sum():,}")
            if peak_disease is not None:
                st.metric("Peak Case Month", 
                          f"{int(peak_disease['Cases']):,} cases",
                          help=f"Occurred in {peak_disease['YearMonth']}"
                          )
            
        with col2:
            st.metric("Avg Max Temp (°C)", f"{weather_filtered['temperature_2m_max'].mean():.1f}")
            st.metric("Total Rainfall (mm)", f"{weather_filtered['precipitation_sum'].sum():.1f}")

        with col3:
            st.metric("Data Range (Months)", f"{joined_df.shape[0]} months")
            
            if max_corr_value is not None:
                st.metric(f"Highest Correlation", 
                          f"{max_corr_value:.2f}",
                          help=f"{max_corr_sign} relationship with {max_corr_name}"
                          )
            else:
                 st.metric("Highest Correlation", "N/A", help="Requires overlapping monthly data.")
        
        st.markdown("---")
        st.subheader("🌍 Comparative & Quality Metrics")

        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            if city_rank is not None:
                st.metric("Disease Severity Rank", f"#{city_rank}", help=f"Rank among {total_cities} cities for total {selected_disease} cases in the range.")
            else:
                st.metric("Disease Severity Rank", "N/A", help="Cannot calculate rank without case data.")
        
        with comp_col2:
            st.metric("Climate Data Coverage", f"{data_coverage:.1f}%", help=f"Actual days of weather data ({actual_days}) vs. expected days ({expected_days}).")


    # --- Disease Trends Tab ---
    with tabs[1]:
        st.subheader("📈 Disease Trends Over Time")
        if not disease_filtered.empty:
            fig = px.bar(disease_filtered, x="Date", y="Cases",
                         title=f"{selected_disease} Cases in {selected_city}",
                         color_discrete_sequence=["#00A896"])
            fig.update_layout(xaxis_title="Date", yaxis_title="Number of Cases", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data available for {selected_disease} in {selected_city} for the selected date range.")

        st.markdown("---")
        st.subheader("🌐 Broader Disease Trends (All Cities in Selected Range)")
        
        if not disease_filtered_all_cities.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig3 = px.line(
                    disease_filtered_all_cities, 
                    x="Date", 
                    y="Cases", 
                    color="Disease", 
                    title="📈 Total Monthly Cases per Disease (All Cities)",
                    height=400
                )
                fig3.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                city_disease = disease_filtered_all_cities.groupby(["District", "Disease"])["Cases"].sum().reset_index()
                
                if not city_disease.empty:
                    fig4 = px.bar(
                        city_disease, 
                        x="District", 
                        y="Cases", 
                        color="Disease", 
                        title="🏙️ Total Cases by Disease in Each City", 
                        barmode="group",
                        height=400
                    )
                    fig4.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("No data found for any disease in this date range.")
        else:
            st.warning("No disease data available nationally for the selected date range.")


    # --- Climate Trends Tab ---
    with tabs[2]:
        st.subheader(f"🌤️ Daily Climate Variables Over Time in {selected_city}")
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
        
        climate_monthly = weather_df.groupby('YearMonth').agg({
            "temperature_2m_max": "mean",
            "relative_humidity_2m_max": "mean",
            "precipitation_sum": "sum"
        }).reset_index()
        
        climate_monthly['Month'] = climate_monthly['YearMonth'].apply(lambda x: x.start_time)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(climate_monthly, x="Month", y="temperature_2m_max", title="🌡️ Monthly Avg Max Temperature", markers=True)
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.bar(climate_monthly, x="Month", y="precipitation_sum", title="🌧️ Total Monthly Rainfall", color_discrete_sequence=["#2a9df4"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

# --- EDA Visualization Page ---
def eda_visualization_page(weather_df, disease_df):
    
    selected_city = st.session_state.selected_city
    selected_disease = st.session_state.selected_disease
    start_date_dt = pd.to_datetime(st.session_state.start_date)
    end_date_dt = pd.to_datetime(st.session_state.end_date)
    
    st.markdown(f"<h1 style='text-align: center;'>📊 EDA: Deep Analysis</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader(f"Analyzing: {selected_disease} in {selected_city} ({start_date_dt.strftime('%Y')} - {end_date_dt.strftime('%Y')})")

    weather_filtered = weather_df[
        (weather_df["city"] == selected_city) &
        (weather_df["time"] >= start_date_dt) &
        (weather_df["time"] <= end_date_dt)
    ].copy()

    disease_filtered = disease_df[
        (disease_df["Disease"] == selected_disease) &
        (disease_df["District"].str.lower() == selected_city.lower()) &
        (disease_df["Date"] >= start_date_dt) &
        (disease_df["Date"] <= end_date_dt)
    ].copy()

    weather_monthly_agg = weather_filtered.groupby('YearMonth').agg(
        temperature_2m_max=('temperature_2m_max', 'mean'),
        temperature_2m_min=('temperature_2m_min', 'mean'),
        precipitation_sum=('precipitation_sum', 'sum'),
        relative_humidity_2m_max=('relative_humidity_2m_max', 'mean'),
        relative_humidity_2m_min=('relative_humidity_2m_min', 'mean'),
        windspeed_10m_max=('windspeed_10m_max', 'mean')
    ).reset_index()
        
    joined_df = pd.merge(
        weather_monthly_agg,
        disease_filtered[['YearMonth', 'Cases']], 
        on='YearMonth',
        how='inner'
    )

    # --- Visualization Tabs ---
    tabs = st.tabs(["📈 Correlation","🔗 Time-Series Overlay", "📍 Map View", "📁 Data Explorer"])

    # --- Correlation Tab ---
    with tabs[0]:
        st.subheader("📊 Climate vs. Disease Correlation Heatmap")

        if not joined_df.empty:
            numeric_cols = [
                "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                "relative_humidity_2m_max", "relative_humidity_2m_min",
                "windspeed_10m_max", "Cases"
            ]
            available_cols = [col for col in numeric_cols if col in joined_df.columns]
            
            corr = joined_df[available_cols].corr()

            fig, ax = plt.subplots(figsize=(10, 8))
            fig.patch.set_alpha(0)
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0,
                         linewidths=0.5, linecolor="black", square=True,
                         cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"}, ax=ax)
            ax.set_facecolor('none')
            ax.tick_params(colors='white')
            plt.title(f"Correlation Heatmap ({selected_city} - {selected_disease})", color='white', fontsize=16, weight='bold')
            plt.ylabel(ax.get_ylabel(), color='white')
            plt.xlabel(ax.get_xlabel(), color='white')
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='white')
            cbar.set_label("Correlation Coefficient", color='white')
            st.pyplot(fig)
            
            # --- Pairplot Section ---
            st.markdown("---")
            st.write("#### Climate-Disease Pairplot")
            
            selected_features = st.multiselect(
                "Select features for pairplot:",
                available_cols,
                default=[col for col in ["temperature_2m_max", "precipitation_sum", "relative_humidity_2m_max", "Cases"] if col in available_cols],
                key='pairplot_multiselect_eda'
            )
            
            if st.button("Generate Pairplot", key='generate_pairplot_eda'):
                if len(selected_features) >= 2:
                    sns.set_style("darkgrid", {"axes.facecolor": ".15", "grid.color": ".2", "xtick.color": "white", "ytick.color": "white", "axes.labelcolor": "white"})
                    pair_fig = sns.pairplot(joined_df[selected_features], corner=True, plot_kws={'alpha': 0.7, 'color': '#00A896'}, diag_kws={'color': '#00A896'})
                    
                    for ax_row in pair_fig.axes:
                        for ax in ax_row:
                            if ax:
                                ax.tick_params(axis='x', colors='white')
                                ax.tick_params(axis='y', colors='white')
                                ax.set_xlabel(ax.get_xlabel(), color='white')
                                ax.set_ylabel(ax.get_ylabel(), color='white')
                        
                    pair_fig.fig.patch.set_alpha(0)
                    st.pyplot(pair_fig)
                else:
                    st.warning("Please select at least two features for the pairplot.")

        else:
            st.warning("No overlapping monthly data found for the selected city, disease, and date range to perform correlation analysis.")

    # --- Time-Series Overlay Plot ---
    with tabs[1]:
        st.subheader("🔗 Disease Cases vs. Climate Variable Over Time")

        if not joined_df.empty:
            
            joined_df['Month'] = joined_df['YearMonth'].apply(lambda x: x.start_time)
            
            climate_options = {
                "Average Max Temperature (°C)": 'temperature_2m_max',
                "Total Precipitation (mm)": 'precipitation_sum',
                "Average Max Humidity (%)": 'relative_humidity_2m_max'
            }
            
            selected_climate_metric = st.selectbox(
                "Select Climate Variable to Overlay:",
                list(climate_options.keys()),
                key='overlay_metric_eda'
            )
            climate_col = climate_options[selected_climate_metric]

            fig_overlay = make_subplots(specs=[[{"secondary_y": True}]])

            fig_overlay.add_trace(
                go.Bar(x=joined_df['Month'], y=joined_df['Cases'], name=f'{selected_disease} Cases', marker_color='#00A896'),
                secondary_y=False,
            )

            fig_overlay.add_trace(
                go.Scatter(x=joined_df['Month'], y=joined_df[climate_col], name=selected_climate_metric, line=dict(color='#2a9df4', width=3)),
                secondary_y=True,
            )

            fig_overlay.update_layout(
                title_text=f'Monthly {selected_disease} Cases vs. {selected_climate_metric}',
                template="plotly_dark", 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                legend=dict(yanchor="top", y=1.1, xanchor="left", x=0.01)
            )

            fig_overlay.update_xaxes(title_text="Month")
            
            fig_overlay.update_yaxes(title_text=f"<b>{selected_disease} Cases</b>", secondary_y=False, title_font=dict(color='#00A896'))

            fig_overlay.update_yaxes(title_text=f"<b>{selected_climate_metric}</b>", secondary_y=True, title_font=dict(color='#2a9df4'))

            st.plotly_chart(fig_overlay, use_container_width=True)
            
        else:
            st.warning("No overlapping monthly data found to create the time-series overlay.")


    # --- Map View Tab ---
    with tabs[2]:
        st.subheader("🗺️ Disease Intensity Heatmap")
        
        district_coords = {
            "Mumbai": (19.0760, 72.8777), "Delhi": (28.7041, 77.1025),
            "Bengaluru": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
            "Ahmedabad": (23.0225, 72.5714), "Chennai": (13.0827, 80.2707),
            "Kolkata": (22.5726, 88.3639), "Pune": (18.5204, 73.8567),
            "Jaipur": (26.9124, 75.7873), "Lucknow": (26.8467, 80.9462)
        }
        
        map_data_filtered = disease_df[
            (disease_df["Disease"] == selected_disease) &
            (disease_df["Date"] >= start_date_dt) &
            (disease_df["Date"] <= end_date_dt)
        ].copy()
        
        map_data_agg = map_data_filtered.groupby('District')['Cases'].sum().reset_index()
        
        map_data_agg["Latitude"] = map_data_agg["District"].map(lambda x: district_coords.get(x, (None, None))[0])
        map_data_agg["Longitude"] = map_data_agg["District"].map(lambda x: district_coords.get(x, (None, None))[1])
        map_data_agg.dropna(subset=['Latitude', 'Longitude', 'Cases'], inplace=True)

        m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB dark_matter")

        if not map_data_agg.empty:
            heat_data = [[row['Latitude'], row['Longitude'], row['Cases']] for idx, row in map_data_agg.iterrows()]
            
            HeatMap(
                data=heat_data,
                radius=20,
                max_zoom=10,
                blur=15,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
            ).add_to(m)
            
            for idx, row in map_data_agg.iterrows():
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=row['Cases'] / map_data_agg['Cases'].max() * 15 + 5,
                    color='#00A896', 
                    fill=True,
                    fill_color='#00A896',
                    fill_opacity=0.7,
                    popup=f"<div style='background-color: #2b2b2b; color: white; padding: 5px; border-radius: 3px;'>{row['District']}<br>Total Cases: {row['Cases']}</div>"
                ).add_to(m)
        
        st_folium(m, width=700, height=500, use_container_width=True)
        if map_data_agg.empty:
             st.warning("No geographical data available for the selected disease and date range.")

    # --- Data Explorer Tab ---
    with tabs[3]:
        st.subheader("📁 Raw Data Viewer")
        st.write("Explore the filtered datasets used in the dashboard.")
        
        st.write("### Daily Weather Data (Filtered)")
        st.dataframe(weather_filtered)
        
        st.write("### Monthly Disease Data (Filtered)")
        st.dataframe(disease_filtered)
        
        if 'joined_df' in locals() and not joined_df.empty:
            csv = joined_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Combined Monthly Data as CSV",
                data=csv,
                file_name=f"climate2cure_data_{selected_city}_{selected_disease}.csv",
                mime="text/csv",
            )


# --- Info Page ---
def info_page():
    st.markdown("<h1 style='text-align: center;'>ℹ️ Project Information</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("About The Project")
    st.write("The Climate2Cure project is an open-source initiative developed to provide accessible tools for visualizing and analyzing public health and climate data. Built with Python and Streamlit, it demonstrates how modern data science libraries can be leveraged to uncover insights from complex datasets. Our goal is to foster a better understanding of environmental health and to provide a template for similar data exploration applications.")

    st.subheader("Methodology")
    st.write("""
    The analysis presented in this dashboard follows a straightforward data processing pipeline:
    1.  **Data Loading:** Climate and disease datasets are loaded from CSV files.
    2.  **Data Cleaning:** Timestamps are converted to a uniform datetime format.
    3.  **Data Aggregation:** For correlation analysis, the daily weather data is aggregated into monthly averages (for temperature, humidity) or sums (for precipitation) to match the monthly frequency of the disease case data.
    4.  **User-Driven Filtering:** The dashboard dynamically filters the data based on the city, disease, and date range selected by the user in the EDA section.
    5.  **Visualization:** Interactive charts and maps are generated using Plotly, Matplotlib/Seaborn, and Folium to present the data in an intuitive format.
    """)

    st.subheader("Data Sources & Disclaimer")
    st.write("""
    - **Climate Data:** Sourced from the Open-Meteo API. It includes daily metrics such as maximum/minimum temperature, precipitation sum, maximum/minimum relative humidity, and maximum wind speed.
    - **Disease Data:** The dataset is sourced from the **Kaggle platform**. The diseases and case counts are for illustrative purposes.
    
    **Disclaimer:** This dashboard is an educational tool and is not intended for medical or public health decision-making. The correlations shown do not imply causation.
    """)

# --- Contact Page ---
def contact_page():
    st.markdown("<h1 style='text-align: center;'>✉️ Contact Us</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Have questions, suggestions, or feedback? We'd love to hear from you!")
    st.write("**Project Lead:** Dilrose Singh")
    st.write("**Email:** dilrosehothi112@gmail.com")
    st.markdown("---")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thank you for your message! We will get back to you shortly.")

# --- Main App Logic ---
if page == "Home":
    home_page()
elif page == "Filter & Insights":
    filter_insights_page(weather_df, disease_df) 
elif page == "EDA":
    eda_visualization_page(weather_df, disease_df)
elif page == "Info":
    info_page()
elif page == "Contact":
    contact_page()