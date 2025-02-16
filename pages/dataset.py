from dash import dcc, html, dash_table
import dash
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import pandas as pd

# Registrasi halaman dataset
dash.register_page(__name__, path='/dataset', name="Dataset")

# Koneksi ke MySQL menggunakan SQLAlchemy
engine = create_engine("mysql+pymysql://root:@127.0.0.1/kartadb")

# Layout halaman dataset
layout = html.Div([
    html.Br(),
    html.H2("Pilih Dataset", className="fw-bold text-center"),

    # Dropdown untuk memilih tabel yang akan ditampilkan
    dcc.Dropdown(
        id='table_selector',
        options=[
            {'label': 'Donatur', 'value': 'donatur'},
            {'label': 'Karang Taruna', 'value': 'karangtaruna'},
            {'label': 'Laporan Dana', 'value': 'laporandana'},
            {'label': 'Lokasi', 'value': 'lokasi'},
            {'label': 'Pengeluaran Acara', 'value': 'pengeluaranacara'},
            {'label': 'Proposal', 'value': 'proposal'},
            {'label': 'Transaksi Donatur', 'value': 'transaksidonatur'}
        ],
        value='donatur',  # Tabel default yang ditampilkan
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Menampilkan data tabel yang dipilih
    html.Div(id='table_containers'),

    # Tombol untuk mengunduh CSV
    html.Button("Unduh CSV", id="download_button", n_clicks=0),
    dcc.Download(id="download_csv"),
], style={"background-color": "#d3e8eb", "padding": "20px", "height": "100vh", "display": "flex", "flexDirection": "column"})  # Full height dan warna latar belakang yang ditentukan


# Callback untuk menampilkan data berdasarkan tabel yang dipilih
@dash.callback(
    [Output('table_containers', 'children'),
     Output("download_csv", "data")],
    [Input('table_selector', 'value'),
     Input("download_button", "n_clicks")]
)
def update_table_and_download(table_name, n_clicks):
    try:
        # Query untuk mengambil data sesuai tabel yang dipilih
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)

        # Jika tombol unduh CSV diklik
        if n_clicks > 0:
            return dash_table.DataTable(
                id="dataset_table",
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict("records"),
                style_table={"overflowX": "auto", "maxWidth": "100%"},  # Menambahkan batas lebar tabel
                style_cell={'textAlign': 'center', 'padding': '10px'},  # Menambahkan padding untuk sel
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},  # Warna header
            ), dcc.send_data_frame(df.to_csv, f"{table_name}_data.csv")
        
        return dash_table.DataTable(
            id="dataset_table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            style_table={"overflowX": "auto", "maxWidth": "100%"},  # Menambahkan batas lebar tabel
            style_cell={'textAlign': 'center', 'padding': '10px'},  # Menambahkan padding untuk sel
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},  # Warna header
        ), None

    except Exception as e:
        return html.Div(f"Error: {str(e)}"), None