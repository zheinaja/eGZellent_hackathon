import streamlit as st



st.set_page_config(
    page_title="Inferensi Data Marketplace Rumah"
)
st.title("Inferensi Data Marketplace Rumah")

st.subheader('''
             Analisa ditampilkan melalui Dashboard Power BI dibawah,
             hasil analisa dapat di-klik melalui nama analisa pada slide dashboard
             ''')

st.markdown("""
    <iframe width="1200" height="700" src="https://app.powerbi.com/view?r=eyJrIjoiNzI2Zjg1ZDItMDBkOC00ZDE3LWI3YzAtM2ZlZmUxZjY2ODdiIiwidCI6ImRkMDlkNzMwLTc3OGYtNDI0Yy04YTdiLTU1ZGNjNjU1Y2EwZiIsImMiOjEwfQ%3D%3D" frameborder="0" style="border:0" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

st.subheader('''
             Deskripsi Data Marketplace Rumah
             menampilkan deskripsi data marketplace rumah, halaman ini menampilkan deskripsi statistik terhadap data dari marketplace rumah. Tampilan ini dapat di filter berdasarkan Kabupaten/Kota di sebelah kanan dari halaman. Untuk kembali ke halaman menu dapat dilakukan dengan meng-klik ikon ← yang terdapat di kiri atas. 
             ''')
st.subheader('''
             Analisa Ketersediaan Rumah untuk Pekerja
Menyajikan analisa ketersediaan rumah bagi masyarakat dengan penghasilan Upah Minimum Kabupaten/Kota (UMK). analisa ini menggunakan asumsi bahwa kemampuan mencicil KPR masyarakat merupakan 30% dari UMK, tingkat suku bunga KPR sebesar 5%, tenor selama 20 tahun, serta tidak dilakukan pembayaran uang muka.
Peta memperlihatkan 3 titik berwarna biru, merah, dan hijau. Warna biru merupakan titik Kabupaten/Kota yang dipilih yang memperlihatkan lokasi tempat kerja, titik merah memperlihatkan tidak ada rumah pada kecamatan yang dapat dibeli dengan gaji UMK, dan titik hijau memperlihatkan terdapat rumah yang dapat dibeli dengan gaji UMK.
Slide ini dapat ditapis dengan 2 kriteria yaitu pilihan Kabupaten/Kota lokasi tempat kerja dan jarak maksimal dan minimal rumah dari tempat kerja. Kedua tapisan tersebut terdapat pada kanan laman.
Tabel di bagian bawah memperlihatkan deskripsi agregat dari rumah pada kecamatan yang yang dapat di beli dengan UMK. Pada tabel ini juga kami memperkenalkan nilai ‘Keterjangkauan’ yang merupakan presentasi rumah yang dapat dibeli oleh masyarakat dengan gaji UMK. Untuk kembali ke halaman menu dapat dilakukan dengan meng-klik ikon ← yang terdapat di kiri atas. 

             ''')
st.subheader('''
             Analisa Prioritas Perumahan berdasarkan Keterjangkauan
             Menyajikan analisa prioritas dalam melakukan fasilitasi bidang perumahan berdasarkan keterjangkauan. Analisa ini masih menggunakan asumsi yang sama dengan slide sebelumnya namun ditambahkan dengan maksimal data yang ditapis adalah 30 kilometer dari tempat kerja. Asumsi tambahan adalah data kota dengan rumah yang dijual dengan jarak 30 kilometer lebih sedikit dari 30 unit rumah, kota tersebut di drop dari data dikarenakan jumlah sampel dikhawatirkan tidak memenuhi populasi berdasarkan central limit theorem
             Data pada slide dapat ditapis berdasarkan provinsi melalui panel di kanan slide. Analisa prioritas memberikan informasi agregasi keterjangkauan pada tingkatan Kabupaten/Kota dimana nilai keterjangkauan terkecil merupakan daerah yang prioritas untuk diberikan fasilitasi bidang perumahan.
             ''')

#simpan paling bawah ye
st.sidebar.title('''
                 Tim eGZellent
                 1. Zhein Adhi Mahendra Setiawan
                 2. Gifari Rahmat Alif
                 ''')
