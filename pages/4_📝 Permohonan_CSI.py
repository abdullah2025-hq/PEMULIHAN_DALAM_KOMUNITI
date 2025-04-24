import streamlit as st
from fpdf import FPDF
import tempfile
import sqlite3
import qrcode
from io import BytesIO
from PIL import Image
import base64
import datetime
import os
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Borang Permohonan CSI", layout="wide")
st.title("Borang Permohonan Program Corporate Smart Internship (CSI)")

# Setup SQLite
conn = sqlite3.connect("permohonan_csi.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS borang_csi (
    tarikh TEXT, nama_syarikat TEXT, no_ssm TEXT, nama_pengurus TEXT, telefon TEXT,
    alamat TEXT, kadar_gaji TEXT, bil_hari_kerja TEXT, elaun_lembur REAL, elaun_kehadiran REAL,
    elaun_lain TEXT, opsyen_makan TEXT, harga_makan TEXT, jenis_penginapan TEXT,
    jenis_pengangkutan TEXT, jarak_kerja TEXT, alamat_penginapan TEXT, perubatan TEXT,
    nama_klinik TEXT, alamat_klinik TEXT, pakaian_kerja TEXT, harga_pakaian TEXT,
    kategori TEXT, kapasiti_lelaki INTEGER, kapasiti_wanita INTEGER, bidang TEXT,
    deskripsi TEXT, masa_kerja TEXT, hari_bekerja INTEGER, cutilain TEXT,
    nama_pengurus_sah TEXT, tarikh_sah TEXT, qr_data TEXT
)''')
conn.commit()

st.header("Maklumat Syarikat")
nama_syarikat = st.text_input("Nama Syarikat")
no_ssm = st.text_input("No. Pendaftaran (SSM)")
nama_pengurus = st.text_input("Nama Pengurus")
telefon = st.text_input("No. Telefon")
alamat = st.text_area("Alamat Syarikat")
emel_jabatan = st.text_input("Alamat Emel Penerima (Jabatan)", value="example@prison.gov.my")

st.subheader("A. Dokumen Sokongan")
profil_syarikat = st.file_uploader("Muat naik Profil Syarikat", key="profil")
carta_organisasi = st.file_uploader("Muat naik Carta Organisasi", key="carta")
bidang_perusahaan = st.file_uploader("Muat naik Bidang Perusahaan", key="bidang")
salinan_ssm = st.file_uploader("Muat naik Salinan SSM", key="ssm")
caruman_perkeso = st.file_uploader("Muat naik Caruman PERKESO (Borang 8A)", key="perkeso")
caruman_kwsp = st.file_uploader("Muat naik Caruman KWSP (KWSP 6A)", key="kwsp")
sistem_sip = st.file_uploader("Muat naik Sistem Insurans Pekerja (SIP)", key="sip")

st.subheader("B. Tawaran Syarikat")
kadar_gaji = st.selectbox("Jenis Bayaran Gaji", ["Bulanan - RM1700", "Harian - RM65.38", "Jam - RM8.72"])
bil_hari_kerja = st.radio("Bilangan Hari Bekerja dalam Seminggu", ["6 Hari", "5 Hari", "4 Hari"])
elaun_lembur = st.number_input("Elaun Lebih Masa (RM)", min_value=0.0)
elaun_kehadiran = st.number_input("Elaun Kehadiran (RM)", min_value=0.0)
elaun_lain = st.text_area("Nyatakan Elaun Lain dan Kadar")
opsyen_makan = st.radio("Kemudahan Makan/Minum", ["Percuma", "Berbayar dengan Potongan Gaji", "Tidak Disediakan"])
harga_makan = st.text_input("Amaun Potongan (Jika berbayar)") if opsyen_makan == "Berbayar dengan Potongan Gaji" else ""
jenis_penginapan = st.text_input("Jenis Penginapan")
jenis_pengangkutan = st.text_input("Jenis Pengangkutan")
jarak_kerja = st.text_input("Jarak ke Tempat Kerja")
alamat_penginapan = st.text_area("Alamat Penginapan")
perubatan = st.radio("Kemudahan Perubatan", ["Percuma", "Berbayar dengan Potongan Gaji", "Tidak Disediakan"])
nama_klinik = st.text_input("Nama Klinik Panel")
alamat_klinik = st.text_area("Alamat Klinik")
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

st.subheader("Perakuan")
setuju = st.checkbox("Saya bersetuju dengan semua syarat penyertaan program CSI")
nama_pengurus_sah = st.text_input("Nama dan Jawatan Penandatangan")
tarikh_sah = st.date_input("Tarikh Tandatangan")

if st.button("Hantar Borang"):
    timestamp = datetime.datetime.now().isoformat()
    qr_text = f"{nama_syarikat}|{no_ssm}|{timestamp}"
    qr_img = qrcode.make(qr_text)
    qr_path = os.path.join(tempfile.gettempdir(), "qr_temp.png")
    qr_img.save(qr_path)

    c.execute('''INSERT INTO borang_csi VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
        timestamp, nama_syarikat, no_ssm, nama_pengurus, telefon, alamat,
        kadar_gaji, bil_hari_kerja, elaun_lembur, elaun_kehadiran, elaun_lain,
        opsyen_makan, harga_makan, jenis_penginapan, jenis_pengangkutan, jarak_kerja,
        alamat_penginapan, perubatan, nama_klinik, alamat_klinik,
        pakaian_kerja, harga_pakaian, ', '.join(kategori), kapasiti_lelaki,
        kapasiti_wanita, ', '.join(bidang), deskripsi, masa_kerja, hari_bekerja,
        cutilain, nama_pengurus_sah, str(tarikh_sah), qr_text
    ))
    conn.commit()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "BORANG PERMOHONAN PROGRAM CSI", 0, 1, "C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Nama Syarikat: {nama_syarikat}", ln=1)
    pdf.cell(0, 10, f"No SSM: {no_ssm}", ln=1)
    pdf.cell(0, 10, f"Telefon: {telefon}", ln=1)
    pdf.cell(0, 10, f"Tarikh Permohonan: {tarikh_sah}", ln=1)
    pdf.image(qr_path, x=160, y=10, w=30)

    pdf_path = os.path.join(tempfile.gettempdir(), "borang_csi_qr.pdf")
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("📄 Muat Turun Salinan PDF dengan QR", f, file_name="borang_csi_qr.pdf")

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Permohonan Baru Program CSI'
        msg['From'] = 'noreply@jabatanpenjara.gov.my'
        msg['To'] = emel_jabatan
        msg.set_content(f"Permohonan baru dari {nama_syarikat} telah diterima.")
        with open(pdf_path, "rb") as f:
            msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename="borang_csi_qr.pdf")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("Abdullah_abdkodir@prison.gov.my", "KATALALUAN_APLIKASI")
            smtp.send_message(msg)
        st.success("Emel berjaya dihantar kepada jabatan!")
    except Exception as e:
        st.warning(f"Gagal hantar emel: {e}")

    st.success("Permohonan telah dihantar dan disimpan!")
