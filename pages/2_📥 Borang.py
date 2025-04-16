import streamlit as st
import os
import json
from datetime import datetime, date

st.set_page_config(page_title="📥 Borang Pengisian Harian", layout="wide")
st.title("📥 Borang Pengisian Data Harian")

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

col1, col2 = st.columns(2)
with col1:
    tarikh = st.date_input("Tarikh", value=datetime.today(), min_value=date(2008, 1, 1))
with col2:
    program = st.selectbox("Program", ["PAROL", "PBSL", "PBL (SHG)", "PRP", "PRPI", "PKW"])


negeri_daerah = {
    "Johor": ["Batu Pahat", "Johor Bahru", "Kluang", "Kota Tinggi", "Mersing", "Muar", "Pontian", "Segamat", "Tangkak"],
    "Kedah": ["Baling", "Bandar Baharu", "Kota Setar", "Kuala Muda", "Kubang Pasu", "Kulim", "Langkawi", "Padang Terap", "Pendang", "Pokok Sena", "Sik", "Yan"],
    "Kelantan": ["Bachok", "Gua Musang", "Jeli", "Kota Bharu", "Kuala Krai", "Machang", "Pasir Mas", "Pasir Puteh", "Tanah Merah", "Tumpat"],
    "Melaka": ["Alor Gajah", "Jasin", "Melaka Tengah"],
    "Negeri Sembilan": ["Jelebu", "Jempol", "Kuala Pilah", "Port Dickson", "Rembau", "Seremban", "Tampin"],
    "Pahang": ["Bentong", "Bera", "Cameron Highlands", "Jerantut", "Kuantan", "Lipis", "Maran", "Pekan", "Raub", "Rompin", "Temerloh"],
    "Perak": ["Bagan Datuk", "Bagan Serai", "Batu Gajah", "Hilir Perak", "Kampar", "Kuala Kangsar", "Larut Matang", "Lenggong", "Manjung", "Muallim", "Parit Buntar", "Perak Tengah", "Selama", "Taiping", "Teluk Intan"],
    "Perlis": ["Kangar", "Padang Besar", "Arau"],
    "Pulau Pinang": ["Barat Daya", "Seberang Perai Tengah", "Seberang Perai Selatan", "Seberang Perai Utara", "Timur Laut"],
    "Sabah": ["Beaufort", "Beluran", "Keningau", "Kota Belud", "Kota Kinabalu", "Kota Marudu", "Kuala Penyu", "Kudat", "Kunak", "Lahad Datu", "Nabawan", "Papar", "Penampang", "Pensiangan", "Putatan", "Ranau", "Sandakan", "Semporna", "Sipitang", "Tambunan", "Tawau", "Tenom", "Tuaran"],
    "Sarawak": ["Betong", "Bintulu", "Kapit", "Kuching", "Limbang", "Lubok Antu", "Miri", "Mukah", "Samarahan", "Sarikei", "Serian", "Sibu", "Sri Aman"],
    "Selangor": ["Gombak", "Hulu Langat", "Hulu Selangor", "Klang", "Kuala Langat", "Kuala Selangor", "Petaling", "Sabak Bernam", "Sepang"],
    "Terengganu": ["Besut", "Dungun", "Hulu Terengganu", "Kemaman", "Kuala Nerus", "Kuala Terengganu", "Marang", "Setiu"]
}

# Senarai negeri bergantung kepada program
if program == "PRP":
    negeri_list = [negeri for negeri in negeri_daerah.keys() if negeri not in ["Perlis", "Pulau Pinang", "Perak", "Melaka", "Pahang", "Sarawak", "Terengganu"]]
else:
    negeri_list = list(negeri_daerah.keys())

negeri = st.selectbox("Pilih Negeri", negeri_list, key="grid_negeri")
daerah_list = negeri_daerah[negeri]

folder_negeri = os.path.join(DATA_FOLDER, tarikh.strftime("%Y-%m-%d"), negeri.lower())
os.makedirs(folder_negeri, exist_ok=True)

