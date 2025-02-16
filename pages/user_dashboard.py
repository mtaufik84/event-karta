import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine, text
import pandas as pd
from dash.exceptions import PreventUpdate

# Registrasi halaman user dashboard
dash.register_page(__name__, path="/user-dashboard", name="Dashboard Pengguna")

# Koneksi ke database MySQL
engine = create_engine("mysql+pymysql://root:@127.0.0.1/kartadb")

# Layout utama
layout = html.Div([    
    html.H2("Dashboard Pengguna", className="text-center", style={"margin-bottom": "20px", 'color': 'black'}),  # Judul dashboard

    # Container untuk form input
    html.Div([        
        # Dropdown untuk memilih nama acara
        dcc.Dropdown(
            id='acara-dropdown',
            options=[],  # Akan diisi melalui callback
            placeholder='Pilih Acara',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Input Nama Donatur
        dcc.Input(
            id='donatur-input',
            type='text',
            placeholder='Masukkan Nama Donatur',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),
        
        # Input Jumlah Donasi
        dcc.Input(
            id='donation-input',
            type='number',
            placeholder='Jumlah Donasi (IDR)',
            style={'width': '50%', 'margin': '10px auto', 'display': 'block', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ccc', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
        ),

        # Tombol CRUD
        html.Div([
            html.Button('Tambah Donasi', id='create-button', n_clicks=0, 
                        style={'background-color': 'green', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
            html.Button('Perbarui Donasi', id='update-button', n_clicks=0, 
                        style={'background-color': 'blue', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
            html.Button('Hapus Donasi', id='delete-button', n_clicks=0, 
                        style={'background-color': 'red', 'color': 'white', 'padding': '10px 20px', 'margin': '5px', 'border-radius': '5px'}),
        ], style={'text-align': 'center'}),  # Tombol CRUD

        # Output Donasi
        html.Div(id='donation-output', style={'margin-top': '20px', 'font-size': '18px', 'color': 'darkblue'}),  # Keterangan hasil

    ], style={'text-align': 'center', 'margin-top': '50px', 'background-color': '#d3e8eb', 'border-radius': '10px', 'padding': '20px'}),  # Container input form

    # Tabel untuk menampilkan data donasi
    html.Div([  
        html.Table(
            id='donation-table',
            style={'width': '50%', 'margin': '20px auto', 'border-collapse': 'collapse'},
            children=[html.Tr([html.Th('Nama Donatur', style={'text-align': 'center'}), html.Th('Jumlah Donasi', style={'text-align': 'center'})])],
        ),
    ]),
], style={'background-color': '#d3e8eb', 'padding': '20px', 'min-height': '100vh'})  # Full blue background for the page

# Callback untuk memperbarui dropdown acara dengan semua acara
@dash.callback(
    Output('acara-dropdown', 'options'),
    Input('acara-dropdown', 'id')  # Trigger pertama kali saat halaman dimuat
)
def update_acara_dropdown(_):
    with engine.connect() as conn:
        query = text("SELECT ID_Proposal, Nama_Acara FROM proposal")  # Mengambil semua acara
        result = conn.execute(query).fetchall()
    return [{'label': row[1], 'value': row[0]} for row in result]  # Menampilkan semua acara

# Callback untuk menangani Create, Update, Delete Donasi
@dash.callback(
    Output('donation-output', 'children'),
    Output('donation-table', 'children'),
    Input('create-button', 'n_clicks'),
    Input('update-button', 'n_clicks'),
    Input('delete-button', 'n_clicks'),
    State('donatur-input', 'value'),
    State('donation-input', 'value'),
    State('acara-dropdown', 'value')
)
def manage_donation(n_create, n_update, n_delete, donatur, donation_amount, selected_proposal_id):
    if not (n_create or n_update or n_delete):
        raise PreventUpdate

    if not donatur or not selected_proposal_id:
        return "Harap isi nama donatur dan pilih acara.", []

    with engine.connect() as conn:
        # Cek apakah donatur sudah ada
        query = text("SELECT ID_Donatur FROM donatur WHERE Nama = :nama_donatur")
        result = conn.execute(query, {'nama_donatur': donatur}).fetchone()
        
        donatur_id = result[0] if result else None

        # CREATE
        if n_create and donation_amount and donation_amount > 0:
            if not donatur_id:
                return "Donatur tidak ditemukan!", []
            
            query = text(""" 
                INSERT INTO transaksidonatur (ID_Donatur, Jumlah_Donasi, ID_Proposal, Tanggal_Donasi)
                VALUES (:donatur_id, :jumlah_donasi, :id_proposal, NOW())
            """)
            conn.execute(query, {'donatur_id': donatur_id, 'jumlah_donasi': donation_amount, 'id_proposal': selected_proposal_id})
            conn.commit()
            return f"Donasi IDR {donation_amount:,} berhasil ditambahkan!", get_donation_table(selected_proposal_id)

        # UPDATE (Tambah ke Donasi Lama)
        elif n_update and donatur_id:
            query = text("SELECT Jumlah_Donasi FROM transaksidonatur WHERE ID_Donatur = :donatur_id AND ID_Proposal = :id_proposal")
            existing_donation = conn.execute(query, {'donatur_id': donatur_id, 'id_proposal': selected_proposal_id}).fetchone()

            if not existing_donation:
                return "Donatur belum memiliki donasi sebelumnya di acara ini!", []

            current_donation = existing_donation[0]
            new_donation = current_donation + donation_amount  # Menambahkan donasi baru ke donasi lama

            query = text(""" 
                UPDATE transaksidonatur 
                SET Jumlah_Donasi = :new_donasi 
                WHERE ID_Donatur = :donatur_id AND ID_Proposal = :id_proposal
            """)
            conn.execute(query, {'new_donasi': new_donation, 'donatur_id': donatur_id, 'id_proposal': selected_proposal_id})
            conn.commit()
            return f"Donasi diperbarui menjadi IDR {new_donation:,}!", get_donation_table(selected_proposal_id)

        # DELETE
        elif n_delete and donatur_id:
            query = text("DELETE FROM transaksidonatur WHERE ID_Donatur = :donatur_id AND ID_Proposal = :id_proposal")
            conn.execute(query, {'donatur_id': donatur_id, 'id_proposal': selected_proposal_id})

            # Mengecek apakah donatur masih memiliki donasi yang tersisa
            query_check = text(""" 
                SELECT COUNT(*) FROM transaksidonatur 
                WHERE ID_Donatur = :donatur_id
            """)
            count = conn.execute(query_check, {'donatur_id': donatur_id}).scalar()

            # Jika tidak ada lagi transaksi donasi untuk donatur ini, hapus data donatur
            if count == 0:
                query_delete_donatur = text("DELETE FROM donatur WHERE ID_Donatur = :donatur_id")
                conn.execute(query_delete_donatur, {'donatur_id': donatur_id})

            conn.commit()
            return "Donasi berhasil dihapus.", get_donation_table(selected_proposal_id)

    return "Terjadi kesalahan! Pastikan data valid.", []

# Fungsi untuk mengambil data donasi berdasarkan ID Proposal
def get_donation_table(selected_proposal_id):
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT d.Nama, t.Jumlah_Donasi 
                FROM donatur d 
                JOIN transaksidonatur t ON d.ID_Donatur = t.ID_Donatur
                WHERE t.ID_Proposal = :id_proposal
            """)
            result = conn.execute(query, {'id_proposal': selected_proposal_id}).fetchall()

            if not result:
                return [html.Tr([html.Th('Nama Donatur', style={'text-align': 'center'}), html.Th('Jumlah Donasi', style={'text-align': 'center'})]), 
                        html.Tr([html.Td("Tidak ada data", style={'text-align': 'center'}), html.Td("-", style={'text-align': 'center'})])]

            # Membuat table row dari hasil query
            rows = [html.Tr([html.Td(row[0], style={'text-align': 'center'}), html.Td(f"IDR {row[1]:,}", style={'text-align': 'center'})]) for row in result]

            return [html.Tr([html.Th('Nama Donatur', style={'text-align': 'center'}), html.Th('Jumlah Donasi', style={'text-align': 'center'})])] + rows

    except Exception as e:
        print(f"Error saat mengambil data donasi: {e}")
        return [html.Tr([html.Th('Nama Donatur', style={'text-align': 'center'}), html.Th('Jumlah Donasi', style={'text-align': 'center'})]), 
                html.Tr([html.Td("Terjadi kesalahan", style={'text-align': 'center'}), html.Td("-", style={'text-align': 'center'})])]