import dash
from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output, State, ALL
from sqlalchemy import create_engine, text
import pandas as pd

# Registrasi halaman manage data
dash.register_page(__name__, path='/manage-data', name="Kelola Data")

# Koneksi ke database MySQL
engine = create_engine("mysql+pymysql://root:@127.0.0.1/kartadb")

# Fungsi untuk mendapatkan daftar tabel
def get_table_list():
    query = "SHOW TABLES"
    with engine.connect() as conn:
        tables = pd.read_sql(query, conn)
    return [{'label': table, 'value': table} for table in tables.iloc[:, 0].tolist()]

# Layout utama
layout = html.Div([
    html.H2("Kelola Data", className="text-center", style={"margin-bottom": "20px"}),
    
    # Dropdown untuk memilih tabel
    html.Div([
        dcc.Dropdown(
            id='table_selector',
            options=get_table_list(),
            placeholder="Pilih Tabel",
            style={'width': '60%', 'margin': 'auto', 'padding': '10px'}
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Tombol CRUD
    html.Div([
        html.Button("Tambah Data", id='add_button', n_clicks=0, style={'background-color': '#007bff', 'color': 'white', 'padding': '10px', 'border-radius': '5px', 'border': 'none'}),
        html.Button("Update Data", id='update_button', n_clicks=0, style={'background-color': '#ffc107', 'color': 'black', 'padding': '10px', 'margin-left': '10px', 'border-radius': '5px', 'border': 'none'}),
        html.Button("Hapus Data", id='delete_button', n_clicks=0, style={'background-color': '#dc3545', 'color': 'white', 'padding': '10px', 'margin-left': '10px', 'border-radius': '5px', 'border': 'none'})
    ], style={'display': 'flex', 'justify-content': 'center', 'gap': '10px', 'margin-bottom': '20px'}),

    # Tabel data
    html.Div(id='table_container', style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),
    
    # Form CRUD
    html.Div(id='form_container', style={
        'margin': 'auto',
        'width': '50%',
        'border': '1px solid black',
        'padding': '20px',
        'display': 'none',
        'background-color': 'white',
        'border-radius': '10px',
        'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
    })
], style={"background-color": "#d3e8eb", "padding": "20px", "min-height": "100vh"})

# Callback untuk Memuat Data Tabel
@dash.callback(
    Output('table_container', 'children'),
    Input('table_selector', 'value')
)
def update_table(table_name):
    if not table_name:
        return html.Div("Pilih tabel terlebih dahulu.", style={'textAlign': 'center'})
    
    with engine.connect() as conn:
        query = text(f"SELECT * FROM {table_name}")
        df = pd.read_sql(query, conn)
    
    columns = [{"name": col, "id": col} for col in df.columns]
    
    return dash_table.DataTable(
        id="data_table",
        columns=columns,
        data=df.to_dict("records"),
        row_selectable="single",
        selected_rows=[],
        page_size=10,
        style_table={"overflowX": "auto", "width": "90%", "margin": "auto"},
        style_cell={'textAlign': 'center', 'padding': '5px', 'whiteSpace': 'normal', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
    )

# Callback untuk menangani CRUD
@dash.callback(
    Output('form_container', 'children'),
    Output('form_container', 'style'),
    Input('add_button', 'n_clicks'),
    State('table_selector', 'value')
)
def show_form(add_clicks, table_name):
    if not table_name or add_clicks == 0:
        return no_update, {'display': 'none'}
    
    with engine.connect() as conn:
        query = text(f"SHOW COLUMNS FROM {table_name}")
        df = pd.read_sql(query, conn)
    columns = df['Field'].tolist()

    inputs = [
        html.Div([
            html.Label(f"{col}:", style={'font-weight': 'bold'}),
            dcc.Input(id={'type': 'input', 'index': col}, type='text', placeholder=f'Masukkan {col}', style={'width': '100%', 'padding': '5px', 'margin-bottom': '10px'})
        ])
        for col in columns
    ]

    return html.Div([
        html.H4("Tambah Data", style={'text-align': 'center'}),
        *inputs,
        html.Button("Simpan Data", id="save_button", n_clicks=0, style={'background-color': '#28a745', 'color': 'white', 'padding': '10px', 'margin-top': '10px', 'border-radius': '5px', 'border': 'none', 'width': '100%'})
    ]), {'display': 'block'}

# Callback untuk menyimpan data
@dash.callback(
    Output('table_container', 'children', allow_duplicate=True),
    Input('save_button', 'n_clicks'),
    State('table_selector', 'value'),
    State({'type': 'input', 'index': ALL}, 'id'),
    State({'type': 'input', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def save_data(n_clicks, table_name, input_ids, input_values):
    if not table_name or not input_ids or not input_values:
        return no_update

    # Membuat dictionary untuk menyocokkan kolom dan nilai
    data = {input_id['index']: input_value for input_id, input_value in zip(input_ids, input_values) if input_value}

    if not data:
        return no_update

    # Membentuk query SQL secara dinamis
    columns = ', '.join(data.keys())
    placeholders = ', '.join([f":{key}" for key in data.keys()])

    query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")

    # Menjalankan query
    try:
        with engine.connect() as conn:
            conn.execute(query, data)
            conn.commit()
    except Exception as e:
        return html.Div(f"Terjadi kesalahan: {str(e)}", style={'color': 'red', 'text-align': 'center'})

    # Memperbarui tabel
    return update_table(table_name)