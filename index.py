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

INTERVENCION = go.Bar(y = merged2["INTERVENCION"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#ff0000"})
BRINDAR = go.Bar(y = merged2["BRINDAR"], x = merged2["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#ff8000"})
LACTANTE = go.Bar(y = merged2["LACTANTE,"], x = merged2["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#ffff00"})
ATENDER = go.Bar(y = merged2["ATENDER"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#80ff00"})
SUPERVISAR = go.Bar(y = merged2["SUPERVISAR"], x = merged2["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#00ff00"})
CAPACITACION = go.Bar(y = merged2["CAPACITACION"], x = merged2["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#00ff80"})
PREESCOLAR = go.Bar(y = merged2["PREESCOLAR"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#00ffff"})

PRIMARIA = go.Bar(y = merged2["PRIMARIA"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#0080ff"})
SECUNDARIA = go.Bar(y = merged2["SECUNDARIA"], x = merged2["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#0000ff"})
SECUNDARIA_TECNICA = go.Bar(y = merged2["SECUNDARIA TECNICA"], x = merged2["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#8000ff"})

TELESECUNDARIA = go.Bar(y = merged2["TELESECUNDARIA"], x = merged2["alcaldia"], name = "PRIMARIA", marker = {"color" : "#ff00ff"})
LICENCIATURA = go.Bar(y = merged2["LICENCIATURA"], x = merged2["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#ff0080"})


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
# SECUNDARIA_TECNICA = go.Bar(y = merged2privados["SECUNDARIA TECNICA"], x = merged2privados["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#8000ff"})
EspecialCAM = go.Bar(y = merged2privados["Especial - CAM"], x = merged2privados["alcaldia"], name = "Especial - CAM", marker = {"color" : "#ff00ff"})
Adultos = go.Bar(y = merged2privados["Adultos"], x = merged2privados["alcaldia"], name = "Adultos", marker = {"color" : "#ff0080"})

layoutprivada = go.Layout(title = "Escuelas Privadas", 
                   xaxis =dict(title="zona"), 
                   yaxis= dict(title="Cantidad"),
                   barmode="stack")

dataprivada=[PreescolarInicial,INICIAL,Preescolar,Primaria,Secundaria,EspecialCAM,Adultos]
figalcaldiasprivada = go.Figure(data = dataprivada, layout = layoutprivada)


layout = go.Layout(title = "Escuelas Publicas", 
                   xaxis =dict(title="zona"), 
                   yaxis= dict(title="Cantidad"),
                   barmode="stack")
data=[INTERVENCION,BRINDAR,LACTANTE,ATENDER,SUPERVISAR,CAPACITACION,PREESCOLAR,PRIMARIA,SECUNDARIA,SECUNDARIA_TECNICA,TELESECUNDARIA,LICENCIATURA]
figalcaldias = go.Figure(data = data, layout = layout)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Escuelas Publicas', href='/EPUBLICAS'),
        dcc.Link('Escuelas Privadas', href='/EPRIVADAS'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/EPUBLICAS':
        return EPUBLICAS.layout
    elif pathname == '/EPRIVADAS':
        return EPRIVADAS.layout
    else:
        return EPUBLICAS.layout

@app.callback(
    Output('display-selected-values', 'children'),
    Input('alcaldia', 'value'),)
#     Input('cities-radio', 'value')
def set_display_children(alcaldia):
    return (u"A seleccionado {} con {} escuelas publicas entre ellas: ".format(
        alcaldia,escuelas_publicas[escuelas_publicas["alcaldia"]==alcaldia].nombre.count() ),
            html.Br(),
            u"con  {} de grado INTERVENCION ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="INTERVENCION")].nombre.count()),
            html.Br(),
            u"con  {} de grado BRINDAR  ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="BRINDAR")].nombre.count()),
            html.Br(),
            u"con  {} de grado LACTANTE ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="LACTANTE")].nombre.count()),
            html.Br(),
            u"con  {} de grado ATENDER ".format(
                escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="ATENDER")].nombre.count()),
            html.Br(),
            u"con  {} de grado SUPERVISAR ".format(
                escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="SUPERVISAR")].nombre.count()),
            html.Br(),
            u"con{} de grado CAPACITACION ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="CAPACITACION")].nombre.count()),
            html.Br(),
            u"con  {} de grado PREESCOLAR ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="PREESCOLAR")].nombre.count()),
            html.Br(),
            u"con  {} de grado PRIMARIA ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="PRIMARIA")].nombre.count()),
            html.Br(),
            u"con  {} de grado SECUNDARIA ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="SECUNDARIA")].nombre.count()),
            html.Br(),
            u"con  {} de grado SECUNDARIA TECNICA ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="SECUNDARIA TECNICA")].nombre.count()),
            html.Br(),
            u"con  {} de grado TELESECUNDARIA  ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="TELESECUNDARIA")].nombre.count()),
            html.Br(),
            u"con  {} de grado LICENCIATURA ".format(
        escuelas_publicas[(escuelas_publicas["alcaldia"]==alcaldia) & (escuelas_publicas["nivel"]=="LICENCIATURA")].nombre.count()),
           )

@app.callback(
    Output("gradobarplot", "figure"),
    [Input("alcaldia","value")],
)
def actualizar(alcaldia):
    merged3=merged2[merged2["alcaldia"]==alcaldia]
    INTERVENCION = go.Bar(y = merged3["INTERVENCION"], x = merged3["alcaldia"], name = "PRIMARIA", marker = {"color" : "#ff0000"})
    BRINDAR = go.Bar(y = merged3["BRINDAR"], x = merged3["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#ff8000"})
    LACTANTE = go.Bar(y = merged3["LACTANTE,"], x = merged3["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#ffff00"})
    ATENDER = go.Bar(y = merged3["ATENDER"], x = merged3["alcaldia"], name = "PRIMARIA", marker = {"color" : "#80ff00"})
    SUPERVISAR = go.Bar(y = merged3["SUPERVISAR"], x = merged3["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#00ff00"})
    CAPACITACION = go.Bar(y = merged3["CAPACITACION"], x = merged3["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#00ff80"})
    PREESCOLAR = go.Bar(y = merged3["PREESCOLAR"], x = merged3["alcaldia"], name = "PRIMARIA", marker = {"color" : "#00ffff"})
    PRIMARIA = go.Bar(y = merged3["PRIMARIA"], x = merged3["alcaldia"], name = "PRIMARIA", marker = {"color" : "#0080ff"})
    SECUNDARIA = go.Bar(y = merged3["SECUNDARIA"], x = merged3["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#0000ff"})
    SECUNDARIA_TECNICA = go.Bar(y = merged3["SECUNDARIA TECNICA"], x = merged3["alcaldia"], name = "SECUNDARIA TECNICA", marker = {"color" : "#8000ff"})
    TELESECUNDARIA = go.Bar(y = merged3["TELESECUNDARIA"], x = merged3["alcaldia"], name = "PRIMARIA", marker = {"color" : "#ff00ff"})
    LICENCIATURA = go.Bar(y = merged3["LICENCIATURA"], x = merged3["alcaldia"], name = "SECUNDARIA", marker = {"color" : "#ff0080"})
    layout = go.Layout(title = "Escuelas Publicas", 
                       xaxis =dict(title="zona"), 
                       yaxis= dict(title="Cantidad"),
                      )
    data=[INTERVENCION,BRINDAR,LACTANTE,ATENDER,SUPERVISAR,CAPACITACION,PREESCOLAR,PRIMARIA,SECUNDARIA,SECUNDARIA_TECNICA,TELESECUNDARIA,LICENCIATURA]
    figalcaldias = go.Figure(data = data, layout = layout)
    return figalcaldias

@app.callback(
    Output("map_publicas", "src"), Input("alcaldia", "value"), prevent_initial_call=True
)
def update_output_div(input_value):
    return f"assets/publicas/{input_value}.html"

@app.callback(
    Output("map_privadas", "src"), Input("alcaldia", "value"), prevent_initial_call=True
)
def update_output_div(input_value):
    return f"assets/privadas/{input_value}.html"

@app.callback(
    Output('display-selected-valuesprivada', 'children'),
    Input('alcaldia', 'value'),)
#     Input('cities-radio', 'value')
def set_display_children(alcaldia):
    return (u"A seleccionado {} con {} escuelas publicas entre ellas: ".format(
        alcaldia,escuelas_privadas[escuelas_privadas["alcaldia"]==alcaldia].nombre.count() ),
            html.Br(),
            u"con  {} de grado Preescolar-Inicial ".format(
        escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Preescolar - Inicial *")].nombre.count()),
            html.Br(),
            u"con  {} de grado INICIAL  ".format(
        escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="INICIAL")].nombre.count()),
            html.Br(),
            u"con  {} de grado Preescolar ".format(
        escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Preescolar")].nombre.count()),
            html.Br(),
            u"con  {} de grado Primaria ".format(
                escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Primaria")].nombre.count()),
            html.Br(),
            u"con  {} de grado Secundaria ".format(
                escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Secundaria")].nombre.count()),
            html.Br(),
            u"con{} de grado EspecialCAM ".format(
        escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Especial - CAM")].nombre.count()),
            html.Br(),
            u"con  {} de grado Adultos ".format(
        escuelas_privadas[(escuelas_privadas["alcaldia"]==alcaldia) & (escuelas_privadas["nivel"]=="Adultos")].nombre.count()),
            html.Br(),
           )

@app.callback(
    Output("gradobarplotprivada", "figure"),
    [Input("alcaldia","value")],
)
def actualizar(alcaldia):
    merged3privadas=merged2privados[merged2privados["alcaldia"]==alcaldia]
    PreescolarInicial = go.Bar(y = merged3privadas["Preescolar - Inicial *"], x = merged3privadas["alcaldia"], name = "Preescolar - Inicial", marker = {"color" : "#00ff00"})
    INICIAL = go.Bar(y = merged3privadas["INICIAL"], x = merged3privadas["alcaldia"], name = "INICIAL", marker = {"color" : "#00ff80"})
    Preescolar = go.Bar(y = merged3privadas["Preescolar"], x = merged3privadas["alcaldia"], name = "Preescolar", marker = {"color" : "#00ffff"})
    Primaria = go.Bar(y = merged3privadas["Primaria"], x = merged3privadas["alcaldia"], name = "Primaria", marker = {"color" : "#0080ff"})
    Secundaria = go.Bar(y = merged3privadas["Secundaria"], x = merged3privadas["alcaldia"], name = "Secundaria", marker = {"color" : "#0000ff"})
    EspecialCAM = go.Bar(y = merged3privadas["Especial - CAM"], x = merged3privadas["alcaldia"], name = "Especial - CAM", marker = {"color" : "#ff00ff"})
    Adultos = go.Bar(y = merged3privadas["Adultos"], x = merged3privadas["alcaldia"], name = "Adultos", marker = {"color" : "#ff0080"})
    layoutprivadas = go.Layout(title = "Escuelas Privadas", 
                       xaxis =dict(title="zona"), 
                       yaxis= dict(title="Cantidad"),
                      )
    dataprivada=[PreescolarInicial,INICIAL,Preescolar,Primaria,Secundaria,EspecialCAM,Adultos]
    figalcaldias = go.Figure(data = dataprivada, layout = layoutprivadas)
    return figalcaldias



if __name__ =="__main__":
    app.run_server(debug=False)