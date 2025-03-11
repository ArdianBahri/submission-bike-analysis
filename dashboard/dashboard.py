import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time

# Set style seaborn
sns.set_theme(style='dark')

# Read the Main Data
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

# Fungsi untuk animasi count-up
def animated_metric(label, value, duration=2):
    start_time = time.time()
    current_value = 0
    increment = value / (duration * 10)  # Hitung jumlah kenaikan per iterasi

    placeholder = st.empty()  # Placeholder untuk menampilkan angka

    while current_value < value:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            break  # Hentikan animasi setelah durasi berakhir
        current_value += increment
        placeholder.metric(label, int(current_value))  # Tampilkan angka saat ini
        time.sleep(0.03)  # Delay agar animasi terlihat smooth

    placeholder.metric(label, value)

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_situation').agg({
        'count': 'sum'
    })
    return weather_rent_df
    


# Membuat komponen filter
min_date = pd.to_datetime(day_df['date']).dt.date.min()
max_date = pd.to_datetime(day_df['date']).dt.date.max()

# Create a sidebar
with st.sidebar:
    st.image("Alya.jpg")
    st.subheader("Ardian Bahri Putra")
    
    # limit start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Ranged Time',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date])
    
    main_df = day_df[(day_df['date'] >= str(start_date)) & 
                (day_df['date'] <= str(end_date))]
    main_df2 = hour_df[(hour_df['date'] >= str(start_date)) &
                (hour_df['date'] <= str(end_date))]
    
# Menghitung rata-rata penyewaan untuk setiap jam
avg_rentals = main_df2.groupby("hour")["cnt"].mean()

# Menentukan jam dengan rata-rata penyewaan tertinggi dan terendah
highest_hour = avg_rentals.idxmax()
lowest_hour = avg_rentals.idxmin()
    
# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# start the streamlit code
st.title("Bike Sharing Dataset 🚲")

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    animated_metric('Casual User', daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    animated_metric('Registered User', daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    animated_metric('Total User', daily_rent_total)

# Membuat jumlah penyewaan harian
# st.subheader('Daily Rentals')
# col1, col2, col3 = st.columns(3)

# with col1:
#     daily_rent_casual = daily_casual_rent_df['casual'].sum()
#     st.metric('Casual User', value= daily_rent_casual)

# with col2:
#     daily_rent_registered = daily_registered_rent_df['registered'].sum()
#     st.metric('Registered User', value= daily_rent_registered)
 
# with col3:
#     daily_rent_total = daily_rent_df['count'].sum()
#     st.metric('Total User', value= daily_rent_total)

# pengaruh kondisi cuaca terhadap permintaan penyewaan sepeda
st.subheader("Bagaimana pengaruh kondisi cuaca terhadap permintaan penyewaan sepeda?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=main_df,
            y='weather_situation',
            x='count',
            hue='weather_situation',
            # estimator=sum,
            ax=ax,
            palette='viridis')
ax.set_title('Pengaruh Kondisi Cuaca terhadap Permintaan Penyewaan Sepeda')
ax.set_ylabel('Kondisi Cuaca')
ax.set_xlabel('Total Penyewaan')
plt.show()
st.pyplot(fig)

# jumlah penyewaan sepeda tertinggi dan terendah
st.subheader("Pada jam berapa jumlah penyewaan sepeda tertinggi dan terendah?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=avg_rentals.index, y=avg_rentals.values, hue=avg_rentals.index, palette='viridis', legend=False)
plt.title('Rata-rata Jumlah Penyewaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
st.pyplot(fig)

# tren tahunan dalam penyewaan sepeda antara tahun 2011 dan 2012
st.subheader(f"Apakah terdapat tren tahunan dalam penyewaan sepeda antara tanggal {start_date} dan {end_date}?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=main_df, x='month', y='count', hue='year', estimator='mean', errorbar=None)
plt.title('Tren Penyewaan Sepeda tahunan pada tanggal ({}-{})'.format(start_date, end_date))
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks(range(1, 13))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Tahun')
plt.show()
st.pyplot(fig)