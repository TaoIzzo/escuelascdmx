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

numalcaldiaprivda=pd.DataFrame(escuelas_privadas["alcaldia"].value_counts())
numalcaldiaprivda=numalcaldiaprivda.reset_index()
numalcaldiaprivda=numalcaldiaprivda.rename(columns={"index" : "grado","alcaldia":"escuelas"})

grados_privados = escuelas_privadas[["alcaldia","nivel"]]
grados_privados
dummies = pd.get_dummies(grados_privados.nivel)
mergedprivados = pd.concat([grados_privados, dummies], axis='columns')
mergedprivados.drop(['nivel'], axis='columns',inplace=True)
merged2privados = mergedprivados.groupby('alcaldia').sum()
merged2privados=merged2privados.reset_index()

PreescolarInicial = go.Bar(y = merged2privados["Preescolar - Inicial *"], x = merged2privados["alcaldia"], name = "Preescolar - Inicial", marker = {"color" : "#00ff00"})
INICIAL = go.Bar(y = merged2privados["INICIAL"], x = merged2privados["alcaldia"], name = "INICIAL", marker = {"color" : "#00ff80"})
Preescolar = go.Bar(y = merged2privados["Preescolar"], x = merged2privados["alcaldia"], name = "Preescolar", marker = {"color" : "#00ffff"})
Primaria = go.Bar(y = merged2privados["Primaria"], x = merged2privados["alcaldia"], name = "Primaria", marker = {"color" : "#0080ff"})
Secundaria = go.Bar(y = merged2privados["Secundaria"], x = merged2privados["alcaldia"], name = "Secundaria", marker = {"color" : "#0000ff"})
EspecialCAM = go.Bar(y = merged2privados["Especial - CAM"], x = merged2privados["alcaldia"], name = "Especial - CAM", marker = {"color" : "#ff00ff"})
Adultos = go.Bar(y = merged2privados["Adultos"], x = merged2privados["alcaldia"], name = "Adultos", marker = {"color" : "#ff0080"})

layoutprivada = go.Layout(title = "Escuelas Privadas", 
                   xaxis =dict(title="zona"), 
                   yaxis= dict(title="Cantidad"),
                   barmode="stack")

dataprivada=[PreescolarInicial,INICIAL,Preescolar,Primaria,Secundaria,EspecialCAM,Adultos]
figalcaldiasprivada = go.Figure(data = dataprivada, layout = layoutprivada)



app = dash.Dash(__name__,
                title ='Escuelas Privadas')
app.title = 'Escuelas Privadas'
variablesprivadas = escuelas_privadas.alcaldia.unique()

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
                    figure=px.pie(numalcaldiaprivda,values="escuelas",names="grado",title="escuelas en alcaldias"))
            ],style={'width': '43%', 'float': 'left', 'display': 'inline-block'}),    
]),

        html.Div([
            dcc.Graph(id='barplot_nivelgeneral', figure=figalcaldiasprivada)
            ],style={'width': '43%', 'float': 'right', 'display': 'inline-block'}),


        html.Div([
                dcc.Dropdown(
                    id='alcaldia',
                    options=[{'label': i, 'value': i} for i in variablesprivadas],
                    value='alcaldia'
                    )
                    ],style={'width': '48%', 'display': 'inline-block'}),
        
        
        html.Div(id='display-selected-valuesprivada'),
        
        html.Div([
            dcc.Graph(id='gradobarplotprivada')
            ],),
        
        html.Div([
                html.P("El siguiente mapa corresponde a las escuelas publicas ubicadas en la CDMX, y del lado superior drecho estan los grados adademicos con los que cuenta este sector",
                style = {"textAlign":"left", 
                    "fontSize":20}),
            html.Iframe(
                id="map_privadas",
                src="assets/map_privada.html",
                style={"height": "800px", "width": "90%"},
            ),
        ]),
           
        
    ],id="header", className = "row flex-display", style = {"margin-bottom":"25px" })
], id = "maincontainer", style = {"display" : "flex", "flex-direction" : "column"})