import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#pemuatan data

base_dir = os.path.dirname(__file__)

# Path menuju file CSV
day_file_path = os.path.join(base_dir, "data_dashboard", "day_data.csv")
hour_file_path = os.path.join(base_dir, "data_dashboard", "hour_data.csv")

# Baca file CSV
day_data = pd.read_csv(day_file_path)
hour_data = pd.read_csv(hour_file_path)

#mengubah tipe data dteday
day_data['dteday'] = pd.to_datetime(day_data['dteday'])
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

#Header
st.title("Analisis Penyewaan Sepeda, Brow!")
st.markdown("Dashboard ini menampilkan tren penyewaan sepeda berdasarkan jam, pengaruh musim terhadap jumlah penyewaan, serta analisis RFM untuk pengguna terdaftar")

#analisis tren sewa sepeda berdasarkan jam
st.subheader("Tren Penyewaan Sepeda berdasarkan jam dan hari kerja")
st.markdown("Grafik ini menunjukkan jumlah penyewaan sepeda pada jam tertentu, dibagi berdasarkan hari kerja dan hari libur.")
hour_rentals = hour_data.groupby(["hr", "workingday"]).agg({"cnt": "sum"}).reset_index()
selected_hour = st.slider("Pilih Jam", min_value=0, max_value=23, value=12)
filtered_hour = hour_rentals[hour_rentals['hr'] == selected_hour]

total_rental = filtered_hour['cnt'].sum()
st.metric("Total Penyewaan pada Jam Terpilih", total_rental)


fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='workingday', y='cnt', data=filtered_hour, palette=['#FF7F50', '#72BCD4'], ax=ax)
ax.set_xticklabels(["Hari Libur", "Hari Kerja"])
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title(f"Total Penyewaan Sepeda pada Jam {selected_hour}")
st.pyplot(fig)

#Analisis pengaruh musim terhadap sewa sepeda
st.subheader("Pengaruh Musim terhadap Penyewaan Sepeda")
st.markdown("Grafik ini menunjukkan bagaimana jumlah penyewaan sepeda berubah selama musim yang berbeda.")
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_data['season'] = day_data['season'].map(season_labels)
selected_season = st.selectbox("Pilih Musim", day_data['season'].unique())
filtered_season = day_data[day_data['season'] == selected_season]

avg_rental_season = filtered_season['cnt'].mean()
st.metric(f"Rata-rata Penyewaan di {selected_season}", int(avg_rental_season))

fig, ax = plt.subplots(figsize=(8,5))
sns.lineplot(x='dteday', y='cnt', data=filtered_season, ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title(f"Tren Penyewaan Sepeda pada {selected_season}")
st.pyplot(fig)

#Analisis RFM
st.subheader("Analisis RFM (Recency, Frequency, Monetary)")
st.markdown("Analisis RFM digunakan untuk mengelompokkan pengguna berdasarkan kapan terakhir mereka menyewa sepeda (Recency), seberapa sering mereka menyewa (Frequency), dan total jumlah transaksi mereka (Monetary).")
rfm_df=hour_data.groupby(by="registered", as_index=False).agg({
    "dteday": "max",
    "instant": "count",
    "cnt": "sum"
})

rfm_df.columns= ["user_id", "max_order_timestamp", "frequency", "monetary"]

rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"]).dt.date
recent_date = hour_data["dteday"].max().date()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

recency_threshold = st.slider("Maksimum Recency (hari)", min_value=0, max_value=rfm_df["recency"].max(), value=30)
frequency_threshold = st.slider("Minimum Frequency", min_value=1, max_value=rfm_df["frequency"].max(), value=5)
monetary_threshold = st.slider("Minimum Monetary", min_value=1, max_value=int(rfm_df["monetary"].max()), value=50)

filtered_rfm = rfm_df[(rfm_df["recency"] <= recency_threshold) & (rfm_df["frequency"] >= frequency_threshold) & (rfm_df["monetary"] >= monetary_threshold)]
st.dataframe(filtered_rfm.head())
st.markdown(f"### Jumlah Pengguna Terfilter: {len(filtered_rfm)}")

# Visualisasi Distribusi Recency, Frequency, dan Monetary
st.markdown("Berikut adalah distribusi dari masing-masing metrik dalam analisis RFM:")
fig, ax = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(rfm_df["recency"], bins=20, kde=True, ax=ax[0], color="blue")
ax[0].set_title("Distribusi Recency")
st.metric("Rata-rata Recency", int(rfm_df["recency"].mean()))
sns.histplot(rfm_df["frequency"], bins=20, kde=True, ax=ax[1], color="green")
ax[1].set_title("Distribusi Frequency")
st.metric("Rata-rata Frequency", int(rfm_df["frequency"].mean()))
sns.histplot(rfm_df["monetary"], bins=20, kde=True, ax=ax[2], color="red")
ax[2].set_title("Distribusi Monetary")
st.metric("Rata-rata Monetary", int(rfm_df["monetary"].mean()))
st.pyplot(fig)
st.markdown("Grafik ini menunjukkan distribusi dari masing-masing komponen RFM. Dari sini kita bisa memahami pola pelanggan, seperti apakah mayoritas pelanggan sering bertransaksi atau hanya sesekali.")





