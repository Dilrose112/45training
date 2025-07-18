import streamlit as st
import pandas as pd
import plotly.express as px

# Sample dummy data generation
def load_data():
    dates = pd.date_range(start='2024-01-01', end='2024-01-10')
    locations = ['Delhi', 'Mumbai', 'Bangalore']
    data = []
    for loc in locations:
        for date in dates:
            data.append({
                'date': date,
                'location': loc,
                'temperature': 25 + (hash(loc+str(date)) % 5),
                'humidity': 60 + (hash(loc[::-1]+str(date)) % 10),
                'disease_cases': 20 + (hash(str(date)+loc) % 15)
            })
    return pd.DataFrame(data)

# Load data
df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
locations = df['location'].unique()
selected_location = st.sidebar.selectbox("Select Location", locations)
selected_date = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

# # Filter data
# if isinstance(selected_date, list) and len(selected_date) == 2:
#     start_date, end_date = selected_date
#     mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
# else:
#     mask = df['date'] == pd.to_datetime(selected_date)

# filtered_df = df[(df['location'] == selected_location) & mask]

# Title
st.title("🌍 Climate2Cure: Environmental Triggers of Illness")
st.markdown("Explore how weather patterns may correlate with disease outbreaks.")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Average Temperature (°C)", f"{df['temperature'].mean():.2f}")
col2.metric("Average Humidity (%)", f"{df['humidity'].mean():.2f}")
col3.metric("Total Disease Cases", df['disease_cases'].sum())

# Time series chart
fig = px.line(df, x='date', y=['temperature', 'humidity', 'disease_cases'],
              labels={"value": "Metric", "date": "Date"},
              title=f"Daily Trends in {selected_location}")
st.plotly_chart(fig)

# Correlation
corr = df[['temperature', 'humidity', 'disease_cases']].corr()
st.subheader("Correlation Matrix")
st.dataframe(corr.style.background_gradient(cmap='coolwarm'))

# Optional: Export
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data as CSV", csv, "climate2cure_data.csv", "text/csv")