def simpan_daerah(data, daerah, program):
    daerah_key = daerah.lower()
    fpath = os.path.join(folder_negeri, f"{daerah_key}_{program.lower()}.json")
    with open(fpath, "w") as f:
        json.dump(data, f, indent=2)
    st.success(f"✅ Data {daerah} berjaya disimpan!")

# Status pengisian daerah hanya untuk program PAROL, PBSL, PBL (SHG), dan PKW
if program in ("PAROL", "PBSL", "PBL (SHG)", "PKW"):
    # Pastikan 'status_isi' didefinisikan berdasarkan keadaan semasa
    status_isi = {
        daerah: os.path.exists(os.path.join(folder_negeri, f"{daerah.lower()}_{program.lower()}.json"))
        for daerah in daerah_list
    }

    # Periksa daerah yang belum dihantar
    belum_isi = [d for d, s in status_isi.items() if not s]
    if belum_isi:
        st.warning(f"⚠️ Daerah belum hantar ({len(belum_isi)}): {', '.join(belum_isi)}")
    else:
        st.success("✅ Semua daerah telah lengkap dihantar.")
# Paparkan borang hanya jika program sesuai
if program in ("PAROL", "PBSL", "PBL (SHG)"):
    st.markdown("### 🧾 Borang Pengisian Mengikut Daerah")

    for daerah in daerah_list:
        with st.expander(f"📍 {daerah}", expanded=False):
            if status_isi[daerah]:
                st.info("✅ Data telah dihantar untuk daerah ini.")
                continue

            st.markdown("#### 👤 Jantina & Bangsa")
            col1, col2 = st.columns(2)
            with col1:
                lelaki = st.number_input("Lelaki", min_value=0, key=f"l_{daerah}")
                melayu = st.number_input("Melayu", min_value=0, key=f"m_{daerah}")
                india = st.number_input("India", min_value=0, key=f"i_{daerah}")
            with col2:
                wanita = st.number_input("Wanita", min_value=0, key=f"w_{daerah}")
                cina = st.number_input("Cina", min_value=0, key=f"c_{daerah}")
                lain_bangsa = st.number_input("Lain-lain Bangsa", min_value=0, key=f"lbb_{daerah}")

            st.markdown("#### 💼 Pekerjaan")
            pekerjaan = {p: st.number_input(p, min_value=0, key=f"pkj_{p}_{daerah}") for p in ["Majikan", "Sendiri", "Keluarga", "Tidak Bekerja"]}

            st.markdown("#### 🏠 Penempatan")
            penempatan = {p: st.number_input(p, min_value=0, key=f"pt_{p}_{daerah}") for p in ["Keluarga", "Majikan", "NGO/Swasta", "RP Jabatan"]}

            st.markdown("#### 💊 Rawatan")
            rawatan = {p: st.number_input(p, min_value=0, key=f"raw_{p}_{daerah}") for p in ["Cure and Care", "Methadone"]}

            st.markdown("#### 🚔 Penahanan Sementara")
            penahanan = {p: st.number_input(p, min_value=0, key=f"tnh_{p}_{daerah}") for p in ["Langgar Syarat Parol", "Penahanan Polis", "Ada Kes Lain", "Methadone", "Penggantungan", "Lain-lain"]}

            st.markdown("#### ❌ Pelanggaran Syarat")
            pelanggaran = {p: st.number_input(p, min_value=0, key=f"plg_{p}_{daerah}") for p in ["Menghilangkan Diri", "Pembatalan"]}

            st.markdown("#### 📅 Tamat Parol")
            tamat_parol = st.number_input("Tamat Parol 2025", min_value=0, key=f"tamat_{daerah}")
            jumlah_tamat = st.number_input("Jumlah Tamat Keseluruhan 2025", min_value=0, key=f"jtamat_{daerah}")

            st.markdown("#### 🧰 Jenis Pekerjaan")
            jenis = {label: st.number_input(label, min_value=0, key=f"jp_{label}_{daerah}") for label in [
                "Pekerja Am", "Berniaga", "Perladangan", "Pembuatan", "Perkilangan",
                "Pembantu Kedai", "Pemandu", "Ternakan", "Kerani", "Mekanik/Teknikal",
                "Lain-lain", "Tidak Bekerja"
            ]}

            st.markdown("#### 📝 Catatan")
            catatan = st.text_area("Catatan", key=f"cat_{daerah}")

            # Data yang akan disimpan
            data_daerah = {
                "Tarikh": tarikh.strftime("%Y-%m-%d"),
                "Program": program,
                "Negeri": negeri,
                "Daerah": daerah,
                "Jantina & Bangsa": {
                    "Lelaki": lelaki, "Wanita": wanita, "Melayu": melayu,
                    "Cina": cina, "India": india, "Lain-lain Bangsa": lain_bangsa
                },
                "Pekerjaan": pekerjaan,
                "Penempatan": penempatan,
                "Rawatan": rawatan,
                "Penahanan Sementara": penahanan,
                "Pelanggaran Syarat": pelanggaran,
                "Tamat Parol 2025": tamat_parol,
                "Jumlah Tamat Keseluruhan 2025": jumlah_tamat,
                "Jenis Pekerjaan": jenis,
                "Catatan": catatan
            }

            if st.button(f"✅ Simpan {daerah}", key=f"simpan_{daerah}"):
                simpan_daerah(data_daerah, daerah, program)  

