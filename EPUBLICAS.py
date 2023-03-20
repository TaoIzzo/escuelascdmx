import pandas as pd
import plotly.graph_objects as go
import dash 
from dash.dependencies import Input,Output
from dash import html as html
from dash import dcc as dcc
import plotly.express as px
import EPRIVADAS
import EPUBLICAS
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from app import app
from app import server

escuelas_publicas= pd.read_excel("Escuelas Publicas_limpias.xlsx")
escuelas_privadas= pd.read_excel("escuelas.xlsx")
poblacion = pd.read_excel("Poblacion.xlsx")
numalcaldia=pd.DataFrame(escuelas_publicas["alcaldia"].value_counts())
numalcaldia=numalcaldia.rename(columns={"Geography" : "alcaldia"})

grados_publicos = escuelas_publicas[["alcaldia","nivel"]]
grados_publicos
dummies = pd.get_dummies(grados_publicos.nivel)
merged = pd.concat([grados_publicos, dummies], axis='columns')
merged.drop(['nivel'], axis='columns',inplace=True)
merged
merged2 = merged.groupby('alcaldia').sum()
merged2=merged2.reset_index()

INTERVENCION = go.Bar(y = merged2["INTERVENCION"], x = merged2["alcaldia"], name = "INTERVENCION", marker = {"color" : "#ff0000"})
BRINDAR = go.Bar(y = merged2["BRINDAR"], x = merged2["alcaldia"], name = "BRINDAR", marker = {"color" : "#ff8000"})
LACTANTE = go.Bar(y = merged2["LACTANTE,"], x = merged2["alcaldia"], name = "LACTANTE", marker = {"color" : "#ffff00"})
ATENDER = go.Bar(y = merged2["ATENDER"], x = merged2["alcaldia"], name = "ATENDER", marker = {"color" : "#80ff00"})
SUPERVISAR = go.Bar(y = merged2["SUPERVISAR"], x = merged2["alcaldia"], name = "SUPERVISAR", marker = {"color" : "#00ff00"})
CAPACITACION = go.Bar(y = merged2["CAPACITACION"], x = merged2["alcaldia"], name = "CAPACITACION", marker = {"color" : "#00ff80"})
PREESCOLAR = go.Bar(y = merged2["PREESCOLAR"], x = merged2["alcaldia"], name = "PREESCOLAR", marker = {"color" : "#00ffff"})

PRIMARIA = go.Bar(y = merged2["PRIMARIA"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#0080ff"})
SECUNDARIA = go.Bar(y = merged2["SECUNDARIA"], x = merged2["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#0000ff"})
SECUNDARIA_TECNICA = go.Bar(y = merged2["SECUNDARIA TECNICA"], x = merged2["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#8000ff"})

TELESECUNDARIA = go.Bar(y = merged2["TELESECUNDARIA"], x = merged2["alcaldia"], name = "TELESECUNDARIA", marker = {"color" : "#ff00ff"})
LICENCIATURA = go.Bar(y = merged2["LICENCIATURA"], x = merged2["alcaldia"], name = "LICENCIATURA", marker = {"color" : "#ff0080"})

layout = go.Layout(title = "Escuelas Publicas", 
                   xaxis =dict(title="zona"), 
                   yaxis= dict(title="Cantidad"),
                   barmode="stack")
data=[INTERVENCION,BRINDAR,LACTANTE,ATENDER,SUPERVISAR,CAPACITACION,PREESCOLAR,PRIMARIA,SECUNDARIA,SECUNDARIA_TECNICA,TELESECUNDARIA,LICENCIATURA]
figalcaldias = go.Figure(data = data, layout = layout)





app = dash.Dash(__name__,
                title ='Escuelas Publicas')
app.title = 'Escuelas Publicas'
variables = escuelas_publicas.alcaldia.unique()

layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=("/assets/iebs-logo.png"),
                    id="ieb-image",
                    style = {"height" : "120px",
                             "width":"240px",
                             "margin bottom" : "25px"})
            
        ], className = "one-third column"
),
        
        html.Div([
            html.Div([
                html.H1("Elige tu mejor escuela",
                       style = {"textAlign":"center"}),
                html.P("Gracias a la base de datos abierta de la SECRETARIA DE EDCUACION PUBLICA (SEP), ponemos a tu disposicion el muestreo de sus escuelas, asi como multiples filtros con la finalidad de que puedas elegir la mejor escuela para ti",
                       style = {"textAlign":"center", 
                                "fontSize":20})
            ])
            
            
        ], className="one-half column", id="title"
),
  
        html.Div([
            html.Div([
                dcc.Link('Escuelas Publicas', href='/EPUBLICAS', style = {"margin-bottom": "20px", 'padding': '25px', 'fontWeight': 'bold', 'color': 'blue'}),
                dcc.Link('Escuelas Privadas', href='/EPRIVADAS', style = {"margin-bottom": "20px", 'padding': '25px', 'fontWeight': 'bold', 'color': 'blue'}),
                ], className = "create_container3 ten columns", id = "title1RegionRegion"),

        ], id = "header1Region", className = "row flex-display"),  
  
        
        html.Div([
            html.Div([
            dcc.Graph(id='lineplot',
                    figure=px.pie(numalcaldia,values="alcaldia",names=numalcaldia.index,title="escuelas en alcaldias"))
            ],style={'width': '43%', 'float': 'left', 'display': 'inline-block'}),    
]),

        html.Div([
            dcc.Graph(id='barplot_nivelgeneral', figure=figalcaldias)
            ],style={'width': '43%', 'float': 'right', 'display': 'inline-block'}),


        html.Div([
                dcc.Dropdown(
                    id='alcaldia',
                    options=[{'label': i, 'value': i} for i in variables],
                    value='Alcaldia'
                    )
                    ],style={'width': '48%', 'display': 'inline-block'}),
        
        
        html.Div(id='display-selected-values'),
        
        html.Div([
            dcc.Graph(id='gradobarplot')
            ],),
        
        html.Div([
                html.P("El siguiente mapa corresponde a las escuelas publicas ubicadas en la CDMX, y del lado superior drecho estan los grados adademicos con los que cuenta este sector",
                style = {"textAlign":"left", 
                    "fontSize":20}),
            html.Iframe(
                id="map_publicas",
                src="assets/map_publica.html",
                style={"height": "800px", "width": "90%"},
            ),
        ]),
           
        
    ],id="header", className = "row flex-display", style = {"margin-bottom":"25px" })
], id = "maincontainer", style = {"display" : "flex", "flex-direction" : "column"})




