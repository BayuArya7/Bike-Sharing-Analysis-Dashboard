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
tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Hourly Analysis', 'Weather Impact', 'RFM Analysis'])

day_data['workingday_label'] = day_data['workingday'].replace({0: 'Weekend', 1: 'Weekday'})
hour_data['workingday_label'] = hour_data['workingday'].replace({0: 'Weekend', 1: 'Weekday'})

with tab1:
    st.subheader(f'Daily Overview for {season} with {weather}')
    
    # Show line chart for total count per day
    st.line_chart(filtered_day_data[['dteday', 'cnt']].set_index('dteday'))
    
    st.subheader('Total Bike Rentals (By Day): Weekdays vs Weekends')
    
    # Kelompokkan data berdasarkan workingday_label
    total_rentals_by_type = day_data.groupby('workingday_label').agg({'cnt': 'sum'}).reset_index()
    
    # Bar plot untuk workingday_label
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='workingday_label', y='cnt', data=total_rentals_by_type, ax=ax)
    ax.set_title('Total Bike Rentals (By Day): Weekdays vs Weekends')
    ax.set_xlabel('Jenis Hari')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)

    st.subheader('Total Bike Rentals (By Hour): Weekdays vs Weekends')
    
    total_rentals_by_type = hour_data.groupby('workingday_label').agg({'cnt': 'sum'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='workingday_label', y='cnt', data=total_rentals_by_type, ax=ax)
    ax.set_title('Total Bike Rentals (By Hour): Weekdays vs Weekends')
    ax.set_xlabel('Jenis Hari')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
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

# Tab 4: RFM Analysis
with tab4:
    st.subheader('RFM Analysis on Bike Rentals')

    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    max_date = day_data['dteday'].max()
    day_data['recency'] = (max_date - day_data['dteday']).dt.days
    
    frequency = day_data.groupby('dteday').agg({'cnt': 'sum'}).reset_index()
    
    monetary = day_data.groupby('dteday').agg({'cnt': 'sum'}).reset_index()

    rfm = day_data.groupby('dteday').agg({
        'recency': 'min',  
        'cnt': 'sum'       
    }).reset_index()

    # visualisasi heatmap untuk menampilkan hasil RFM
    st.subheader('RFM Heatmap (Recency, Frequency, Monetary)')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(rfm[['recency', 'cnt']].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
    
    # Summary RFM analysis
    st.subheader('RFM Summary')
    st.write(rfm.describe())
