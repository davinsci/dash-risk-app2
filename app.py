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
    'Z1 Ml %':'Zone 1 Male', 'Z2 Ml %':'Zone 2 Male', 'Z3 Ml %':'Zone 3 Male', 'Z4 Ml %':'Zone 4 Male', 
    'Z1 Fl %':'Zone 1 Female', 'Z2 Fl %':'Zone 2 Female', 'Z3 Fl %':'Zone 3 Female', 'Z4 Fl %':'Zone 4 Female',
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
    df['Category (EN)'] = df['Category'].map({
            'ALL': 'All',
            'Zone 1': 'Northwest',
            'Zone 1 Male': 'Northwest Male','Zone 1 Female': 'Northwest Female',
            'Zone 1 Age 15-19': 'Northwest Age 15-19','Zone 1 Age 20-29': 'Northwest Age 20-29',
            'Zone 1 Age 30-59': 'Northwest Age 30-59','Zone 1 Age 60+': 'Northwest Age 60+',
            'Zone 2': 'Northeast',
            'Zone 2 Male': 'Northeast Male','Zone 2 Female': 'Northeast Female',
            'Zone 2 Age 15-19': 'Northeast Age 15-19','Zone 2 Age 20-29': 'Northeast Age 20-29',
            'Zone 2 Age 30-59': 'Northeast Age 30-59','Zone 2 Age 60+': 'Northeast Age 60+',
            'Zone 3': 'Southwest',
            'Zone 3 Male': 'Southwest Male','Zone 3 Female': 'Southwest Female',
            'Zone 3 Age 15-19': 'Southwest Age 15-19','Zone 3 Age 20-29': 'Southwest Age 20-29',
            'Zone 3 Age 30-59': 'Southwest Age 30-59','Zone 3 Age 60+': 'Southwest Age 60+',
            'Zone 4': 'Southeast',
            'Zone 4 Male': 'Southeast Male','Zone 4 Female': 'Southeast Female',
            'Zone 4 Age 15-19': 'Southeast Age 15-19','Zone 4 Age 20-29': 'Southeast Age 20-29',
            'Zone 4 Age 30-59': 'Southeast Age 30-59','Zone 4 Age 60+': 'Southeast Age 60+'
    })
    df['Category (ES)'] = df['Category'].map({
            'ALL': 'Todo',
            'Zone 1': 'Norponiente',
            'Zone 1 Male': 'Norponiente Hombre','Zone 1 Female': 'Norponiente Mujer',
            'Zone 1 Age 15-19': 'Norponiente Edad 15-19','Zone 1 Age 20-29': 'Norponiente Edad 20-29',
            'Zone 1 Age 30-59': 'Norponiente Edad 30-59','Zone 1 Age 60+': 'Norponiente Edad 60+',
            'Zone 2': 'Nororiente',
            'Zone 2 Male': 'Nororiente Hombre','Zone 2 Female': 'Nororiente Mujer',
            'Zone 2 Age 15-19': 'Nororiente Edad 15-19','Zone 2 Age 20-29': 'Nororiente Edad 20-29',
            'Zone 2 Age 30-59': 'Nororiente Edad 30-59','Zone 2 Age 60+': 'Nororiente Edad 60+',
            'Zone 3': 'Surponiente',
            'Zone 3 Male': 'Surponiente Hombre','Zone 3 Female': 'Surponiente Mujer',
            'Zone 3 Age 15-19': 'Surponiente Edad 15-19','Zone 3 Age 20-29': 'Surponiente Edad 20-29',
            'Zone 3 Age 30-59': 'Surponiente Edad 30-59','Zone 3 Age 60+': 'Surponiente Edad 60+',
            'Zone 4': 'Suroriente',
            'Zone 4 Male': 'Suroriente Hombre','Zone 4 Female': 'Suroriente Mujer',
            'Zone 4 Age 15-19': 'Suroriente Edad 15-19','Zone 4 Age 20-29': 'Suroriente Edad 20-29',
            'Zone 4 Age 30-59': 'Suroriente Edad 30-59','Zone 4 Age 60+': 'Suroriente Edad 60+'
    })

    df['VI (EN)'] = df['VI']
    df['VI (ES)'] = df['VI'].map({
        'Extreme': 'Extrema', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Baja'
    })
    
    df['VI_desc (EN)'] = df['VI (EN)'].map({
        'Extreme': 'Exposure to a high number of threats and lack of means of protection against them.',
        'High': 'Exposure to multiple risk factors and limited access to protection mechanisms.',
        'Medium': "Some threat factors present, but partial access to means to mitigate them.",
        'Low': 'Certain risks may exist, but threats are neither imminent nor severe.'
    })
    
    df['VI_desc (ES)'] = df['VI (EN)'].map({
        'Extreme': 'Existe gran cantidad de amenazas y no se cuenta con medios efectivos para protegersede estas.',
        'High': 'Exposición a varios factores de riesgo y acceso limitado a mecanismos de protección.',
        'Medium': 'Existen factores de amenaza y hay acceso parcial a medios para mitigar dichas amenazas.',
        'Low': 'Existen ciertos riesgos, pero las amenazas no son inminentes o severas.'
    })
    
