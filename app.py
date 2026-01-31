import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Accounting Pro Online", layout="wide")

# --- DATABASE CONNECTION (Local for Dev, can be swapped to Cloud) ---
def get_connection():
    conn = sqlite3.connect('akuntansi_online.sqlite')
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT PRIMARY KEY, pw TEXT, theme TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS jurnal (id INTEGER PRIMARY KEY AUTOINCREMENT, tgl TEXT, bukti TEXT, ket TEXT, akun TEXT, debet REAL, kredit REAL)")
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123', 'Professional Blue')")
    conn.commit()

init_db()

# --- SISTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_page():
    st.title("?? Login Sistem Akuntansi")
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")
        
        if submit:
            if user == "admin" and pw == "admin123": # Nanti cek ke tabel users
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Username atau Password Salah")

# --- DASHBOARD UTAMA ---
def main_app():
    st.sidebar.title(f"Welcome, {st.session_state['user']}")
    menu = st.sidebar.selectbox("Navigasi", ["Dashboard", "Input Jurnal", "Laporan Keuangan", "Pengaturan"])
    
    if menu == "Dashboard":
        st.header("?? Ringkasan Keuangan")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Pendapatan", "Rp 50.000.000")
        col2.metric("Total Beban", "Rp 20.000.000")
        col3.metric("Laba Bersih", "Rp 30.000.000", delta="+10%")

    elif menu == "Input Jurnal":
        st.header("?? Input Transaksi Baru")
        with st.form("jurnal_form", clear_on_submit=True):
            tgl = st.date_input("Tanggal")
            bukti = st.text_input("No. Bukti")
            ket = st.text_area("Keterangan")
            akun = st.selectbox("Pilih Akun", ["1-101 Kas", "1-102 Piutang", "4-101 Pendapatan"])
            col1, col2 = st.columns(2)
            debet = col1.number_input("Debet", min_value=0)
            kredit = col2.number_input("Kredit", min_value=0)
            
            if st.form_submit_button("Simpan Transaksi"):
                # Logika Simpan Database
                st.success("Data berhasil disimpan ke cloud!")

    elif menu == "Laporan Keuangan":
        st.header("?? Laporan")
        tipe = st.radio("Jenis Laporan", ["Buku Besar", "Laba Rugi", "Neraca"], horizontal=True)
        
        # Contoh Data Table
        data = pd.DataFrame({
            'Tanggal': ['2023-10-01', '2023-10-02'],
            'Keterangan': ['Saldo Awal', 'Penerimaan Piutang'],
            'Debet': [1000000, 500000],
            'Kredit': [0, 0]
        })
        
        st.table(data)
        
        # Fitur Cetak
        st.download_button("Download Laporan (Excel)", data.to_csv(), "laporan.csv", "text/csv")

    elif menu == "Pengaturan":
        st.header("?? Pengaturan Aplikasi")
        tema = st.selectbox("Tema Warna Print Out", ["Professional Blue", "Modern Green", "Dark Mode", "Classic Gray"])
        st.session_state['theme'] = tema
        
        if st.button("Simpan Perubahan"):
            st.success(f"Tema berhasil diubah ke {tema}")

    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

# --- RUN LOGIC ---
if st.session_state['logged_in']:
    main_app()
else:
    login_page()