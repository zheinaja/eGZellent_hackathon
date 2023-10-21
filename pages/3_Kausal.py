from email.policy import default
from logging import PlaceHolder
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.formula.api as sm
from PIL import Image




df = pd.read_csv("Data/clean data rumah 2023 dan tol terdekat.csv", sep = ';')
hasil_cem = pd.read_csv("Data/hasil cem.csv", sep = ';')

kabkot = df['Kab/Kota']
kabkot.drop_duplicates(inplace=True)
jarak_terjauh = df['tol terdekat'].max()
jarak_terjauh = int(jarak_terjauh)

batas_tol = []
lokasi = []
m_jarak = []
tol = ''

def cem(batas_tol, lokasi, m_jarak):
    df_run = df.copy()
    df_run = df_run[df_run['Kab/Kota'].isin(lokasi)]
    df_run = df_run[df_run['tol terdekat'] <= m_jarak]

    def treatment(row):
        if row['tol terdekat'] <= batas_tol :
            val = 1
        else:
            val = 0
        return val

    df_run['tol'] = df_run.apply(treatment, axis=1)

    #log harga
    df_run['log_harga'] = np.log2(df_run['Harga'])

    # Count how many treated and control observations
    # are in each bin
    treated = df_run.loc[df_run['tol'] == 1].groupby(['Luas Tanah','Luas Bangunan', 'Kamar Tidur']).size().to_frame('treated')
    control = df_run.loc[df_run['tol'] == 0].groupby(['Luas Tanah','Luas Bangunan', 'Kamar Tidur']).size().to_frame('control')

    # Merge those counts back in
    df_run = df_run.join(treated, on = ['Luas Tanah','Luas Bangunan', 'Kamar Tidur'])
    df_run = df_run.join(control, on = ['Luas Tanah','Luas Bangunan','Kamar Tidur'])

    # For treated obs, weight is 1 if there are any control matches
    df_run['weight'] = 0
    df_run.loc[(df_run['tol'] == 1) & (df_run['control'] > 0), 'weight'] = 1

    # For control obs, weight depends on total number of treated and control
    # obs that found matches
    totalcontrols = sum(df_run.loc[df_run['tol']==0]['treated'] > 0)
    totaltreated = sum(df_run.loc[df_run['tol']==1]['control'] > 0)

    # Then, control weights are treated/control in the bin,
    # times control/treated overall
    df_run['controlweights'] = (df_run['treated']/df_run['control'])*(totalcontrols/totaltreated)
    df_run.loc[(df_run['tol'] == 0), 'weight'] = df_run['controlweights']

    # Now, use the weights to estimate the effect
    df_run = df_run.replace(np.inf, np.nan).replace(-np.inf, np.nan).dropna()

    result = sm.wls(formula = 'log_harga ~ tol', weights = df_run['controlweights'], data = df_run).fit()

    hasil = pd.read_html(result.summary().tables[1].as_html(),header=0,index_col=0)[0]
    koef_tol = hasil['coef'].values[1]
    conf_tol =hasil['P>|t|'].values[1]
    st.write(f'Dengan tingkat kepercayaan sebesar {100-conf_tol}%, efek keberadaan gerbang tol dengan radius \
          :blue[{batas_tol} kilometer] dari rumah mengakibatkan peningkatan harga rumah sebesar :red[{np.round(koef_tol*100,2)}%]')

def main():
    # judul
    st.title("Efek Rata-Rata Perubahan Harga Rumah diakibatkan Gerbang Tol")
    #input data
    st.subheader('''
                terdapat 2 pilihan analisa inferensi kausal menggunakan Coarsened Exact Matching (CEM), yaitu:
                1. Average Treatment Effect (ATE)
                   Menjelaskan dampak rata-rata gerbang tol terhadap harga rumah di Pulau Jawa
                2. Conditional Average Treatment Effect (CATE)
                   Melakukan simulasi CATE untuk melihat dampak rata-rata dengan kondisi lokasi Kabupaten/Kota dan jarak tol terhadap rumah
                ''')
    opsi_cem = st.selectbox('Pilih salah satu analisa', ['Hasil ATE', 'Simulasi CATE'])
   
    if opsi_cem=='Simulasi CATE':
       lokasi = st.multiselect('Kabupaten/Kota yang disertakan',
                           kabkot, default = kabkot)
       batas_tol = st.number_input('Jarak rumah ke gerbang Tol terdekat (KM)', step = 0.1,
                               min_value=1.0)
       m_jarak = st.slider('Maksimal Jarak Control group', 0, jarak_terjauh , 15)
       
       
       if st.button('Hitung efek gerbang tol terhadap harga rumah'):
        tol = cem(batas_tol, lokasi,m_jarak)
    else:
       st.write('Dalam penghitungan ATE, kita membandingkan treatment grup dan control grup \
                di Pulau Jawa. treatment yang dipilih adalah efek dari jarak rumah ke gerbang \
                tol terdekat yang kurang dari sama dengan 2 kilometer. \
                Tabel berikut adalah ringkasan hasil penghitungan ATE:')
       
       d_ate = {' ': ['Outcome', 'Treatment', 'Metode', 'Matching Var', 'Hasil'],
                'Deskripsi': ['Persentase perubahan harga rumah',
                         'Rumah dengan jarak ke gerbang tol terdekat kurang 2 kilometer',
                         'Coarsened Exact Matching (CEM)', 
                         ' Luas Tanah, Luas Bangunan, dan Jumlah Kamar',
                         'Terdapat perbedaan harga rumah sebesar 93,55% antara treatment grup dan control grup']} 
       st.dataframe(d_ate, width=1000, hide_index=True)
       st.write('Berikut ringkasan statistik hasil perhitungan CEM:')
       image = Image.open('Data/sum cem.png')
       st.image(image, caption='Ringkasan Hasil Perhitungan CEM')


if __name__ ==  '__main__':
   main()

#simpan paling bawah ye
st.sidebar.title('''
                 Tim eGZellent
                 1. Zhein Adhi Mahendra Setiawan
                 2. Gifari Rahmat Alif
                 ''')
