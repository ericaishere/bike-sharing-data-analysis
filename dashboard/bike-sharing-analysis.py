import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For alternative visualizations (optional)
import numpy as np
import streamlit as st
import plotly.express as px

bike_df = pd.read_csv('https://raw.githubusercontent.com/ericaishere/bike-sharing-data-analysis/main/dashboard/bikesharing_df.csv')
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Sidebar untuk memilih rentang waktu
min_date = bike_df['dteday'].min()
max_date = bike_df['dteday'].max()

with st.sidebar:
    st.header('Analisis Data Bike Sharing')
    st.image('https://static.thenounproject.com/png/410860-200.png')

    start_date, end_date = st.date_input(
        label='Pilih rentang waktu:', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter data berdasarkan rentang waktu yang dipilih
main_df = bike_df[(bike_df['dteday'] >= str(start_date)) & 
                 (bike_df['dteday'] <= str(end_date))]

# Menghitung total penyewaan dan penyewa
total_rent = main_df['cnt_day'].sum()
casual_renter = main_df['casual_day'].sum()
registered_renter = main_df['registered_day'].sum()


# Function to calculate monthly average rentals 
def calculate_monthly_avg_rent(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })

    monthly_rent_df.index = monthly_rent_df.index.strftime('%Y-%m')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_renter',
        'registered_day': 'registered_renter'
    }, inplace=True)

    return monthly_rent_df

# Function to calculate seasonal average rentals 
def calculate_seasonal_avg_rent(df):
    seasonal_rent_df = df.groupby('season_day').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })
    seasonal_rent_df = seasonal_rent_df.reset_index()
    seasonal_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_renter',
        'registered_day': 'registered_renter'
    }, inplace=True)

    return seasonal_rent_df

# Function to calculate hourly average rentals
def calculate_hourly_avg_rent(df):
    hourly_rent_df = df.groupby('hr').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })
    hourly_rent_df = hourly_rent_df.reset_index()
    hourly_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_renter',
        'registered_day': 'registered_renter'
    }, inplace=True)

    return hourly_rent_df

# Function to calculate seasonal average rentals without date 
def calculate_seasonal_avg_rent_no_date(df):
    seasonal_rent_no_date_df = df[['season_day', 'cnt_day']].groupby('season_day')['cnt_day'].mean()
    seasonal_rent_no_date_df = seasonal_rent_no_date_df.reset_index()
    return seasonal_rent_no_date_df

# Function to calculate weather average rentals without date
def calculate_weather_avg_rent_no_date(df):
    weather_rent_no_date_df = df[['weathersit_day', 'cnt_day']].groupby('weathersit_day')['cnt_day'].mean()
    weather_rent_no_date_df = weather_rent_no_date_df.reset_index()
    return weather_rent_no_date_df

# Function to calculate hourly rentals by season
def calculate_hourly_rent_by_season(df, season):
    hourly_rent_by_season_df = df[['season_hour', 'hr', 'cnt_hour']]
    hourly_rent_by_season_df = hourly_rent_by_season_df[hourly_rent_by_season_df['season_hour'] == season].groupby(['season_hour', 'hr'])['cnt_hour'].mean()
    hourly_rent_by_season_df = hourly_rent_by_season_df.reset_index()
    return hourly_rent_by_season_df



# Menghitung rata-rata penyewaan per bulan, musim, dan jam
monthly_rent_df = calculate_monthly_avg_rent(main_df)
seasonal_rent_df = calculate_seasonal_avg_rent(main_df)
hourly_rent_df = calculate_hourly_avg_rent(main_df)

# Menghitung rata-rata penyewaan per musim dan cuaca tanpa tanggal
seasonal_rent_no_date_df = calculate_seasonal_avg_rent_no_date(bike_df)
weather_rent_no_date_df = calculate_weather_avg_rent_no_date(bike_df)

# Menampilkan informasi dashboard
st.header('Bike Sharing Dashboard')
st.markdown("""
- **Nama:** Hendrika Rosa Vincensia Kaluge
- **Email:** erikakaluge175@gmail.com
- **ID Dicoding:** erika_kaluge
""")

