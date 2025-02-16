import dash
from dash import html

# Registrasi halaman
dash.register_page(__name__, path="/", name="Introduction")

# Layout halaman introduction
layout = html.Div([
    html.H1("Selamat Datang di Dashboard Karang Taruna", className="text-center"),
    html.P("Dashboard ini menyediakan analisis donasi dan pengelolaan dana untuk berbagai acara Karang Taruna."),
    html.P("Database ini mencakup beberapa tabel yang saling terkait dan berfungsi untuk menyimpan informasi terkait kegiatan Karang Taruna."),
    
    html.Br(),
    
    html.H3("Tabel yang Tersedia dalam Database", className="text-center"),
    html.Ul([
        html.Li("Donatur - Menyimpan informasi tentang para donatur, seperti ID, nama, alamat, dan tanggal pendaftaran."),
        html.Li("Karang Taruna - Berisi data mengenai kelompok Karang Taruna, termasuk ID dan nama kelompok."),
        html.Li("Laporan Dana - Merupakan laporan donasi yang diterima dari berbagai kegiatan."),
        html.Li("Lokasi - Menyimpan informasi terkait dengan lokasi acara, termasuk ID dan nama lokasi."),
        html.Li("Pengeluaran Acara - Tabel ini berisi catatan pengeluaran untuk acara yang diselenggarakan."),
        html.Li("Proposal - Menyimpan data proposal acara, yang berisi nama acara, anggaran, status acara, dan relasi dengan Karang Taruna serta lokasi."),
        html.Li("Transaksi Donatur - Mencatat semua transaksi donasi yang dilakukan oleh para donatur."),
    ]),

    html.Br(),

    html.H3("Diagram Relasi Antar Tabel", className="text-center"),
    html.Img(src="assets/relasi_diagram.png", style={"width": "100%", "height": "auto", "marginTop": "20px"}, className="text-center"),
    
    html.Br(),

    html.H3("Cara Menggunakan Dashboard", className="text-center"),
    html.P("Gunakan menu navigasi di atas untuk mengakses berbagai bagian dashboard, termasuk melihat data, menjalankan query SQL, dan menganalisis distribusi donasi.", className="text-center"),
], style={"background-color": "#d3e8eb", "padding": "20px"})  # Gray background