# Borang Pengisian untuk PKW
if program == "PKW":
    st.markdown("### 🧾 Borang Pengisian Mengikut Daerah")

    for daerah in daerah_list:
        with st.expander(f"📍 {daerah}", expanded=False):
            if status_isi[daerah]:
                st.info("✅ Data telah dihantar untuk daerah ini.")
                continue

            # Bahagian Jumlah Semasa
            st.markdown("#### 📊 Jumlah Semasa")
            jumlah_semasa = st.number_input("Jumlah Pesalah Semasa", min_value=0, key=f"jumlah_semasa_{daerah}")

            # Bahagian Jantina & Bangsa
            st.markdown("#### 👤 Jantina & Bangsa")
            col1, col2 = st.columns(2)
            with col1:
                lelaki = st.number_input("Lelaki", min_value=0, key=f"l_{daerah}")
                melayu = st.number_input("Melayu", min_value=0, key=f"m_{daerah}")
                india = st.number_input("India", min_value=0, key=f"i_{daerah}")
            with col2:
                wanita = st.number_input("Wanita", min_value=0, key=f"w_{daerah}")
                cina = st.number_input("Cina", min_value=0, key=f"c_{daerah}")
                lain_bangsa = st.number_input("Lain-lain Bangsa", min_value=0, key=f"lbb_{daerah}")

            # Bahagian Status PKW
            st.markdown("#### ⚖️ Status PKW")
            col3, col4 = st.columns(2)
            with col3:
                pkw_jenayah = st.number_input("PKW Jenayah", min_value=0, key=f"pkw_jenayah_{daerah}")
            with col4:
                pkw_syariah = st.number_input("PKW Syariah", min_value=0, key=f"pkw_syariah_{daerah}")

            # Bahagian Jenis Kesalahan
            st.markdown("#### 🚨 Jenis Kesalahan")
            kesalahan = {
                p: st.number_input(p, min_value=0, key=f"kesalahan_{p}_{daerah}")
                for p in ["Dadah", "Jenayah", "Syariah", "Lain-lain"]
            }

            # Bahagian Pembatalan dan Tamat Perintah
            st.markdown("#### ❌ Pembatalan dan Tamat Perintah")
            col5, col6 = st.columns(2)
            with col5:
                pembatalan = st.number_input("Pembatalan", min_value=0, key=f"pembatalan_{daerah}")
            with col6:
                tamat_perintah = st.number_input("Tamat Perintah", min_value=0, key=f"tamat_perintah_{daerah}")

            # Bahagian Catatan
            st.markdown("#### 📝 Catatan")
            catatan = st.text_area("Catatan", key=f"cat_{daerah}")

            # Data yang akan disimpan
            data_daerah = {
                "Tarikh": tarikh.strftime("%Y-%m-%d"),
                "Program": program,
                "Negeri": negeri,
                "Daerah": daerah,
                "Jumlah Semasa": jumlah_semasa,
                "Jantina & Bangsa": {
                    "Lelaki": lelaki, "Wanita": wanita, "Melayu": melayu,
                    "Cina": cina, "India": india, "Lain-lain Bangsa": lain_bangsa
                },
                "Status PKW": {
                    "PKW Jenayah": pkw_jenayah,
                    "PKW Syariah": pkw_syariah
                },
                "Jenis Kesalahan": kesalahan,
                "Pembatalan": pembatalan,
                "Tamat Perintah": tamat_perintah,
                "Catatan": catatan
            }

            # Butang Simpan
            if st.button(f"✅ Simpan {daerah}", key=f"simpan_{daerah}"):
                simpan_daerah(data_daerah, daerah, program)

