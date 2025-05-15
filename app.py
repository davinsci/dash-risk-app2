import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

key_dict = "/tmp/google_creds.json"
with open(key_dict, "w") as f:
    f.write(os.getenv("GOOGLE_CREDS"))
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_dict, scope)
client = gspread.authorize(creds)

# Setup
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Access Google Sheet
HSI = client.open_by_url("https://docs.google.com/spreadsheets/d/1D5V-B51Van2Vt1frrM8xkMyI9_3t-r26YFkuxv-B67M")
dfP = pd.DataFrame(HSI.worksheet('P8').get_all_records())

# Dataframe Setup
Perz = ['Index','Type 2','VI', 'ALL %',
        'Z1 %', 'Z1 A %', 'Z1 J %', 'Z1 O %', 'Z1 M %', 
        'Z2 %', 'Z2 A %', 'Z2 J %', 'Z2 O %', 'Z2 M %', 
        'Z3 %', 'Z3 A %', 'Z3 J %', 'Z3 O %', 'Z3 M %', 
        'Z4 %', 'Z4 A %', 'Z4 J %', 'Z4 O %', 'Z4 M %' 
        ]
dfP2 = dfP[Perz]

# Column mapping
rename_map = {
    'ALL %': 'ALL',
    'Z1 %': 'Zone 1', 'Z2 %': 'Zone 2', 'Z3 %': 'Zone 3', 'Z4 %': 'Zone 4', 
    'Z1 A %':'Zone 1 Age 15-19', 'Z2 A %':'Zone 2 Age 15-19', 
    'Z3 A %':'Zone 3 Age 15-19', 'Z4 A %':'Zone 4 Age 15-19', 
    'Z1 J %':'Zone 1 Age 20-29', 'Z2 J %':'Zone 2 Age 20-29', 
    'Z3 J %':'Zone 3 Age 20-29', 'Z4 J %':'Zone 4 Age 20-29', 
    'Z1 O %':'Zone 1 Age 30-59', 'Z2 O %':'Zone 2 Age 30-59', 
    'Z3 O %':'Zone 3 Age 30-59', 'Z4 O %':'Zone 4 Age 30-59', 
    'Z1 M %':'Zone 1 Age 60+', 'Z2 M %':'Zone 2 Age 60+', 
    'Z3 M %':'Zone 3 Age 60+', 'Z4 M %':'Zone 4 Age 60+'
}

dfP2 = dfP2.rename(columns=rename_map, errors='ignore')
dfP2 = dfP2.melt(id_vars=['Index','Type 2','VI'], var_name='Category', value_name='Value')
dfP2['Category'] = dfP2['Category'].astype('category')


# Dataset Configuration
datasetz = {}

for index_value in dfP2["Index"].unique():
    datasetz[index_value] = dfP2[dfP2["Index"] == index_value]

DZ1 = datasetz["D1"].reset_index().copy()
DZ2 = datasetz["D2"].reset_index().copy()
DZ3 = datasetz["D3"].reset_index().copy()
DZ4 = datasetz["D4"].reset_index().copy()
DZ5 = datasetz["D5"].reset_index().copy()
DZ6 = datasetz["D6"].reset_index().copy()
DZ7 = datasetz["D7"].reset_index().copy()
DZ8 = datasetz["D8"].reset_index().copy()
DZ9 = datasetz["D9"].reset_index().copy()

dimensionz = {
    'D1': DZ1,
    'D2': DZ2,
    'D3': DZ3,
    'D4': DZ4,
    'D5': DZ5,
    'D6': DZ6,
    'D7': DZ7,
    'D8': DZ8,
    'D9': DZ9
}

# Translated columns
for name, df in dimensionz.items():
    df['Category (EN)'] = df['Category']
    df['Category (ES)'] = df['Category'].map({
            'ALL': 'TODO',
            'Zone 1': 'Zona 1',
            'Zone 1 Male': 'Zona 1 Hombre','Zone 1 Female': 'Zona 1 Mujer',
            'Zone 1 Age 15-19': 'Zona 1 Edad 15-19','Zone 1 Age 20-29': 'Zona 1 Edad 20-29',
            'Zone 1 Age 30-59': 'Zona 1 Edad 30-59','Zone 1 Age 60+': 'Zona 1 Edad 60+',
            'Zone 2': 'Zona 2',
            'Zone 2 Male': 'Zona 2 Hombre','Zone 2 Female': 'Zona 2 Mujer',
            'Zone 2 Age 15-19': 'Zona 2 Edad 15-19','Zone 2 Age 20-29': 'Zona 2 Edad 20-29',
            'Zone 2 Age 30-59': 'Zona 2 Edad 30-59','Zone 2 Age 60+': 'Zona 2 Edad 60+',
            'Zone 3': 'Zona 3',
            'Zone 3 Male': 'Zona 3 Hombre','Zone 3 Female': 'Zona 3 Mujer',
            'Zone 3 Age 15-19': 'Zona 3 Edad 15-19','Zone 3 Age 20-29': 'Zona 3 Edad 20-29',
            'Zone 3 Age 30-59': 'Zona 3 Edad 30-59','Zone 3 Age 60+': 'Zona 3 Edad 60+',
            'Zone 4': 'Zona 4',
            'Zone 4 Male': 'Zona 4 Hombre','Zone 4 Female': 'Zona 4 Mujer',
            'Zone 4 Age 15-19': 'Zona 4 Edad 15-19','Zone 4 Age 20-29': 'Zona 4 Edad 20-29',
            'Zone 4 Age 30-59': 'Zona 4 Edad 30-59','Zone 4 Age 60+': 'Zona 4 Edad 60+'

    })

    df['VI (EN)'] = df['VI']
    df['VI (ES)'] = df['VI'].map({
        'Extreme': 'Extremo', 'High': 'Alto', 'Medium': 'Medio', 'Low': 'Bajo'
    })
    
