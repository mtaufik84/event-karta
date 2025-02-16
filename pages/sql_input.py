from dash import dcc, html, dash_table
import dash
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
import pandas as pd

# Registrasi halaman Input SQL Dinamis
dash.register_page(__name__, path='/input-sql', name="Input SQL Dinamis")

# Koneksi ke MySQL menggunakan SQLAlchemy
engine = create_engine("mysql+pymysql://root:@127.0.0.1/kartadb")

# Layout untuk input SQL dinamis
layout = html.Div([
    html.Br(),
    html.H2("Input SQL Dinamis", className="fw-bold text-center"),

    html.Label("Masukkan Query SQL:"),
    dcc.Textarea(id="sql_query", style={"width": "100%", "height": 100}, value="SELECT * FROM proposal"),

    html.Button("Jalankan Query", id="run_sql", n_clicks=0),

    html.Div(id="query_output"),

    # Wrapper div dengan flex untuk memusatkan tabel
    html.Div([
        dash_table.DataTable(
            id="result_table", 
            style_table={"overflowX": "auto", "maxHeight": "400px", "width": "80%"},  # Membatasi tinggi dan lebar
            style_cell={'textAlign': 'center', 'padding': '10px'},  # Menambahkan padding untuk sel
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},  # Warna header
        ),
        # Tombol untuk mengunduh CSV
        html.Button("Unduh CSV", id="download_button", n_clicks=0),
        dcc.Download(id="download_csv_sql"),
        # Store untuk mengirim data ke page Relationship
        dcc.Store(id="sql_query_result")
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})  # Menambahkan gaya untuk memusatkan
], style={"background-color": "#d3e8eb", "padding": "20px", "height": "100vh", "display": "flex", "flexDirection": "column"})  # Full height

# Callback untuk menjalankan query SQL dan menyimpan hasilnya
@dash.callback(
    [Output("query_output", "children"),
     Output("result_table", "data"),
     Output("sql_query_result", "data"),
     Output("download_csv_sql", "data")],
    [Input("run_sql", "n_clicks"),
     Input("download_button", "n_clicks")],
    [State("sql_query", "value")],
    prevent_initial_call=True
)
def run_sql_and_download(n_clicks_run, n_clicks_download, query):
    try:
        print("Running query:", query)  # Debugging print to see the query
        # Menjalankan query dan mengambil data
        df = pd.read_sql(query, engine)

        # Cek jika query dijalankan
        print("Query result:", df.head())  # Debugging print to verify query result
        
        # Mengonversi data ke format CSV jika tombol "Unduh CSV" ditekan
        if n_clicks_download > 0:
            return "Query berhasil dijalankan!", df.to_dict("records"), df.to_dict("records"), dcc.send_data_frame(df.to_csv, "query_results.csv")
        
        return "Query berhasil dijalankan!", df.to_dict("records"), df.to_dict("records"), None
    except Exception as e:
        print("Error:", e)  # Debugging print to show error
        return f"Error: {str(e)}", [], [], None