import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Set Streamlit page configuration
st.set_page_config(page_title="📊 Dashboard Statistik Program", layout="wide")
st.title("📊 Dashboard Statistik Program")

# Sidebar Filters
st.sidebar.header("🛠️ Penapis Data")
kategori = st.sidebar.selectbox("Kategori", ["PPD (Daerah)", "PPN (Negeri)", "IPPM (Keseluruhan)"])
program = st.sidebar.selectbox("Program", ["Semua", "PAROL", "PBSL", "PBL (SHG)", "PRP", "PRPI", "PKW"])
tarikh_mula = st.sidebar.date_input("Tarikh Mula", value=datetime.today() - timedelta(days=30))
tarikh_akhir = st.sidebar.date_input("Tarikh Akhir", value=datetime.today())

# Butang Cari
if st.sidebar.button("Cari"):
    cari_ditekan = True
else:
    cari_ditekan = False

# Dummy data untuk simulasi
@st.cache_data
def load_dummy_data():
    rows = []
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
    for negeri, daerah_list in negeri_daerah.items():
        for daerah in daerah_list:
            for program in ["PAROL", "PBSL", "PRP", "PRPI", "PKW"]:
                rows.append({
                    "Tarikh": datetime.today().strftime("%Y-%m-%d"),
                    "Program": program,
                    "Negeri": negeri,
                    "Daerah": daerah,
                    "Lelaki": 100 + len(daerah),  # Data dummy
                    "Wanita": 50 + len(daerah),  # Data dummy
                    "Melayu": 120 + len(daerah),
                    "Cina": 30 + len(daerah),
                    "India": 20 + len(daerah),
                    "Lain-lain Bangsa": 10 + len(daerah),
                    "Majikan": 30 + len(daerah),
                    "Sendiri": 20 + len(daerah),
                    "Keluarga": 10 + len(daerah),
                    "RP Jabatan": 10 + len(daerah),
                    "Tidak Bekerja": 40 + len(daerah),
                })
    return pd.DataFrame(rows)

# Load dummy data
data = load_dummy_data()