# Menampilkan total penyewaan dan penyewa
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Penyewaan', '{:,.0f}'.format(total_rent).replace(',', '.'))
with col2:
    st.metric('Total Penyewa Kasual', '{:,.0f}'.format(casual_renter).replace(',', '.'))
with col3:
    st.metric('Total Penyewa Terdaftar', '{:,.0f}'.format(registered_renter).replace(',', '.'))

# Tab untuk visualisasi utama dan tambahan
tab1, tab2 = st.tabs(['Visualisasi Utama', 'Visualisasi Lainnya'])

# Visualisasi Utama
with tab1:
    st.subheader('Visualisasi Utama ')
    st.write('***\*Gunakan date input pada sidebar untuk mengatur visualisasi***')

    # Grafik rata-rata penyewaan per bulan
    monthly_rent_chart = px.line(
        monthly_rent_df,
        x='dteday',
        y=['total_rental', 'casual_renter', 'registered_renter'],
        color_discrete_sequence = px.colors.qualitative.Pastel,
        title='Rata-rata Penyewaan Sepeda per Bulan',
        markers=True
    )
    st.plotly_chart(monthly_rent_chart.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewaan (Rata-rata)'))

    # Grafik rata-rata penyewaan per musim
    seasonal_rent_chart = px.bar(
        seasonal_rent_df,
        x='season_day',
        y=["casual_renter", "registered_renter"],
        title='Rata-rata Penyewaan Sepeda per Musim (Berdasarkan Tanggal)',
        color_discrete_sequence = px.colors.qualitative.Pastel

    )
    st.plotly_chart(seasonal_rent_chart.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Penyewaan (Rata-rata)'))

    # Grafik rata-rata penyewaan per jam
    hourly_rent_chart = px.bar(
        hourly_rent_df,
        x='hr',
        y=["casual_renter", "registered_renter"],
        title='Rata-rata Penyewaan Sepeda per Jam (Berdasarkan Tanggal)',
        color_discrete_sequence = px.colors.qualitative.Pastel

    )
    st.plotly_chart(hourly_rent_chart.update_layout(xaxis_title='Jam', yaxis_title='Jumlah Penyewaan (Rata-rata)'))

# Visualisasi Lainnya
with tab2:
    st.subheader('Visualisasi Lainnya ')

    # Grafik rata-rata penyewaan per musim tanpa tanggal
    seasonal_rent_no_date_chart = px.bar(
        seasonal_rent_no_date_df,
        x='season_day',
        y='cnt_day',
        color='season_day',
        title='Rata-rata Penyewaan Sepeda per Musim'
    )
    st.plotly_chart(seasonal_rent_no_date_chart.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Rata-rata'))

    # Grafik rata-rata penyewaan per cuaca tanpa tanggal
    weather_rent_no_date_chart = px.bar(
        weather_rent_no_date_df,
        x='weathersit_day',
        y='cnt_day',
        color='weathersit_day',
        title='Rata-rata Penyewaan Sepeda per Cuaca'
    )
    st.plotly_chart(weather_rent_no_date_chart.update_layout(xaxis_title='Cuaca', yaxis_title='Jumlah Rata-rata'))

    # Memilih musim untuk melihat rata-rata penyewaan per jam
    season = st.selectbox(
        label="Pilih jenis musim:",
        options=('Fall', 'Spring', 'Summer', 'Winter')
    )

    # Menghitung rata-rata penyewaan per jam berdasarkan musim yang dipilih
    color_palette = {
    'Fall': ['#FFC0CB', '#ADD8E6'],
    'Spring': ['#BDB7ED', '#FFEBEE'],
    'Summer': ['#FF9999', '#FFFFCC'],
    'Winter': ['#C2C2F0', '#AACCFF']
    }


    color = color_palette.get(season, 'pink')

    hourly_rent_by_season_df = calculate_hourly_rent_by_season(bike_df, season)
    hourly_rent_by_season_chart = px.bar(
        hourly_rent_by_season_df,
        x='hr',
        y='cnt_hour',
        color_discrete_sequence=[color],
        title=f'Rata-rata Jumlah Penyewaan Sepeda per Jam berdasarkan Musim ({season})'
    )
    st.plotly_chart(hourly_rent_by_season_chart.update_layout(xaxis_title='Jam', yaxis_title='Jumlah Rata-rata'))

st.caption('Copyright © 2023')

