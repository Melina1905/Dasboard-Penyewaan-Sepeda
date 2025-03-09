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
hour_rentals=hour_data.groupby(["hr", "workingday"]).agg({
    "cnt": "sum",
    "casual": "sum",
    "registered": "sum"
}).reset_index()

hour_rentals.columns = ['hr', 'workingday', 'cnt_sum', 'casual_sum', 'registered_sum']
workingday_df = hour_rentals[hour_rentals["workingday"]==1]
non_workingday_df = hour_rentals[hour_rentals["workingday"] == 0]
overall_rentals = hour_rentals.groupby("hr")["cnt_sum"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(workingday_df["hr"], workingday_df["cnt_sum"],marker = 'o', label = "Hari Kerja", color="#72BCD4")
ax.plot(non_workingday_df["hr"], non_workingday_df["cnt_sum"], marker='o', label="Hari Libur", color="#FF7F50")
ax.plot(overall_rentals["hr"], overall_rentals["cnt_sum"], marker='o', linestyle="--", label="Tren Keseluruhan", color="#2E8B57")
ax.set_xlabel("Jam")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

#Analisis pengaruh musim terhadap sewa sepeda
st.subheader("Pengaruh Musim terhadap Penyewaan Sepeda")
season_rentals = day_data.groupby("season").agg({
    "cnt": ["sum", "mean"]
}).reset_index()
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_rentals["season"] = season_rentals["season"].map(season_labels)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="season", y=("cnt", "sum"), data=season_rentals, palette="coolwarm", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

st.markdown("### Rata-rata penyewaan sepeda per musim")
st.markdown(f"<h1>{season_rentals[('cnt', 'mean')].mean():.2f}</h1>", unsafe_allow_html= True)

#Analisis RFM
st.subheader("Analisis RFM (Recency, Frequency, Monetary)")
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

st.dataframe(rfm_df.head())
st.markdown("### Rata-rata frekuensi peminjaman pengguna terdaftar")
st.markdown(f"<h1>{rfm_df['frequency'].mean():.2f}</h1>", unsafe_allow_html=True)

st.markdown("### Rata-rata nilai moneter peminjaman")
st.markdown(f"<h1>{rfm_df['monetary'].mean():.2f}</h1>", unsafe_allow_html=True)

# Visualisasi Distribusi Recency, Frequency, dan Monetary
fig, ax = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(rfm_df["recency"], bins=20, kde=True, ax=ax[0], color="blue")
ax[0].set_title("Distribusi Recency")
sns.histplot(rfm_df["frequency"], bins=20, kde=True, ax=ax[1], color="green")
ax[1].set_title("Distribusi Frequency")
sns.histplot(rfm_df["monetary"], bins=20, kde=True, ax=ax[2], color="red")
ax[2].set_title("Distribusi Monetary")
st.pyplot(fig)





