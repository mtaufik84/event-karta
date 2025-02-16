import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine, text
import pandas as pd
from dash.exceptions import PreventUpdate

# Registrasi halaman Karang Taruna
dash.register_page(__name__, path="/karang-taruna", name="Karang Taruna")

# Koneksi ke database MySQL
engine = create_engine("mysql+pymysql://root:@127.0.0.1/kartadb")

# Layout utama
layout = html.Div([    
    html.H2("Dashboard Karang Taruna", className="text-center", style={"margin-bottom": "20px", 'color': 'black'}),  # Judul dashboard

    # Container untuk form input
    html.Div([        
        # Dropdown untuk memilih Karang Taruna
        dcc.Dropdown(
            id='karangtaruna-dropdown',
            options=[],  # Akan diisi melalui callback
            placeholder='Pilih Karang Taruna',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Input Nama Karang Taruna
        dcc.Input(
            id='karangtaruna-name-input',
            type='text',
            placeholder='Masukkan Nama Karang Taruna',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),
        
        # Input Alamat
        dcc.Input(
            id='karangtaruna-address-input',
            type='text',
            placeholder='Masukkan Alamat Karang Taruna',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Input Nama Acara
        dcc.Input(
            id='proposal-name-input',
            type='text',
            placeholder='Masukkan Nama Acara',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Tombol CRUD
        html.Div([
            html.Button('Tambah Karang Taruna', id='create-karangtaruna-button', n_clicks=0, 
                        style={'background-color': 'green', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
            html.Button('Perbarui Karang Taruna', id='update-karangtaruna-button', n_clicks=0, 
                        style={'background-color': 'blue', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
            html.Button('Hapus Karang Taruna', id='delete-karangtaruna-button', n_clicks=0, 
                        style={'background-color': 'red', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
        ], style={'text-align': 'center'}),  # Tombol CRUD untuk Karang Taruna

        # Output hasil
        html.Div(id='karangtaruna-output', style={'margin-top': '20px', 'font-size': '18px', 'color': 'darkblue'}),  # Keterangan hasil

    ], style={'text-align': 'center', 'margin-top': '50px', 'background-color': '#d3e8eb', 'border-radius': '10px', 'padding': '20px'}),  # Container input form

    # Tabel untuk menampilkan data Karang Taruna
    html.Div([  
        html.Table(
            id='karangtaruna-table',
            style={'width': '50%', 'margin': '20px auto', 'border-collapse': 'collapse'},
            children=[html.Tr([html.Th('Nama Karang Taruna', style={'text-align': 'center'}), html.Th('Alamat', style={'text-align': 'center'})])],
        ),
    ]),

], style={'background-color': '#d3e8eb', 'padding': '20px', 'min-height': '100vh'})  # Full background for the page


# Callback untuk memperbarui dropdown dengan semua Karang Taruna
@dash.callback(
    Output('karangtaruna-dropdown', 'options'),
    Input('karangtaruna-dropdown', 'id')  # Trigger pertama kali saat halaman dimuat
)
def update_karangtaruna_dropdown(_):
    try:
        with engine.connect() as conn:
            query = text("SELECT ID_KarangTaruna, Nama FROM karangtaruna")  # Mengambil semua Karang Taruna
            result = conn.execute(query).fetchall()
        return [{'label': row[1], 'value': row[0]} for row in result]  # Menampilkan semua Karang Taruna
    except Exception as e:
        print(f"Error: {e}")
        return [{'label': 'Tidak ada data', 'value': None}] 


# Callback untuk menangani Create, Update, Delete Karang Taruna
@dash.callback(
    Output('karangtaruna-output', 'children'),
    Output('karangtaruna-table', 'children'),
    Input('create-karangtaruna-button', 'n_clicks'),
    Input('update-karangtaruna-button', 'n_clicks'),
    Input('delete-karangtaruna-button', 'n_clicks'),
    State('karangtaruna-name-input', 'value'),
    State('karangtaruna-address-input', 'value'),
    State('proposal-name-input', 'value'),
    State('karangtaruna-dropdown', 'value')
)
def manage_karangtaruna(n_create, n_update, n_delete, name, address, proposal_name, selected_karangtaruna_id):
    if not (n_create or n_update or n_delete):
        raise PreventUpdate

    if not name and not address and not proposal_name:
        return "Harap isi data yang valid.", []

    with engine.connect() as conn:
        # CREATE
        if n_create:
            query = text("""
                INSERT INTO karangtaruna (Nama, Alamat) 
                VALUES (:name, :address)
            """)
            conn.execute(query, {'name': name, 'address': address})
            conn.commit()

            # If the proposal_name is filled, insert it into the proposal table
            if proposal_name:
                query_proposal = text("""
                    INSERT INTO proposal (Nama_Acara, ID_KarangTaruna)
                    VALUES (:proposal_name, LAST_INSERT_ID())
                """)
                conn.execute(query_proposal, {'proposal_name': proposal_name})
                conn.commit()

            return f"Karang Taruna {name} berhasil ditambahkan!", get_karangtaruna_table()

        # UPDATE
        elif n_update and selected_karangtaruna_id:
            query = text("""
                UPDATE karangtaruna 
                SET Nama = :name, Alamat = :address 
                WHERE ID_KarangTaruna = :id
            """)
            conn.execute(query, {'name': name, 'address': address, 'id': selected_karangtaruna_id})
            conn.commit()

            # If the proposal_name is filled, update the proposal
            if proposal_name:
                query_proposal = text("""
                    UPDATE proposal 
                    SET Nama_Acara = :proposal_name 
                    WHERE ID_KarangTaruna = :id
                """)
                conn.execute(query_proposal, {'proposal_name': proposal_name, 'id': selected_karangtaruna_id})
                conn.commit()

            return f"Karang Taruna {name} berhasil diperbarui!", get_karangtaruna_table()

        # DELETE
        elif n_delete and selected_karangtaruna_id:
            query = text("""
                DELETE FROM karangtaruna WHERE ID_KarangTaruna = :id
            """)
            conn.execute(query, {'id': selected_karangtaruna_id})
            conn.commit()

            # Optionally, delete the related proposal too
            query_delete_proposal = text("""
                DELETE FROM proposal WHERE ID_KarangTaruna = :id
            """)
            conn.execute(query_delete_proposal, {'id': selected_karangtaruna_id})
            conn.commit()

            return f"Karang Taruna dengan ID {selected_karangtaruna_id} berhasil dihapus!", get_karangtaruna_table()

    return "Terjadi kesalahan! Pastikan data valid.", []


# Fungsi untuk mengambil data Karang Taruna dan menampilkan tabel
def get_karangtaruna_table():
    with engine.connect() as conn:
        query = text("""SELECT Nama, Alamat FROM karangtaruna""")
        result = conn.execute(query).fetchall()

        if not result:
            return [html.Tr([html.Th('Nama Karang Taruna', style={'text-align': 'center'}), html.Th('Alamat', style={'text-align': 'center'})]),
                    html.Tr([html.Td("Tidak ada data", style={'text-align': 'center'}), html.Td("-", style={'text-align': 'center'})])]

        rows = [html.Tr([html.Td(row[0], style={'text-align': 'center'}), html.Td(row[1], style={'text-align': 'center'})]) for row in result]
        return [html.Tr([html.Th('Nama Karang Taruna', style={'text-align': 'center'}), html.Th('Alamat', style={'text-align': 'center'})])] + rows