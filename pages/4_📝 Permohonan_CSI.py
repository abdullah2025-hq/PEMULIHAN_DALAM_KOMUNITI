import streamlit as st

st.set_page_config(page_title="Borang Permohonan CSI", layout="wide")
st.title("Borang Permohonan Program Corporate Smart Internship (CSI)")

st.header("Maklumat Syarikat")
nama_syarikat = st.text_input("Nama Syarikat")
no_ssm = st.text_input("No. Pendaftaran (SSM)")
nama_pengurus = st.text_input("Nama Pengurus")
telefon = st.text_input("No. Telefon")
alamat = st.text_area("Alamat Syarikat")

st.subheader("A. Dokumen Sokongan")
profil_syarikat = st.file_uploader("Muat naik Profil Syarikat", key="profil")
carta_organisasi = st.file_uploader("Muat naik Carta Organisasi", key="carta")
bidang_perusahaan = st.file_uploader("Muat naik Bidang Perusahaan", key="bidang")
salinan_ssm = st.file_uploader("Muat naik Salinan SSM", key="ssm")
caruman_perkeso = st.file_uploader("Muat naik Caruman PERKESO (Borang 8A)", key="perkeso")
caruman_kwsp = st.file_uploader("Muat naik Caruman KWSP (KWSP 6A)", key="kwsp")
sistem_sip = st.file_uploader("Muat naik Sistem Insurans Pekerja (SIP)", key="sip")

st.subheader("B. Tawaran Syarikat")
st.markdown("**1. Gaji yang Ditawarkan**")
kadar_gaji = st.selectbox("Jenis Bayaran Gaji", ["Bulanan - RM1700", "Harian - RM65.38", "Jam - RM8.72"])
bil_hari_kerja = st.radio("Bilangan Hari Bekerja dalam Seminggu", ["6 Hari", "5 Hari", "4 Hari"])

st.markdown("**2. Elaun**")
elaun_lembur = st.number_input("Elaun Lebih Masa (RM)", min_value=0.0)
elaun_kehadiran = st.number_input("Elaun Kehadiran (RM)", min_value=0.0)
elaun_lain = st.text_area("Nyatakan Elaun Lain dan Kadar")

st.markdown("**3. Makan/Minum**")
opsyen_makan = st.radio("Kemudahan Makan/Minum", ["Percuma", "Berbayar dengan Potongan Gaji", "Tidak Disediakan"])
harga_makan = st.text_input("Amaun Potongan (Jika berbayar)") if opsyen_makan == "Berbayar dengan Potongan Gaji" else ""

st.markdown("**4. Penginapan & Kemudahan**")
jenis_penginapan = st.text_input("Jenis Penginapan")
jenis_pengangkutan = st.text_input("Jenis Pengangkutan")
jarak_kerja = st.text_input("Jarak ke Tempat Kerja")
alamat_penginapan = st.text_area("Alamat Penginapan")

st.markdown("**5. Perubatan**")
perubatan = st.radio("Kemudahan Perubatan", ["Percuma", "Berbayar dengan Potongan Gaji", "Tidak Disediakan"])
nama_klinik = st.text_input("Nama Klinik Panel")
alamat_klinik = st.text_area("Alamat Klinik")

st.markdown("**6. Pakaian Kerja**")
pakaian_kerja = st.radio("Kemudahan Pakaian Kerja", ["Percuma", "Berbayar dengan Potongan Gaji", "Tidak Disediakan"])
harga_pakaian = st.text_input("Amaun Potongan (Jika berbayar)") if pakaian_kerja == "Berbayar dengan Potongan Gaji" else ""

st.subheader("C. Kategori Pengambilan")
kategori = st.multiselect("Kategori", ["ODP", "OBB", "ODS", "PBL"])
kapasiti_lelaki = st.number_input("Kapasiti Lelaki", min_value=0)
kapasiti_wanita = st.number_input("Kapasiti Wanita", min_value=0)

st.subheader("D. Skop Pekerjaan")
bidang = st.multiselect("Bidang", ["Perkhidmatan", "Pembuatan", "Perladangan", "Pembinaan", "Pertanian/Penternakan"])
deskripsi = st.text_area("Skop / Deskripsi Kerja")
masa_kerja = st.text_input("Waktu Kerja (Normal/Syif)")
hari_bekerja = st.number_input("Jumlah Hari Bekerja", min_value=0)
cutilain = st.text_area("Jenis dan Jumlah Cuti")

st.subheader("E. Gambar-Gambar")
gambar_info = st.file_uploader("Muat Naik Gambar Berkaitan (Penginapan, Tempat Kerja, dll)", accept_multiple_files=True)

st.subheader("Perakuan")
st.checkbox("Saya bersetuju dengan semua syarat penyertaan program CSI")
nama_pengurus_sah = st.text_input("Nama dan Jawatan Penandatangan")
tarikh_sah = st.date_input("Tarikh Tandatangan")

if st.button("Hantar Borang"):
    st.success("Permohonan telah dihantar dengan berjaya!")