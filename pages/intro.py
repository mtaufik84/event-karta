import dash
from dash import html

# Registrasi halaman
dash.register_page(__name__, path="/", name="Introduction")

# Layout halaman introduction
layout = html.Div([
    html.H1("Selamat Datang di Dashboard Karang Taruna", className="text-center"),
    html.P(""),
    html.P(""),

    html.Br(),

    html.H3("", className="text-center"),
    html.P(""),

    html.Div([
        html.H4(" Panduan untuk Karang Taruna", className="text-center"),
        html.Ul([
            html.Li("Karang Taruna dapat mengelola data nama, alamat, serta acara yang diselenggarakan.", className="text-justify"),
            html.Li("Melalui fitur CRUD (Create, Read, Update, Delete), Karang Taruna dapat menambah, memperbarui, atau menghapus data terkait Karang Taruna.", className="text-justify"),
            html.Li("Setiap Karang Taruna juga dapat menambahkan nama acara serta anggaran yang terkait dengan acara yang mereka selenggarakan.", className="text-justify"),
            html.Li("Setelah menginputkan data, Karang Taruna dapat melihat laporan lengkap terkait dengan data dan transaksi donasi.", className="text-justify"),
        ], className="card"),

        html.Br(),

        html.H4(" Panduan untuk Donatur", className="text-center"),
        html.Ul([
            html.Li("Donatur dapat memilih acara yang mereka minati melalui dropdown yang tersedia.", className="text-justify"),
            html.Li("Setelah memilih acara, donatur dapat memberikan donasi yang akan tercatat di sistem.", className="text-justify"),
            html.Li("Donatur dapat melihat riwayat donasi mereka untuk setiap acara yang mereka dukung.", className="text-justify"),
            html.Li("Semua donasi yang dilakukan oleh donatur akan tercatat dengan jelas bersama dengan jumlah donasi yang telah diberikan.", className="text-justify"),
        ], className="card"),
        
    ], style={"padding": "20px", "background-color": "#d3e8eb", "border-radius": "10px"}),

    html.Br(),

    html.H3("Fitur Dashboard Karang Taruna", className="text-center"),
    html.P("Dashboard ini memiliki beberapa fitur utama yang mendukung pengelolaan data, transaksi donasi, dan laporan acara:", className="card"),
    html.Ul([
        html.Li("Manajemen data Karang Taruna, acara, dan anggaran.", className="text-justify"),
        html.Li("Pencatatan transaksi donasi dari donatur, serta laporan terkait.", className="text-justify"),
        html.Li("Fitur download CSV untuk mempermudah pengunduhan data yang telah dimasukkan ke dalam sistem.", className="text-justify"),
        html.Li("Tampilan tabel yang rapi dan mudah dipahami untuk memonitor kegiatan Karang Taruna.", className="text-justify"),
    ], className="card"),

    html.Br(),

    html.H3("Cara Menggunakan Dashboard", className="text-center"),
    html.P("Gunakan menu navigasi di atas untuk mengakses berbagai bagian dashboard, seperti mengelola data Karang Taruna, melihat transaksi donasi, serta memanfaatkan laporan yang ada. Anda dapat memilih acara dan memberikan donasi langsung dari dashboard dan melihat kontribusi Anda.", className="card"),

], style={"background-color": "#d3e8eb", "padding": "20px"})  # Gray background