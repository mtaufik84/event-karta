# dashboard.py

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Instansiasi aplikasi Dash terlebih dahulu
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dcc.Link("Intro 📄", href='/', className="nav-link"),
            dcc.Link("Dashboard Pengguna 🧑‍🤝‍🧑", href='/user-dashboard', className="nav-link"),
            dcc.Link("Dataset 📊", href='/dataset', className="nav-link"),
            dcc.Link("Input SQL ⚙️", href='/input-sql', className="nav-link"),
            dcc.Link("Chart 📈", href='/chart', className="nav-link"),
            dcc.Link("Kelola Data 🛠️", href='/manage-data', className="nav-link"),
            dcc.Link("Karang Taruna 🏡", href='/karang-taruna', className="nav-link"),  # Menambahkan emotikon untuk Karang Taruna
        ],
        brand="KarTaDash",
        brand_href="/",
        color="dark",
        dark=True,
        style={"background-color": "#343a40"}
    ),
    dash.page_container  # Kontainer untuk halaman-halaman
])

if __name__ == '__main__':
    app.run_server(debug=True)