# Filter data berdasarkan pilihan tapisan hanya apabila butang cari ditekan
if cari_ditekan:
    filtered_data = data[
        (pd.to_datetime(data["Tarikh"]) >= pd.to_datetime(tarikh_mula)) &
        (pd.to_datetime(data["Tarikh"]) <= pd.to_datetime(tarikh_akhir))
    ]
    if program != "Semua":
        filtered_data = filtered_data[filtered_data["Program"] == program]

    # Filter mengikut kategori
    if kategori == "PPD (Daerah)":
        filtered_data = filtered_data.groupby(["Daerah", "Program"]).sum(numeric_only=True).reset_index()
    elif kategori == "PPN (Negeri)":
        filtered_data = filtered_data.groupby(["Negeri", "Program"]).sum(numeric_only=True).reset_index()

    # **Paparkan Live View**
    if not filtered_data.empty:
        total_odp = filtered_data[filtered_data["Program"] == "PAROL"]["Lelaki"].sum() + \
                    filtered_data[filtered_data["Program"] == "PAROL"]["Wanita"].sum()
        total_obb = filtered_data[filtered_data["Program"] == "PBSL"]["Lelaki"].sum() + \
                    filtered_data[filtered_data["Program"] == "PBSL"]["Wanita"].sum()
        total_ods = filtered_data[filtered_data["Program"] == "PRP"]["Lelaki"].sum() + \
                    filtered_data[filtered_data["Program"] == "PRP"]["Wanita"].sum()
        total_odsi = filtered_data[filtered_data["Program"] == "PRPI"]["Lelaki"].sum() + \
                     filtered_data[filtered_data["Program"] == "PRPI"]["Wanita"].sum()
        total_pkw = filtered_data[filtered_data["Program"] == "PKW"]["Lelaki"].sum() + \
                    filtered_data[filtered_data["Program"] == "PKW"]["Wanita"].sum()

        total_keseluruhan = total_odp + total_obb + total_ods + total_odsi + total_pkw

    st.markdown("## 📟 Live View: Jumlah Peserta Mengikut Program")
    st.markdown("Bahagian ini memaparkan **jumlah semasa** peserta bagi setiap program dan kumulatif keseluruhan berdasarkan input jantina (Lelaki + Wanita).")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<div style='text-align: center;'><span style='font-size: 40px; font-weight: bold; color: #FF5733;'>{total_odp}</span><br><span style='font-size: 14px; color: #555;'>ODP (PAROL)</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center;'><span style='font-size: 40px; font-weight: bold; color: #33C4FF;'>{total_obb}</span><br><span style='font-size: 14px; color: #555;'>OBB (PBSL)</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align: center;'><span style='font-size: 40px; font-weight: bold; color: #FFC300;'>{total_ods}</span><br><span style='font-size: 14px; color: #555;'>ODS (PRP)</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='text-align: center;'><span style='font-size: 40px; font-weight: bold; color: #C70039;'>{total_odsi}</span><br><span style='font-size: 14px; color: #555;'>ODSI (PRPI)</span></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div style='text-align: center;'><span style='font-size: 40px; font-weight: bold; color: #900C3F;'>{total_pkw}</span><br><span style='font-size: 14px; color: #555;'>PKW</span></div>", unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><span style='font-size: 50px; font-weight: bold; color: #4CAF50;'>{total_keseluruhan}</span><br><span style='font-size: 18px; color: #555;'>Jumlah Kumulatif Keseluruhan</span></div>", unsafe_allow_html=True)

    # **Paparkan Data Ditapis**
    st.markdown("### 📄 Data Ditapis")
    st.dataframe(filtered_data)

    # **Statistik Visual Tambahan**
    st.markdown("## 📊 Statistik Tambahan")

    # **Peratusan Jantina**
    jantina_data = {
        "Lelaki": filtered_data["Lelaki"].sum(),
        "Wanita": filtered_data["Wanita"].sum(),
    }
    fig_jantina = px.pie(values=jantina_data.values(), names=jantina_data.keys(), title="Peratusan Jantina", color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_jantina, use_container_width=True)

    # **Perbandingan Program**
    program_data = filtered_data.groupby("Program")[["Lelaki", "Wanita"]].sum().reset_index()
    fig_program = px.bar(program_data, x="Program", y=["Lelaki", "Wanita"], barmode="group", title="Perbandingan Peserta Berdasarkan Program", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_program, use_container_width=True)

    # **Jumlah Peserta Berdasarkan Negeri**
    if not filtered_data.empty:
        negeri_data = filtered_data.groupby("Negeri")[["Lelaki", "Wanita"]].sum().reset_index()
        negeri_data["Jumlah"] = negeri_data["Lelaki"] + negeri_data["Wanita"]
        fig_negeri = px.bar(
            negeri_data,
            x="Negeri",
            y="Jumlah",
            text="Jumlah",
            title="Jumlah Peserta Berdasarkan Negeri",
            color="Negeri",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_negeri.update_traces(texttemplate='%{text:.0f}', textposition='outside')
        fig_negeri.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig_negeri, use_container_width=True)

    # **Statistik Bangsa**
    bangsa_data = {
        "Melayu": filtered_data["Melayu"].sum(),
        "Cina": filtered_data["Cina"].sum(),
        "India": filtered_data["India"].sum(),
        "Lain-lain Bangsa": filtered_data["Lain-lain Bangsa"].sum()
    }
    fig_bangsa = px.pie(values=bangsa_data.values(), names=bangsa_data.keys(), title="Peratusan Bangsa", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bangsa, use_container_width=True)

    # **Statistik Pekerjaan**
    pekerjaan_data = {
        "Majikan": filtered_data["Majikan"].sum(),
        "Sendiri": filtered_data["Sendiri"].sum(),
        "Keluarga": filtered_data["Keluarga"].sum(),
        "Tidak Bekerja": filtered_data["Tidak Bekerja"].sum(),
    }
    fig_pekerjaan = px.bar(x=pekerjaan_data.keys(), y=pekerjaan_data.values(), title="Bilangan Mengikut Jenis Pekerjaan", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig_pekerjaan, use_container_width=True)
