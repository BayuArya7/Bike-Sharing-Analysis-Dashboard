import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_data = pd.read_csv('dashboard/day_preprocessed.csv')
hour_data = pd.read_csv('dashboard/hour_preprocessed.csv')

# Set title for the dashboard
st.title('Bike Sharing Analysis Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
season = st.sidebar.selectbox('Select Season', day_data['season'].unique())
weather = st.sidebar.selectbox('Select Weather Condition', day_data['weathersit'].unique())

# Filter data based on sidebar inputs
filtered_day_data = day_data[(day_data['season'] == season) & (day_data['weathersit'] == weather)]

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(['Overview', 'Hourly Analysis', 'Weather Impact'])

# Tab 1: Overview
with tab1:
    st.subheader(f'Daily Overview for {season} with {weather}')
    
    # Show line chart for total count per day
    st.line_chart(filtered_day_data[['dteday', 'cnt']].set_index('dteday'))
    
    # Bar chart for casual and registered users
    st.subheader('Casual vs Registered Users')
    fig, ax = plt.subplots()
    filtered_day_data[['casual', 'registered']].plot(kind='bar', stacked=True, ax=ax)
    plt.xticks(rotation=90, fontsize=5)  # Rotate the x-axis labels for better readability
    st.pyplot(fig)
    
    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(filtered_day_data[['temp', 'hum', 'windspeed', 'cnt']].describe())

# Tab 2: Hourly Analysis
with tab2:
    st.subheader('Hourly Analysis')
    
    # Show the user a slider to filter by hour
    hour = st.slider('Select Hour', 0, 23, 12)
    
    # Filter hour dataset
    hourly_filtered_data = hour_data[hour_data['hr'] == hour]
    
    # Line chart for hourly trends based on selected hour
    st.line_chart(hourly_filtered_data[['dteday', 'cnt']].set_index('dteday'))
    
    # Heatmap to show hour vs weekday rental patterns
    st.subheader('Hourly Rental Patterns (Heatmap)')
    pivot_table = hour_data.pivot_table(values='cnt', index='hr', columns='weekday', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt='.1f', ax=ax)
    st.pyplot(fig)

# Tab 3: Weather Impact
with tab3:
    st.subheader('Impact of Weather on Rentals')
    
    # Filter data for analysis
    weather_data = day_data.groupby('weathersit')['cnt'].mean().reset_index()
    
    # Bar chart to show the impact of weather
    fig, ax = plt.subplots()
    sns.barplot(data=weather_data, x='weathersit', y='cnt', ax=ax)
    ax.set_title('Average Bike Rentals by Weather Condition')
    st.pyplot(fig)
    
    # Correlation heatmap for weather-related variables
    st.subheader('Correlation of Weather Variables')
    corr_matrix = day_data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Run the app with: streamlit run <your_script_name>.py