if program == "PRP":
    pilihan_prp = st.selectbox("Pilih PRP", [
        "PRP Kuala Muda", "PRP Kuala Krai", "PRP Sepang",
        "PRP Mantin", "PRP Kluang", "PRP Tuaran", "Tiada"
    ])

    st.header("📝 Bahagian PRP")
    col1, col2, col3 = st.columns(3)
    ods = col1.number_input("PRP (ODS)", min_value=0, key="ods_prp")
    odsi = col2.number_input("PRPI (ODSI)", min_value=0, key="odsi_prp")
    odsa = col3.number_input("3P (ODSA)", min_value=0, key="odsa_prp")

    mahkamah = st.number_input("Mahkamah", min_value=0, key="mahkamah_prp")
    temuduga = st.number_input("Temuduga", min_value=0, key="temuduga_prp")
    hospital = st.number_input("Hospital", min_value=0, key="hospital_prp")
    tumpeng = st.number_input("Tumpang", min_value=0, key="tumpeng_prp")

    # Header untuk kategori Jantina
    st.subheader("Jantina")
    col_jantina_1, col_jantina_2 = st.columns(2)

    # Input untuk kategori Jantina
    with col_jantina_1:
        lelaki = st.number_input("Lelaki", min_value=0, key="lelaki_prp")
    with col_jantina_2:
        wanita = st.number_input("Wanita", min_value=0, key="wanita_prp")

    # Header untuk kategori Bangsa
    st.subheader("Bangsa")
    col_bangsa_1, col_bangsa_2 = st.columns(2)

    # Input untuk kategori Bangsa
    with col_bangsa_1:
        melayu = st.number_input("Melayu", min_value=0, key="melayu_prp")
        cina = st.number_input("Cina", min_value=0, key="cina_prp")
    with col_bangsa_2:
        india = st.number_input("India", min_value=0, key="india_prp")
        llb = st.number_input("LLB", min_value=0, key="llb_prp")
        wa = st.number_input("W/A", min_value=0, key="wa_prp")

    # Header untuk kategori Keluar Program
    st.subheader("Keluar Program")
    col_program_1, col_program_2 = st.columns(2)

    # Input untuk kategori Keluar Program
    with col_program_1:
        parol = st.number_input("Parol", min_value=0, key="parol_prp")
        pbsl = st.number_input("PBSL", min_value=0, key="pbsl_prp")
    with col_program_2:
        kesalahan_tatatertib = st.number_input("Kesalahan Tatatertib", min_value=0, key="tatatertib_prp")
        masalah_kesihatan_pindah = st.number_input("Masalah Kesihatan/Pindah Lokasi Lain", min_value=0, key="masalah_kesihatan_prp")

    # Butang simpan
    if st.button("✅ Simpan PRP", key="simpan_prpi"):
        st.session_state["prpi_data"] = st.session_state.syarikat_list
        st.success("✅ Data PRP berjaya disimpan!")


