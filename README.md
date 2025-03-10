# Dashboard Analisis Penyewaan Sepeda 🚲  

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data penyewaan sepeda berdasarkan metode **RFM Analysis**.  

## Fitur Utama  
- Menampilkan tren penyewaan sepeda harian dan per jam.  
- Analisis perilaku pelanggan menggunakan **RFM (Recency, Frequency, Monetary)**.  
- Visualisasi data interaktif menggunakan **Matplotlib** dan **Seaborn**.  

## Setup Environment - Anaconda  
Jalankan perintah berikut untuk membuat environment:  

```sh
conda create --name penyewaan_dashboard python=3.9  
conda activate penyewaan_dashboard  
pip install -r requirements.txt  
```

## Setup Environment - Shell/Terminal  
Jika menggunakan virtual environment biasa:  

```sh
mkdir penyewaan_dashboard  
cd penyewaan_dashboard  
pipenv install  
pipenv shell  
pip install -r requirements.txt  
```

## Menjalankan Dashboard Streamlit  
Jalankan perintah berikut di terminal:  

```sh
streamlit run dashboard.py  
```

## Struktur Folder  
```
dashboard_streamlit/
│── data_dashboard              # Data dashboard     
│   ├── day_data.csv
|   ├── hour_data.csv     
│── dashboard.py                # File utama Streamlit
Data                            # Data analisis
│──day.csv
│──hour.csv                     
Proyek_Analisis_Data.py         # File utama analisis   
README.md                       # Langkah menjalankan dashboard
requirements.txt                # Library yang dibutuhkan
url.txt                         # url streamlit
```

>>>>>>> 895d28e (Upload proyek dashboard penyewaan sepeda)