translations = {
    '(EN)': {
        'title': 'Vulnerability Level per Dimension',
        'yaxis': 'Percentage',
        'dimensions': {'D1': 'Personal Security', 'D2': 'Economic Security', 'D3': 'Food Security', 
                     'D4': 'Health Security', 'D5': 'Political Security', 'D6': 'Community Security', 
                     'D7': 'Environmental Security', 'D8': 'Ontological Security', 'D9': 'Technological Security'},
        'components': {
            'Average': 'Level of Vulnerability', 'Exposure': 'Level of Exposure to Threats',
            'Protection': 'Level of Access to Protection Mechanisms', 'Rights': 'Level of Freedom to Exercise Rights'
        }
    },
    '(ES)': {
        'title': 'Nivel de vulnerabilidad por dimensión',
        'yaxis': 'Porcentaje',
        'dimensions': {'D1': 'Seguridad Personal', 'D2': 'Seguridad Económica', 'D3': 'Seguridad Alimentaria', 
                     'D4': 'Seguridad Sanitaria', 'D5': 'Seguridad Política', 'D6': 'Seguridad Comunitaria', 
                     'D7': 'Seguridad Ambiental', 'D8': 'Seguridad Ontológica', 'D9': 'Seguridad Tecnológica'},
        'components': {
            'Average': 'Nivel de Vulnerabilidad', 'Exposure': 'Nivel de Exposición a Amenazas',
            'Protection': 'Nivel de Acceso a Mecanismos de Protección', 'Rights': 'Nivel de Libertad para Ejercer Derechos'
        }
    }
}

vi_order = ['Extreme', 'High', 'Medium', 'Low']
vi_colors = {'Extreme': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}

intro_descriptions = {
    '(EN)': "The Glocal Human Security Index measures individuals' levels of vulnerability\
        across nine dimensions by integrating the scores of three components: \
        Exposure to Threats; Access to Protection Mechanisms; and Freedom to Exercise Rights.",
    '(ES)': "El Índice Glocal de Seguridad Humana mide el nivel de vulnerabilidad \
        de las personas en nueve dimensiones, integrando los puntajes de tres componentes:\
        Exposición a Amenazas; Acceso a Mecanismos de Protección; y Libertad para Ejercer Derechos."
}

component_descriptions = {
    '(EN)': {
        'Average': 'Weighted average of scores for exposure to threats, access to protection, and freedom to exercise rights.',
        'Exposure': 'Exposure to threats: How exposed was the person to factors and situations that endangered their life, livelihood, or rights?',
        'Protection': 'Access to protection mechanisms: How accessible and effective were the resources, services, or support systems to protect against or recover from those threats?',
        'Rights': 'Freedom to exercise rights: To what extent was the person able to fully and freely exercise their rights without restrictions?'
    },
    '(ES)': {
        'Average': 'Promedio ponderado de las puntuaciones sobre la exposición a amenazas, el acceso a protección y la libertad para ejercer derechos.',
        'Exposure': 'Exposición a amenazas: ¿Qué tan expuesta estuvo la persona a situaciones que ponen en riesgo su vida, sustento o derechos?',
        'Protection': 'Acceso a mecanismos de protección: ¿Qué tan accesibles y eficaces fueron los recursos, servicios o apoyos para protegerse o recuperarse frente a esas amenazas?',
        'Rights': 'Libertad para ejercer derechos: ¿Qué tanto margen tuvo la persona para ejercer sus derechos de manera plena y sin restricciones?'
    }
}