if program == "PRPI":
    pilihan_prpi = st.selectbox("Pilih PRPI", [
        "RTI Sg. Buloh", "RTI Penor", "RTI Muar",
        "PKK Sg. Petani", "PKK Batu Pahat", "PRP Tuaran", "Tiada"
    ])

    st.header("📝 Bahagian PRPI")

    # Simpan senarai syarikat dalam session state
    if "syarikat_list" not in st.session_state:
        st.session_state.syarikat_list = [{"id": 1}]  # Mulakan dengan satu borang

    # Fungsi untuk menambah syarikat
    def tambah_syarikat():
        new_id = len(st.session_state.syarikat_list) + 1
        st.session_state.syarikat_list.append({"id": new_id})

    # Fungsi untuk menghapus syarikat terakhir
    def hapus_syarikat():
        if len(st.session_state.syarikat_list) > 1:  # Pastikan sekurang-kurangnya satu borang kekal
            st.session_state.syarikat_list.pop()

    # Paparkan borang untuk setiap syarikat dalam senarai
    for syarikat in st.session_state.syarikat_list:
        i = syarikat["id"]
        st.markdown(f"### Syarikat {i}")
        nama_industri = st.text_input(f"Nama Syarikat (Syarikat {i})", key=f"nama_syarikat_{i}_prpi")

        col1, col2, col3 = st.columns(3)
        jumlah_kapasiti = col1.number_input(f"Jumlah Kapasiti (Syarikat {i})", min_value=0, key=f"kapasiti_{i}_prpi")
        jumlah_bekerja = col2.number_input(f"Jumlah Bekerja (Syarikat {i})", min_value=0, key=f"bekerja_{i}_prpi")
        urusan_penjara = col3.number_input(f"Urusan Penjara (Syarikat {i})", min_value=0, key=f"penjara_{i}_prpi")

        col4, col5 = st.columns(2)
        rawatan = col4.number_input(f"Rawatan (Syarikat {i})", min_value=0, key=f"rawatan_{i}_prpi")
        lain_lain = col5.number_input(f"Lain-lain (Syarikat {i})", min_value=0, key=f"lain_{i}_prpi")

        st.markdown("#### Jantina")
        col_jantina1, col_jantina2 = st.columns(2)
        lelaki = col_jantina1.number_input(f"Lelaki (Syarikat {i})", min_value=0, key=f"lelaki_{i}_prpi")
        wanita = col_jantina2.number_input(f"Wanita (Syarikat {i})", min_value=0, key=f"wanita_{i}_prpi")

        st.markdown("#### Bangsa")
        col_bangsa1, col_bangsa2 = st.columns(2)
        melayu = col_bangsa1.number_input(f"Melayu (Syarikat {i})", min_value=0, key=f"melayu_{i}_prpi")
        cina = col_bangsa1.number_input(f"Cina (Syarikat {i})", min_value=0, key=f"cina_{i}_prpi")
        india = col_bangsa2.number_input(f"India (Syarikat {i})", min_value=0, key=f"india_{i}_prpi")
        llb = col_bangsa2.number_input(f"LLB (Syarikat {i})", min_value=0, key=f"llb_{i}_prpi")
        wa = col_bangsa2.number_input(f"W/A (Syarikat {i})", min_value=0, key=f"wa_{i}_prpi")

        col6, col7, col8 = st.columns(3)
        jumlah_bebas = col6.number_input(f"Jumlah Bebas (Syarikat {i})", min_value=0, key=f"bebas_{i}_prpi")
        parol = col7.number_input(f"Parol (Syarikat {i})", min_value=0, key=f"parol_{i}_prpi")
        pbsl = col8.number_input(f"PBSL (Syarikat {i})", min_value=0, key=f"pbsl_{i}_prpi")

        col9, col10 = st.columns(2)
        kesalahan_tatatertib = col9.number_input(f"Kesalahan Tatatertib (Syarikat {i})", min_value=0, key=f"tatatertib_{i}_prpi")
        masalah_kesihatan = col10.number_input(f"Masalah Kesihatan (Syarikat {i})", min_value=0, key=f"masalah_{i}_prpi")

        hantar_institusi = st.number_input(f"Hantar Institusi (Syarikat {i})", min_value=0, key=f"institusi_{i}_prpi")

    # Butang untuk menambah dan menghapus syarikat (pindahkan ke bawah)
    st.markdown("---")
    col_tambah, col_hapus = st.columns(2)
    with col_tambah:
        st.button("Tambah Syarikat", on_click=tambah_syarikat)
    with col_hapus:
        st.button("Hapus Syarikat", on_click=hapus_syarikat)

    # Butang simpan
    if st.button("✅ Simpan PRPI", key="simpan_prpi"):
        st.session_state["prpi_data"] = st.session_state.syarikat_list
        st.success("✅ Data PRPI berjaya disimpan!")