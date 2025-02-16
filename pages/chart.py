import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Registrasi halaman chart
dash.register_page(__name__, path='/chart', name="Chart")

# Layout halaman chart
layout = html.Div([
    html.H1("Distribusi Donasi", className="text-center"),
    
    # Komponen upload untuk file CSV
    dcc.Upload(
        id='upload-data',
        children=html.Button('Browse CSV File'),
        multiple=False
    ),
    
    # Menampilkan grafik
    dcc.Graph(id='graph_output'),
    
    # Dropdown untuk memilih jenis grafik
    dcc.Dropdown(
        id='chart_type',
        options=[
            {'label': 'Diagram Batang', 'value': 'bar'},
            {'label': 'Diagram Garis', 'value': 'line'}
        ],
        value='bar'  # Nilai default
    )
], style={"background-color": "#d3e8eb", "padding": "20px"})  # Menambahkan background abu-abu

# Callback untuk menampilkan grafik berdasarkan file yang di-upload dan tipe grafik
@dash.callback(
    Output('graph_output', 'figure'),
    [Input('upload-data', 'contents'),
     Input('chart_type', 'value')]
)
def update_graph(uploaded_file, chart_type):
    if uploaded_file is not None:
        # Mengambil konten file CSV
        content = uploaded_file.split(",")[1]
        import base64
        from io import StringIO
        
        # Decode base64 file
        decoded = base64.b64decode(content)
        file = StringIO(decoded.decode('utf-8'))
        
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(file)
        
        # Menyiapkan data untuk chart
        if 'Nama_Acara' in df.columns and 'Total_Donasi' in df.columns:
            figure = go.Figure(data=[
                go.Bar(x=df['Nama_Acara'], y=df['Total_Donasi']) if chart_type == 'bar' else 
                go.Scatter(x=df['Nama_Acara'], y=df['Total_Donasi'], mode='lines')
            ])
            figure.update_layout(
                title='Distribusi Donasi per Acara',
                xaxis_title='Nama Acara',
                yaxis_title='Total Donasi',
                template='plotly_dark'
            )
            return figure
    return go.Figure()