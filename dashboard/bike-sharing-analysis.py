import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For alternative visualizations (optional)
import numpy as np
import streamlit as st
import plotly.express as px

bikesharing_df = pd.read_csv('https://raw.githubusercontent.com/ericaishere/bike-sharing-data-analysis/main/dashboard/bikesharing_df.csv')
bikesharing_df['dteday'] = pd.to_datetime(bikesharing_df['dteday'])

# Sidebar untuk memilih rentang waktu
min_date = bikesharing_df['dteday'].min()
max_date = bikesharing_df['dteday'].max()

with st.sidebar:
    st.header('Analisis Data Bike Sharing')
    st.image('https://static.thenounproject.com/png/410860-200.png')

    start_date, end_date = st.date_input(
        label='Pilih rentang waktu:', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter data berdasarkan rentang waktu yang dipilih
main_df = bikesharing_df[(bikesharing_df['dteday'] >= str(start_date)) & 
                 (bikesharing_df['dteday'] <= str(end_date))]

# Menghitung total penyewaan dan penyewa
total_rent = main_df['cnt_day'].sum()
casual_rent = main_df['casual_day'].sum()
registered_rent = main_df['registered_day'].sum()


# Function to calculate monthly average rentals 
def create_monthly_average_rent(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })

    monthly_rent_df.index = monthly_rent_df.index.strftime('%Y-%m')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_rent',
        'registered_day': 'registered_rent'
    }, inplace=True)

    return monthly_rent_df

# Function to calculate seasonal average rentals 
def create_seasonal_average_rental(df):
    seasonal_rent_df = df.groupby('season_day').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })
    seasonal_rent_df = seasonal_rent_df.reset_index()
    seasonal_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_rent',
        'registered_day': 'registered_rent'
    }, inplace=True)

    return seasonal_rent_df

# Function to calculate hourly average rentals
def create_hourly_average_rent(df):
    hourly_rent_df = df.groupby('hr').agg({
        'cnt_day': 'mean',
        'casual_day': 'mean',
        'registered_day': 'mean'
    })
    hourly_rent_df = hourly_rent_df.reset_index()
    hourly_rent_df.rename(columns={
        'cnt_day': 'total_rental',
        'casual_day': 'casual_rent',
        'registered_day': 'registered_rent'
    }, inplace=True)

    return hourly_rent_df

# Function to calculate seasonal average rentals without date 
def create_seasonal_average_rental_no_date(df):
    seasonal_rent_no_date_df = df[['season_day', 'cnt_day']].groupby('season_day')['cnt_day'].mean()
    seasonal_rent_no_date_df = seasonal_rent_no_date_df.reset_index()
    return seasonal_rent_no_date_df

# Function to calculate weather average rentals without date
def create_avg_rent_based_weathersit(df):
    weather_rent_no_date_df = df[['weathersit_day', 'cnt_day']].groupby('weathersit_day')['cnt_day'].mean()
    weather_rent_no_date_df = weather_rent_no_date_df.reset_index()
    return weather_rent_no_date_df

# Function to calculate hourly rentals by season
def create_hour_rent_based_workingday(df, workingday):
    hourly_rent_by_workingday_df = df[['workingday_hour', 'hr', 'cnt_hour']]
    hourly_rent_by_workingday_df = hourly_rent_by_workingday_df[hourly_rent_by_workingday_df['workingday_hour'] == workingday].groupby(['workingday_hour', 'hr'])['cnt_hour'].mean().reset_index()
    return hourly_rent_by_workingday_df




# Menghitung rata-rata penyewaan per bulan, musim, dan jam
monthly_rent_df = create_monthly_average_rent(main_df)
seasonal_rent_df = create_seasonal_average_rental(main_df)
hourly_rent_df = create_hourly_average_rent(main_df)

# Menghitung rata-rata penyewaan per musim dan cuaca tanpa tanggal
seasonal_rent_no_date_df = create_seasonal_average_rental_no_date(bikesharing_df)
weather_rent_no_date_df = create_avg_rent_based_weathersit(bikesharing_df)

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
    st.metric('Total Penyewa Kasual', '{:,.0f}'.format(casual_rent).replace(',', '.'))
with col3:
    st.metric('Total Penyewa Terdaftar', '{:,.0f}'.format(registered_rent).replace(',', '.'))

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
        y=['total_rental', 'casual_rent', 'registered_rent'],
        color_discrete_sequence = px.colors.qualitative.Pastel,
        title='Rata-rata Penyewaan Sepeda per Bulan',
        markers=True
    )
    st.plotly_chart(monthly_rent_chart.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewaan (Rata-rata)'))

    # Grafik rata-rata penyewaan per musim
    seasonal_rent_chart = px.bar(
        seasonal_rent_df,
        x='season_day',
        y=["casual_rent", "registered_rent"],
        title='Rata-rata Penyewaan Sepeda per Musim (Berdasarkan Tanggal)',
        color_discrete_sequence = px.colors.qualitative.Pastel

    )
    st.plotly_chart(seasonal_rent_chart.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Penyewaan (Rata-rata)'))

    # Grafik rata-rata penyewaan per jam
    hourly_rent_chart = px.bar(
        hourly_rent_df,
        x='hr',
        y=["casual_rent", "registered_rent"],
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

    
    workingday = st.selectbox(
        label="Pilih jenis hari:",
        options=('holiday', 'work')
    )

    # Menghitung rata-rata penyewaan per jam berdasarkan musim yang dipilih
    color_palette = {
        'holiday': px.colors.qualitative.Plotly[0],
        'work': px.colors.qualitative.Plotly[1],
    }
    color = color_palette.get(workingday, 'blue')
    hourly_rent_by_workingday_df = create_hour_rent_based_workingday(bikesharing_df, workingday)
    hourly_rent_by_workingday_chart = px.line(
    hourly_rent_by_workingday_df,
    x='hr',
    y='cnt_hour',
    color_discrete_sequence=[color],
    title=f'Average Bike Rental Count per Hour on Workingday: {workingday}'
)
hourly_rent_by_workingday_chart.update_layout(xaxis_title='Hour', yaxis_title='Mean Count')
st.plotly_chart(hourly_rent_by_workingday_chart)


st.caption('Copyright © 2023')
