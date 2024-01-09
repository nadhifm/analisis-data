import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_daily_user_df(df):
    daily_user_df = df.groupby(by='dteday').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    return daily_user_df

def create_hourly_user_df(df):
    hourly_user_df = df.groupby(by='hr').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()
    return hourly_user_df

# Load data hour_df
hour_df = pd.read_csv('hour.csv')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Filter data
min_date = pd.to_datetime('2012-12-24')
max_date = pd.to_datetime('2012-12-31')
 
with st.sidebar:
    st.image('icon.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= hour_df['dteday'].min(),
        max_value= hour_df['dteday'].max(),
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df['dteday'] >= str(start_date)) & 
                (hour_df['dteday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_user_df = create_daily_user_df(main_df)
hourly_user_df = create_hourly_user_df(main_df)

# Dashboard
st.header('Bike Sharing Dashboard')

# Membuat jumlah penyewaan harian
st.subheader('Daily User')
col1, col2, col3 = st.columns(3)

with col1:
    daily_user_casual = daily_user_df['casual'].sum()
    st.metric('Casual User', value= daily_user_casual)

with col2:
    daily_user_registered = daily_user_df['registered'].sum()
    st.metric('Registered User', value= daily_user_registered)
 
with col3:
    daily_user_total = daily_user_df['cnt'].sum()
    st.metric('Total User', value= daily_user_total)

# Membuat grafik pengguna harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_user_df['dteday'],
    daily_user_df['cnt'],
    marker='o', 
    linewidth=2,
    color='#FFD28F'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Membuat grafik pengguna berdasarkan jam
st.subheader('Hoourly User')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    data=hourly_user_df,
    x='hr',
    y='cnt',
    palette='cubehelix',
    ax=ax
)

ax.set_title('')
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)