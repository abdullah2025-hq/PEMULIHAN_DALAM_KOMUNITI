import streamlit as st

st.set_page_config(page_title="🏠 Laman Utama", layout="wide")

st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #dff9fb, #c7ecee);
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main'>
    <h1>📊 Sistem Statistik Pemulihan Dalam Komuniti</h1>
    <p>Selamat datang ke sistem pemantauan program pemulihan komuniti Jabatan Penjara Malaysia.</p>
    <ul>
        <li><strong>Isi Maklumat Harian</strong> bagi program Parol, PBSL, PBL (SHG), PRP dan PKW melalui borang khusus.</li>
        <li><strong>Semak Statistik</strong> harian, bulanan, atau tahunan secara automatik dengan carta interaktif.</li>
    </ul>
    <p>Sila gunakan menu di sebelah kiri untuk navigasi.</p>
</div>
""", unsafe_allow_html=True)

st.info("Gunakan tab 📥 Isi Maklumat Harian untuk key-in data dan 📊 Statistik Program untuk semakan.")
