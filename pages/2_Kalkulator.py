# -*- coding: utf-8 -*-
"""
dong dong dong
"""

import numpy as np
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

#buka data set
df = pd.read_csv('Data/clean_data_rumah 2023.csv', sep=';')
lokasi = pd.read_excel('Data/koordinat Kecamatan Jawa.xlsx')
lok_kota = pd.read_excel('Data/lonlatkec_kota.xlsx')
daftar_kota = lok_kota[lok_kota['kota'] != 'KEPULAUAN SERIBU']

#buat id kota
df ['ID_kecamatan'] = df ['ID_kecamatan'].astype (str)
df['ID_Kota'] =df['ID_kecamatan'].str[:4]
lokasi.drop(['Unnamed: 4', 'Unnamed: 5', 'location'], axis=1, inplace=True)
lokasi = lokasi.rename(columns={'lokasi': 'Lokasi'})


nama_kota = []
hntenor_cicilan = []
suku_bunga = []
uang_muka = [] 
gaji = []
jarak = []

def beli_rumah(nama_kota, hntenor_cicilan, suku_bunga, uang_muka, gaji, jarak):
  try:
    nama_kota = str.upper(nama_kota)
  
    suku_bunga = suku_bunga/100
    uang_muka = uang_muka/100
    max_cicilan = gaji*0.3
  
  
    #lokasi yang masuk kedalam cicilan (kolom Lokasi)
    df['cicilan'] = (suku_bunga/12) * (1/ (1- (1+suku_bunga/12)**(-(hntenor_cicilan*12))))* df['Harga'] *(1-uang_muka)
    df['cicilan'] = df['cicilan'].astype(float)
    df_beli = df[df['cicilan'] <= max_cicilan]
  
    #groupby harga di average kolom harga rata2 (Kolom Harga Rata2)
    df_beli1 = df_beli.groupby(['Lokasi'])['Harga'].mean().reset_index()
    df_beli1 = round(df_beli1.rename(columns={'Harga': 'Harga Rata2'}))
  
    #Hitung Jumlah rumah yang dijual (% rumah terbeli)
    df_beli2 = df_beli.groupby(['Lokasi'])['Harga'].count().reset_index()
    df_beli2 = df_beli2.rename(columns={'Harga': 'rumah beli'})
    df_beli3 = df.groupby(['Lokasi'])['Harga'].count().reset_index()
    df_beli3 = df_beli3.rename(columns={'Harga': 'rumah jual'})
    df_beli2 = pd.merge(df_beli2, df_beli3, how='left', left_on='Lokasi', right_on='Lokasi')
    df_beli2['persen rmh terbeli'] = round((df_beli2['rumah beli']/df_beli2['rumah jual'])*100, 2)
    df_beli1 = pd.merge(df_beli1, df_beli2, how='left', left_on='Lokasi', right_on='Lokasi')
  
  
    #hitung jarak (kolom jarak terhadap tempat kerja dalam KM)
    _lat = lok_kota[lok_kota['kota'] == nama_kota]
    _lat = _lat['latitude']
    _lat = _lat.iloc[0]
    _lon = lok_kota[lok_kota['kota'] == nama_kota]
    _lon = _lon['longitude']
    _lon = _lon.iloc[0]
  
    df_beli1 = pd.merge(df_beli1, lokasi, how='left', left_on='Lokasi', right_on='Lokasi')
  
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # radius of Earth in kilometers
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
        return np.round(res, 2)
    
    df_beli1['jarak km'] = df_beli1.apply(lambda row: haversine(_lat, _lon, row['latitude'], row['longitude']), axis=1)
    df_beli1 = df_beli1[df_beli1['jarak km'] <= jarak]
    # df_beli1.drop(['latitude', 'longitude'], axis=1, inplace=True)
    df_beli1.sort_values(by=['jarak km'], inplace=True)
    
    # df_beli1.dropna(subset=['latitude', 'longitude'], inplace=True)
    
    #Initialize titik tengah peta. pakai mean dari tiap lokasi di df_beli1
    
    mean_lat = df_beli1['latitude'].mean()
    mean_long = df_beli1['longitude'].mean()
    
    map = folium.Map(location=[mean_lat, mean_long], zoom_start=10)
  
    # Taruh marker di lokasi kerja
    folium.Marker([_lat, _lon], 
                  popup='Lokasi Kerja',
                  icon=folium.Icon(color='red', icon='cloud')).add_to(map)
    #Tambah marker untuk lokasi-lokasi rumah potensial
    for index, row in df_beli1.iterrows():
      folium.Marker([row['latitude'], row['longitude']], 
                    popup=f"{row['Lokasi']}").add_to(map)
  
    df_beli1.drop(['latitude', 'longitude'], axis=1, inplace=True)
    df_beli1['Harga Rata2'] = df_beli1['Harga Rata2'].astype(int)

  
    st.dataframe(df_beli1.style.format({"jarak km": "{:,.2f}", "persen rmh terbeli": "{:,.2f}"}), hide_index=True)
    # Display the Folium map in Streamlit
    st.write(map._repr_html_(), unsafe_allow_html=True)
  except :
    st.write(f':red[tidak ada] rumah terjangkau pada radius :blue[{jarak} kilometer] dari lokasi kerja')

def main():
   # judul
   st.title("Lokasi Kerja dan Keterjangkauan Rumah")
   st.subheader('''
Berikut penjelasaan daftar input:
1. Lokasi Kerja - diisi dengan Kabupaten/Kota yang menjadi lokasi kerja masyarakat pencari rumah
2. Tenor Pinjaman - diisi dengan tahun lamanya KPR dicicl
3. Suku Bunga -  diisi dengan persentase tingkat suku bunga KPR
4. Uang Muka - diisi dengan persentase uang muka terhadap harga rumah
5. Penghasilan per Bulan - diisi dengan penghasilan per bulan dalam rupiah.
6. Radius Maksimal ke Lokasi Kerja - diisi dengan jarak maksimal rumah ke tempat kerja dalam kilometer.
untuk menampilkan hasil dapat meng-klik tombol :blue[Lokasi yang dapat terjangkau]

                ''')
   #input data
   nama_kota = st.selectbox('Lokasi Kerja',daftar_kota['kota'])
   hntenor_cicilan = st.number_input('tenor pinjaman (tahun)', step = 1)
   suku_bunga = st.number_input('suku bunga (%)', step = 0.1)
   uang_muka = st.number_input('uang muka (%)', step = 1)
   gaji = st.number_input('Penghasilan per Bulan(Rp)', step = 1e6)
   jarak = st.number_input('Radius Maksimal ke Lokasi Kerja(KM)', step = 0.1)

   terjangkau = ''



   if st.button('lokasi yang dapat terjangkau'):
      terjangkau = beli_rumah(nama_kota, hntenor_cicilan, suku_bunga, uang_muka, gaji, jarak)

if __name__ ==  '__main__':
   main()

#simpan paling bawah ye
st.sidebar.title('''
                 Tim eGZellent
                 1. Zhein Adhi Mahendra Setiawan
                 2. Gifari Rahmat Alif
                 ''')
