import streamlit as st
from datetime import date

# Judul Halaman
st.title("📍 Borang Pergerakan Masuk dan Keluar")

# Pilihan Program dan Institusi
st.header("📋 Maklumat Program")
program = st.selectbox("Pilih Program", ["PRPI", "PRP", "Lain-lain"])
if program == "PRPI":
    institusi = st.selectbox("Pilih Institusi", [
        "RTI Sg. Buloh", "RTI Penor", "RTI Muar",
        "PKK Sg. Petani", "PKK Batu Pahat", "PRPI Tuaran", "Tiada"
    ])
elif program == "PRP":
    institusi = st.selectbox("Pilih Institusi", [
        "PRP Kuala Muda", "PRP Kuala Krai", "PRP Sepang",
        "PRP Mantin", "PRP Kluang", "PRP Tuaran", "Tiada"
    ])
else:
    institusi = "Lain-lain"

# Pilih Tarikh
selected_date = st.date_input("Pilih Tarikh", value=date.today())

# Data Pergerakan Keluar
st.header("🚶‍♂️ Pergerakan Keluar")
if "keluar_data" not in st.session_state:
    st.session_state.keluar_data = []

# Tambah Pergerakan Keluar
with st.expander("Tambah Pergerakan Keluar"):
    nama_keluar = st.text_input("Nama", key="keluar_nama")
    no_smpp_keluar = st.text_input("No. SMPP", key="keluar_no_smpp")
    epd_keluar = st.date_input("EPD (Pilih Tarikh)", value=date.today(), min_value=date.today(), max_value=date(2050, 12, 31), key="keluar_epd")
    catatan_keluar = st.text_area("Catatan", key="keluar_catatan")
    if st.button("Tambah Pergerakan Keluar"):
        st.session_state.keluar_data.append({
            "nama": nama_keluar,
            "no_smpp": no_smpp_keluar,
            "epd": epd_keluar,
            "catatan": catatan_keluar,
            "tarikh": selected_date,
            "institusi": institusi
        })
        st.success("Pergerakan Keluar berjaya ditambah!")

# Paparkan Senarai Pergerakan Keluar
if st.session_state.keluar_data:
    st.write("### Senarai Pergerakan Keluar")
    for idx, data in enumerate(st.session_state.keluar_data):
        st.markdown(f"**{idx + 1}. Nama**: {data['nama']}")
        st.markdown(f"- No. SMPP: {data['no_smpp']}")
        st.markdown(f"- EPD: {data['epd']}")
        st.markdown(f"- Catatan: {data['catatan']}")
        st.markdown(f"- Tarikh: {data['tarikh']}")
        st.markdown(f"- Institusi: {data['institusi']}")
        if st.button(f"Hapus Pergerakan Keluar {idx + 1}", key=f"hapus_keluar_{idx}"):
            st.session_state.keluar_data.pop(idx)
            st.experimental_rerun()

# Butang Submit untuk Pergerakan Keluar
if st.button("Submit Pergerakan Keluar"):
    st.success("Semua data pergerakan keluar telah disubmit!")
    st.session_state.keluar_data = []  # Kosongkan data selepas submit

# Data Pergerakan Masuk
st.header("🚶‍♂️ Pergerakan Masuk")
if "masuk_data" not in st.session_state:
    st.session_state.masuk_data = []

# Tambah Pergerakan Masuk
with st.expander("Tambah Pergerakan Masuk"):
    nama_masuk = st.text_input("Nama", key="masuk_nama")
    no_smpp_masuk = st.text_input("No. SMPP", key="masuk_no_smpp")
    epd_masuk = st.date_input("EPD (Pilih Tarikh)", value=date.today(), min_value=date.today(), max_value=date(2050, 12, 31), key="masuk_epd")
    catatan_masuk = st.text_area("Catatan", key="masuk_catatan")
    if st.button("Tambah Pergerakan Masuk"):
        st.session_state.masuk_data.append({
            "nama": nama_masuk,
            "no_smpp": no_smpp_masuk,
            "epd": epd_masuk,
            "catatan": catatan_masuk,
            "tarikh": selected_date,
            "institusi": institusi
        })
        st.success("Pergerakan Masuk berjaya ditambah!")

# Paparkan Senarai Pergerakan Masuk
if st.session_state.masuk_data:
    st.write("### Senarai Pergerakan Masuk")
    for idx, data in enumerate(st.session_state.masuk_data):
        st.markdown(f"**{idx + 1}. Nama**: {data['nama']}")
        st.markdown(f"- No. SMPP: {data['no_smpp']}")
        st.markdown(f"- EPD: {data['epd']}")
        st.markdown(f"- Catatan: {data['catatan']}")
        st.markdown(f"- Tarikh: {data['tarikh']}")
        st.markdown(f"- Institusi: {data['institusi']}")
        if st.button(f"Hapus Pergerakan Masuk {idx + 1}", key=f"hapus_masuk_{idx}"):
            st.session_state.masuk_data.pop(idx)
            st.experimental_rerun()

# Butang Submit untuk Pergerakan Masuk
if st.button("Submit Pergerakan Masuk"):
    st.success("Semua data pergerakan masuk telah disubmit!")
    st.session_state.masuk_data = []  # Kosongkan data selepas submit