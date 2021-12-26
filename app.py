import dash
from dash import dcc
from dash import html
from dash.html.Br import Br
import plotly.express as px
import pandas as pd
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np


df=pd.read_excel("data/final.xlsx")
df0=pd.read_excel("data/df0.xlsx")
df1=df[["Continent","Valeur DHS 2018","Valeur DHS 2019","Valeur DHS 2020","Valeur DHS 2021","Libellé du flux"]]
df2=pd.read_excel("data/df2.xlsx")
df3=pd.read_excel("data/df3.xlsx")
df4=pd.read_excel("data/df4.xlsx")
df5=pd.read_excel("data/df5.xlsx")
df6=pd.read_excel("data/df6.xlsx")

all_pays=df3["Libellé du pays"].unique()

app = dash.Dash(__name__)

colors = {'background': ' #00204E','text': '#FFFFFF'}


fig = px.bar(df0, x="année", y="valeur en DHS", color="Libellé du flux", barmode="group",color_discrete_sequence=['indianred','#03B0BD','#330C73','#EB89B5','#117270','#533847'],width=10)
fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])

fig2 = px.scatter(df2, x="Année", y="Valeur DHS",color="Continent", hover_name="Libellé du flux",size_max=400)
fig2.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])

fig5= px.scatter_geo(df4, locations="iso_alpha", color="Continent",hover_name="Libellé du flux", size="Valeur DHS",animation_frame="Année",projection="natural earth")
fig5.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])

fig6 = px.bar(df5, x="Année", y="Valeur DHS ", color="Libellé du groupement d'utilisation", barmode="group",hover_name="Libellé du flux",color_discrete_sequence=['lightcyan','cyan','royalblue','darkblue','#0D5283','indianred','#03B0BD','#330C73','#EB89B5'])
fig6.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])

fig7= px.sunburst(df6, path=['Libellé du flux','Libellé de la section CTCI'], values='Valeur DHS',color_discrete_map={'Exportations FAB':'lightcyan','Importations CAF':'cyan','Importations en admission temporaire pour perfectionnement actif  avec paiement':'royalblue','Importations en admission temporaire pour perfectionnement actif  sans paiement':'darkblue',"Réexportations en suite d'admission temporaire pour perfectionnement actif avec paiement":'#0D5283'})
fig7.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])


app.layout = html.Div(
    
    id="main-page",
    children=[
        html.Div(
            id="header",
            className="banner row",
            children=[
                # Logo and Title
                html.Div(
                    className="banner-logo-and-title",
                    children=[
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="logo",
                        ),
                         html.H1(
                            "Commerce Extérieur du Maroc"
                        )
                    ],
                ),
            ],
        ),
    html.Br(),



   # *********************   GRAPHE1   ********************************
    html.Div(
        [
        html.Strong("Libellé du flux & Valeur DHS", className="subtitle padded",),
        dcc.Graph(id='example-graph',figure=fig),
        ],
        className="graphe",
        ),
    html.Br(),
    html.Br(),


   # *********************   GRAPHE2   ********************************
     html.Div(
        [ html.Strong("Valeur en DHS de chaque Libellé du flux (2018/19/20/21) ", className="subtitle padded",),
        html.P("Libellé:"),
        dcc.Dropdown(id='names', value='Libellé du flux', options=[{'value': x, 'label': x} for x in ['Libellé du flux']],clearable=False),
        html.P("Valeur en DHS:"),
        dcc.Dropdown(id='values', value='Valeur DHS 2018',options=[{'value': x, 'label': x} for x in ['Valeur DHS 2018', 'Valeur DHS 2019', 'Valeur DHS 2020','Valeur DHS 2021']],clearable=False),
        dcc.Graph(id="pie-chart"),
        ],
        className="graphe",
        ),
    html.Br(),
    html.Br(),
  

   # *********************   GRAPHE3   ********************************
        html.Div(
        [
        html.Strong("Libellé du flux & Continent & Valeur DHS", className="subtitle padded",),
        dcc.Graph(id='graphe_4',figure=fig2)
        ],
        className="graphe",),
        html.Br(),
        html.Br(),
  

   # *********************   GRAPHE4   ********************************
        html.Div(
        [
        html.Strong("Libellé du flux & Libellé du pays & Valeur DHS", className="subtitle padded",),
        dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in all_pays],
        value=all_pays[3:],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
        ],
        className="graphe",
        ),
    html.Br(),
    html.Br(),

   # *********************   GRAPHE5   ********************************
       html.Div(
        [
        html.Strong("Carte graphique de le Libellé du flux", className="subtitle padded",),
        dcc.Graph(id='graphe_5',figure=fig5)
        ],
        className="graphe",
        ),
    html.Br(),
    html.Br(),
   
    
   # *********************   GRAPHE6   ********************************
        html.Div(
        [
        html.Strong("Libellé du flux & Libellé du groupement d'utilisation & Valeur DHS", className="subtitle padded",),
        dcc.Graph(id='graphe_6',figure=fig6,)

        ],
        className="graphe",
        ),
    html.Br(),        
    html.Br(),


   # *********************   GRAPHE7   ********************************
        html.Div(
        [
        html.Strong("Libellé du flux & Libellé de la section CTCI & Valeur DHS", className="subtitle padded",),
        dcc.Graph(id='graphe_7',figure=fig7,)

        ],
        className="graphe",
        ),
        html.Br(),
        
   # *****************************************************


],)
@app.callback(
    Output("pie-chart", "figure"), 
    [Input("names", "value"), 
     Input("values", "value")])
def generate_chart(names, values):
    fig1= px.pie(df, values=values, names=names,color=names,color_discrete_map={'Exportations FAB':'lightcyan','Importations CAF':'cyan','Importations en admission temporaire pour perfectionnement actif  avec paiement':'royalblue','Importations en admission temporaire pour perfectionnement actif  sans paiement':'darkblue',"Réexportations en suite d'admission temporaire pour perfectionnement actif avec paiement":'#0D5283'})
    fig1.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    return fig1

@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(pays):
    mask = df3["Libellé du pays"].isin(pays)
    fig = px.line(df3[mask], x="Année", y="Valeur DHS", color='Libellé du flux')
    fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)