dimension_descriptions = {
    '(EN)': {
        'D1': 'Protection from harm caused by any form of violence.', 
        'D2': 'Protection of livelihoods.', 
        'D3': 'Protection of reliable access to food and adequate nutrition.', 
        'D4': 'Protection of physical and mental health and access to quality medical services.', 
        'D5': 'Protection of fundamental rights, including the right to participate in public affairs.', 
        'D6': 'Protection of peaceful coexistence among community members and their ability to function as support systems.', 
        'D7': 'Protection from disasters, environmental threats, and hazardous conditions in the built environment.', 
        'D8': "Protection of dignity and a person's sense of social relevance.", 
        'D9': 'Protection from risks associated with technology use and access to its benefits.'
    },
    '(ES)': {
        'D1': 'Protección frente a daños causados por cualquier forma de violencia.', 
        'D2': 'Protección de los medios de vida', 
        'D3': 'Protección del acceso confiable a alimentos y a una nutrición adecuada.', 
        'D4': 'Protección de la salud mental y física y del acceso a servicios médicos de calidad.', 
        'D5': 'Protección de los derechos fundamentales, incluido el derecho a participar en asuntos públicos.', 
        'D6': 'Protección de la convivencia pacífica entre miembros de una comunidad y su capacidad para funcionar como sistemas de apoyo.', 
        'D7': 'Protección frente a desastres, amenazas ambientales y condiciones peligrosas del entorno construido.', 
        'D8': 'Protección de la dignidad y el sentido de relevancia social de las personas.', 
        'D9': 'Protección frente a los riesgos derivados del uso de tecnologías y acceso a sus beneficios.'
    }
}

# DASH Bar Plot - By Zone & Age

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),
    
    html.Div(id='intro-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),

    html.Div([
        html.Label('Dimension:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dimension-select', style={'fontFamily': 'Avenir Book'}),
        
        html.Div(id='dimension-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),

        html.Label('Component:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='component-select', style={'fontFamily': 'Avenir Book'}),

        html.Div(id='component-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),
        
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
    Output('dimension-description', 'children'),
    Output('component-description', 'children'),
    Output('intro-description', 'children'),
    Input('dimension-select', 'value'),
    Input('component-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(dimension_key, component_key, lang):
    df = dimensionz[dimension_key]
    df = df[df['Type 2'] == component_key].copy()
    df['Percentage'] = df['Value'] * 100
#    df['Percentage'] = pd.to_numeric(df['Percentage'], errors='coerce')
    df['VI_desc'] = df[f'VI_desc {lang}']  # Just pick the right column
    df['VI_hover'] = df[f'VI {lang}'] + '<br>' + df['VI_desc']

    # Use translated columns
    x_column = 'Category ' + lang
    color_column = 'VI ' + lang

    # Legend and color map
    vi_labels = [df[f'VI {lang}'][df['VI'] == vi].iloc[0] for vi in vi_order]
    color_map = {df[f'VI {lang}'][df['VI'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

    fig = px.bar(
        df,
        x=x_column,
        y='Percentage',
        color=color_column,
        category_orders={color_column: vi_labels},
        color_discrete_map=color_map,
            text=df['Percentage'].round(1).astype(str) + '%',
        custom_data=['VI_hover'],
        hover_data=[]
    )

    fig.update_traces(
        hovertemplate='<b>%{x}<br>%{y}</b><br>%{customdata[0]}<extra></extra>')
    
    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title=translations[lang]['yaxis'],
            range=[0, 100],
            ticksuffix='%'
        ),
        title=dict(
            text=f"{translations[lang]['components'][component_key]} ({translations[lang]['dimensions'][dimension_key]})",
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

    description = dimension_descriptions[lang][dimension_key]
    cescription = component_descriptions[lang][component_key]
    intro_text = intro_descriptions[lang]

    return fig, translations[lang], description, cescription, intro_text

if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')