translations = {
    '(EN)': {
        'title': 'Vulnerability Level per Dimension',
        'yaxis': 'Percentage',
        'dimensions': {'D1': 'Personal Security', 'D2': 'Economic Security', 'D3': 'Food Security', 
                     'D4': 'Health Security', 'D5': 'Political Security', 'D6': 'Community Security', 
                     'D7': 'Environmental Security', 'D8': 'Ontological Security', 'D9': 'Technological Security'},
        'components': {
            'Average': 'Average', 'Exposure': 'Exposure',
            'Protection': 'Protection', 'Rights': 'Rights'
        }
    },
    '(ES)': {
        'title': 'Nivel de vulnerabilidad por dimensión',
        'yaxis': 'Porcentaje',
        'dimensions': {'D1': 'Seguridad Personal', 'D2': 'Seguridad Económica', 'D3': 'Seguridad Alimentaria', 
                     'D4': 'Seguridad Sanitaria', 'D5': 'Seguridad Política', 'D6': 'Seguridad Comunitaria', 
                     'D7': 'Seguridad Ambiental', 'D8': 'Seguridad Ontológica', 'D9': 'Seguridad Tecnológica'},
        'components': {
            'Average': 'Promedio', 'Exposure': 'Exposición',
            'Protection': 'Protección', 'Rights': 'Derechos'
        }
    }
}

vi_order = ['Extreme', 'High', 'Medium', 'Low']
vi_colors = {'Extreme': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}

# DASH Bar Plot - By Zone & Age

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),

    html.Div([
        html.Label('Dimension:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dimension-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Component:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='component-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Language:', style={'fontFamily': 'Avenir Book'}),
        dcc.RadioItems(
        id='language-select',
        options=[
        {'label': 'English', 'value': '(EN)'},
        {'label': 'Español', 'value': '(ES)'}
        ],
        value='(EN)',
        labelStyle={
        'display': 'inline-block',
        'padding': '6px 12px',
        'margin': '4px',
        'borderRadius': '5px',
        'border': '1px solid #ccc',
        'backgroundColor': '#f8f8f8',
        'cursor': 'pointer',
        'fontFamily': 'Avenir Book'
        },
        style={'fontFamily': 'Avenir Book'}
        )
    ], style={'width': '60%', 'margin': 'auto', 'padding': '20px'}),

    dcc.Graph(id='bar-chart')
], style={'fontFamily': 'Avenir Book'})

@app.callback(
    Output('dimension-select', 'options'),
    Output('dimension-select', 'value'),
    Output('component-select', 'options'),
    Output('component-select', 'value'),
    Input('language-select', 'value')
)
def update_dropdowns(lang):
    dimension_options = [{'label': translations[lang]['dimensions'][k], 'value': k} for k in dimensionz.keys()]
    component_options = [{'label': translations[lang]['components'][k], 'value': k} for k in ['Average', 'Exposure', 'Protection', 'Rights']]
    return dimension_options, 'D1', component_options, 'Average'

@app.callback(
    Output('bar-chart', 'figure'),
    Output('chart-title', 'children'),
    Input('dimension-select', 'value'),
    Input('component-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(dimension_key, component_key, lang):
    df = dimensionz[dimension_key]
    df = df[df['Type 2'] == component_key].copy()
    df['Percentage'] = df['Value'] * 100
#    df['Percentage'] = pd.to_numeric(df['Percentage'], errors='coerce')

    # Using translated columns
    x_column = 'Category ' + lang
    color_column = 'VI ' + lang

    # Building legend order and color map
    vi_labels = [df[f'VI {lang}'][df['VI'] == vi].iloc[0] for vi in vi_order]
    color_map = {df[f'VI {lang}'][df['VI'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

    fig = px.bar(
        df,
        x=x_column,
        y='Percentage',
        color=color_column,
        category_orders={color_column: vi_labels},
        color_discrete_map=color_map,
            text=df['Percentage'].round(1).astype(str) + '%'
    )

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title=translations[lang]['yaxis'],
            range=[0, 100],
            ticksuffix='%'
        ),
        title=dict(
            text=f"{translations[lang]['title']} – {translations[lang]['components'][component_key]} ({translations[lang]['dimensions'][dimension_key]})",
            x=0.5
        ),
        font=dict(
        family="Avenir Book",
        size=14,
        color='black'
        ),
        legend_title_text='',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig, translations[lang]['title']

if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')
