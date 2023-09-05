from asyncio import LimitOverrunError
from ctypes import alignment

#from turtle import color, filling, width
from unicodedata import name
import dash
#import dash_table
from dash import dash_table
#import dash_html_components as html
#import dash_core_components as dcc
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import matplotlib 
import plotly.express as px
import plotly.figure_factory as ff
from dash import State, html
import numpy as np
from dash.dash_table.Format import Group

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)
server=app.server
DOUANE_LOGO = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdMAssJmAtnUVyh4Lr_EeQvuHgh6n__V9q8cBOMb_AFg&s"
dash_data=pd.read_excel(r'D:\Dash_21TO\DASH_21TO.xlsx',sheet_name='2023')
dash_data_1=pd.read_excel(r'D:\Dash_21TO\DASH_21TO.xlsx',sheet_name='2022')
tab_data=pd.read_excel(r'D:\Dash_21TO\DASH_21TO.xlsx',sheet_name='EXO')
tab_ind=pd.read_excel(r'D:\Dash_21TO\DINDI.xlsx')
#tab_rea=pd.read_excel(r'C:\Users\0003\Documents\Pratique_python\21TO\DINDI.xlsx',sheet_name='REA')
#tab_del=pd.read_excel(r'C:\Users\0003\Documents\Pratique_python\21TO\DINDI.xlsx',sheet_name='DEL')
tab_21TO=tab_ind.query("DIV=='21TO'")
#print(tab_21TO)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=DOUANE_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("REVUE DE LA PERFORMANCE DU BUREAU DE TOAMASINA ", className="text-center")),
                    ],
                    align="center",
                    className="g-0",
                ),
                #href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            
        ]
    ),
    color="dark",
    dark=True,
)
def TO_CDL (dash_data):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TOT_21TO'],name='21TO',
               text = dash_data['TOT_21TO'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#5474A0'),
                hoverinfo='text'),
                go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']], y=dash_data['TOT_CDL'],name='CDL',
                text = dash_data['TOT_CDL'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#9C0C36'),
                hoverinfo='text')])

    fig.update_layout(title = 'REPARTITION 21TO-CDL',
                  xaxis_title = 'MONTH',
                  yaxis_title = "VOLUME D'IMPORTATION", 
                  barmode = 'stack'
                  )
    return fig

def IM4_TREND(dash_data,dash_data_1):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TOT_IM4'],name='IM4 2023',text=dash_data['TOT_IM4'],textposition='auto',marker=dict(color='#03B2C9')),
                    go.Scatter(
            x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
            y=dash_data_1['TOT_IM4'],
            mode = 'markers+lines',
            name='IM4 2022',
            #line=dict(shape = 'spline', smoothing = 1.3, width = 3, color = '#9C0C38'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#FF00FF', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data['TOT_IM4'].astype(str) + '<br>' 


        )])
    fig.update_layout(title = 'VARIATION IM4',
                  xaxis_title = 'MONTH',
                  yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig


def IM_IM4(dash_data):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TOT_IMP'],name='IM',text=dash_data['TOT_IMP'],textposition='auto',marker=dict(color='#4E878C')),
                    go.Scatter(
            x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
            y=dash_data['TOT_IM4'],
            mode = 'markers+lines',
            name='IM4',
            #line=dict(shape = 'spline', smoothing = 1.3, width = 3, color = '#9C0C38'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#FF00FF', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data['TOT_IM4'].astype(str) + '<br>' 


        )])
    fig.update_layout(title = 'REPARTITION IMPORTATION',
                  xaxis_title = 'MONTH',
                  yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def rec_previsions(dash_data):
    prev=dash_data['PREVISION'].sum()
    rec=dash_data['RECETTES'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
        mode = "gauge+number+delta",
        title = {'text': "RECETTES"},
        delta = {'reference': 380},
        gauge = {'axis': {'range': [None, prev+50000000000]},
             'steps' : [
                 {'range': [0, 100000000000], 'color': "lightgray"},
                 {'range': [100000000000, 500000000000], 'color': "gray"}],
             'threshold' : {'line': {'color': "green", 'width': 20}, 'thickness': 0.75, 'value': prev}}))
    fig.update_layout(title = 'RECETTES ENREGISTREES',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def VOLUME (dash_data,dash_data_1):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TOT_IMP'],name='IMP 2023',
               text = dash_data['TOT_IMP'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='none',
                marker=dict(color='#5474A0'),
                hoverinfo='text',hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data['TOT_IMP'].astype(str) + '<br>' ),
                
                go.Scatter(
            x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
            y=dash_data_1['TOT_IMP'],
            mode = 'markers+lines',
            name='IMP 2022',
            #line=dict(shape = 'spline', smoothing = 1.3, width = 3, color = '#9C0C38'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#FF00FF', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['TOT_IMP'].astype(str) + '<br>' 


        )
                ])
    
    fig.update_annotations(font_size=20,align="left")
    fig.update_layout(title = 'IMPORTATION 2023vs2022',
                  xaxis_title = 'Periode',
                  yaxis_title = "VOLUME D''IMPORTATION",
                  barmode = 'stack'
                  )
    return fig

def REG_LIQ(dash_data,dash_data_1):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['REG_LIQ_YEL'],name='Enregistrement-liquidation en circuit jaune',
               text = dash_data['REG_LIQ_YEL'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#EBDA1E'),
                hoverinfo='text'),
                go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']], y=dash_data['REG_LIQ_RED'],name='Enregistrement-liquidation en circuit Rouge',
                text = dash_data['REG_LIQ_RED'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#FF0035'),
                hoverinfo='text'),
                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_LIQ_YEL'],
               mode = 'markers+lines',
               name='Délai jaune en 2022',
            line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_LIQ_YEL'].astype(str) + '<br>' 
                           ),
                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_LIQ_RED'],
               mode = 'markers+lines',
               name='Délai rouge en 2022',
            line=dict(smoothing = 1.3, width = 3, color = '#E03616'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#FF00FF', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_LIQ_RED'].astype(str) + '<br>' 
                           ),           
                
                ])

    fig.update_layout(title = 'DELAI ENREGISTREMENT-',
                  xaxis_title = 'MONTH',
                  yaxis_title = "HEURES OUVREES", 
                  #barmode = 'stack'
                  )
    return fig

def REG_EXIT(dash_data,dash_data_1):
    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['REG_EXIT_YEL'],name='Sortie jaune',
               text = dash_data['REG_EXIT_YEL'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#EBDA1E'),
                hoverinfo='text'),
                go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']], y=dash_data['REG_EXIT_RED'],name='Sortie Rouge',
                text = dash_data['REG_EXIT_RED'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#FF0035'),
                hoverinfo='text'),
                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_EXIT_YEL'],
               mode = 'markers+lines',
               name='jaune N-1',
            line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_EXIT_YEL'].astype(str) + '<br>' 
                           ),
                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_EXIT_RED'],
               mode = 'markers+lines',
               name='Rouge N-1',
            line=dict(smoothing = 1.3, width = 3, color = '#E03616'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#FF00FF', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_EXIT_RED'].astype(str) + '<br>' 
                           ),           
                
                ])

    fig.update_layout(title = 'ENREGISTREMENT-SORTIE',
                  xaxis_title = 'MONTH',
                  yaxis_title = "JOURS OUVRABLES", 
                  #barmode = 'stack'
                  )
    return fig

def Valeur(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['VALEUR'],name='Importation en 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#6A8E7F'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['VALEUR'].astype(str) + '<br>'),
                go.Bar(x=[dash_data['DASH_YEAR'],dash_data_1['DASH_MONTH']],y=dash_data_1['VALEUR'],name='Importation en 2022',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#87C38F'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['VALEUR'].astype(str) + '<br>'),

                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data['Franchise'],
               mode = 'markers+lines',
               name='Franchise 2023',
            line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data['Franchise'].astype(str) + '<br>' 
                           ),
                  go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['Franchise'],
               mode = 'markers+lines',
               name='Franchise 2022',
            line=dict(smoothing = 1.3, width = 3, color = '#9F9A56'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['Franchise'].astype(str) + '<br>' 
                           ),
                ])

    fig.update_layout(title = 'VALEUR D''IMPORTATION',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Montant en Ariary", 
                  #barmode = 'stack'
                  )
    return fig

def cours_devise(dash_data,dash_data_1):
    fig=go.Figure([go.Scatter(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['CUR_EURO'],name='EURO_2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                texttemplate='%{text:,.0f}',
                mode = 'markers+lines',
                #textposition='auto',
                marker=dict(color='#0B4F6C'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['CUR_EURO'].astype(str) + '<br>'),
                go.Scatter(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['CUR_USD'],name='USD_2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                mode = 'markers+lines',
                #textposition='auto',
                marker=dict(color='#3E8989'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['CUR_USD'].astype(str) + '<br>'),
                go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH'],],
                y=dash_data_1['CUR_EURO'],
               mode = 'markers+lines',
               name='EURO_2022',
               marker=dict(color='#6B8EC7'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['CUR_EURO'].astype(str) + '<br>' 
                           ),
            go.Scatter(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH'],],
                y=dash_data_1['CUR_USD'],
               mode = 'markers+lines',
               name='USD_2022',
               marker=dict(color='#764919'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['CUR_USD'].astype(str) + '<br>' 
                           ),               
                
                ])

    fig.update_layout(#title = 'COURS DEVISE',
                  xaxis_title = 'MONTH',
                  yaxis_title = "ARIARY", 
                  #barmode = 'stack'
                  )
    return fig    
def susp_conf(dash_data,dash_data_1):
    fig=go.Figure([go.Scatter(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['SUSP_CONF'],name='Suspects confirmés 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                mode = 'markers+lines',
                #textposition='auto',
                marker=dict(color='#EB5D47'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['SUSP_CONF'].astype(str) + '<br>'),
                go.Scatter(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['SUSP_CONF_2022'],name='Suspects confirmés 2022',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                mode = 'markers+lines',
                #textposition='auto',
                marker=dict(color='#764919'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['SUSP_CONF_2022'].astype(str) + '<br>'),
                             
                
                ])

    fig.update_layout(title = 'Evolution Taux de suspects confirmés',
                  xaxis_title = 'MONTH',
                  yaxis_title = "TAUX DE  ICION", 
                  #barmode = 'stack'
                  )
    return fig 

def EVP(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['EVP'],name='EVP en 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#6A8E7F'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['EVP'].astype(str) + '<br>'),
                
                go.Bar(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['EVP'],
               #mode = 'markers+lines',
               name='EVP en 2022',
               marker=dict(color='#7380AB'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['EVP'].astype(str) + '<br>' 
                           ),
                           
                
                ])

    fig.update_layout(title = 'TAXE MOYENNE PAR EVP',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Montant en Ariary", 
                  #barmode = 'stack'
                  )
    return fig

def DAU(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TAX_PER_DAU'],name='TAX DAU 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#3A8E7F'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['TAX_PER_DAU'].astype(str) + '<br>'),
                
                go.Bar(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['TAX_PER_DAU'],
               #mode = 'markers+lines',
               name='TAX DAU en 2022',
               marker=dict(color='#9572AB'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['TAX_PER_DAU'].astype(str) + '<br>' 
                           ),
                           
                
                ])

    fig.update_layout(title = 'TAXE MOYENNE PAR DAU',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Montant en Ariary", 
                  #barmode = 'stack'
                  )
    return fig



def Taxe_liq(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TAX'],name='Taxes liquidées 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#CF995F'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['TAX'].astype(str) + '<br>'),
                
                go.Bar(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['TAX'],
               #mode = 'markers+lines',
               name='Taxes liquidées en 2022',
               marker=dict(color='#FBD24B'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['TAX'].astype(str) + '<br>' 
                           ),
                           
                
                ])

    fig.update_layout(title = 'TAXES LIQUIDEES',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Montant en Ariary", 
                  #barmode = 'stack'
                  )
    return fig

def reg_liq_jaune(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['REG_LIQ_YEL'],name='REG_LIQ_jaune 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#ECA009'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['REG_LIQ_YEL'].astype(str) + '<br>'),
                
                go.Bar(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_LIQ_YEL'],
               #mode = 'markers+lines',
               name='REG_LIQ 2022',
               marker=dict(color='#F9C762'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_LIQ_YEL'].astype(str) + '<br>' 
                           ),
                           
                
                ])

    fig.update_layout(title = 'Délai de liquidation jaune',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Heures ouvrées", 
                  #barmode = 'stack'
                  )
    return fig

def reg_liq_rouge(dash_data,dash_data_1):

    fig=go.Figure([go.Bar(x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['REG_LIQ_RED'],name='REG_LIQ_Rouge 2023',
               #text = dash_data['VALEUR'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}',
                textposition='auto',
                marker=dict(color='#F52314'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' +
                '<b>Mois</b>: ' + dash_data['DASH_MONTH'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + dash_data['REG_LIQ_RED'].astype(str) + '<br>'),
                
                go.Bar(
                x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],
                y=dash_data_1['REG_LIQ_RED'],
               #mode = 'markers+lines',
               name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + dash_data_1['DASH_YEAR'].astype(str) + '<br>' +
            '<b>Mois</b>: ' + dash_data_1['DASH_MONTH'].astype(str) + '<br>' +
            '<b>Nombre</b>: ' + dash_data_1['REG_LIQ_RED'].astype(str) + '<br>' 
                           ),
                           
                
                ])

    fig.update_layout(title = 'Délai de liquidation rouge',
                  xaxis_title = 'MONTH',
                  yaxis_title = "Heures ouvrées", 
                  #barmode = 'stack'
                  )
    return fig


def Recap_delai_jaune(dash_data,dash_data_1):
    recap_jaune=dash_data['REG_LIQ_YEL'].mean()
    ref_recap_jaune=dash_data_1['REG_LIQ_YEL'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['REG_LIQ_YEL'].mean()),
    
    delta = {'reference': int(dash_data_1['REG_LIQ_YEL'].mean()), 'relative': True,'valueformat':'.2%'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(title={
            'text' : 'Délai moyen jaune',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
#paper_bgcolor="lightgray",
height=70,  # Added parameter
)  
    return fig

def Recap_delai_rouge(dash_data,dash_data_1):
    recap_jaune=dash_data['REG_LIQ_RED'].mean()
    ref_recap_jaune=dash_data_1['REG_LIQ_RED'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['REG_LIQ_RED'].mean()),
    
    delta = {'reference': int(dash_data_1['REG_LIQ_RED'].mean()), 'relative': True,'valueformat':'.2%'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(title={
            'text' : 'Délai moyen rouge',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
#paper_bgcolor="lightgray",
height=70,  # Added parameter
)  
    return fig    

def Recap_delai_sortie_jaune(dash_data,dash_data_1):
    recap_jaune=dash_data['REG_EXIT_YEL'].mean()
    ref_recap_jaune=dash_data_1['REG_EXIT_YEL'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['REG_EXIT_YEL'].mean()),
    
    delta = {'reference': int(dash_data_1['REG_EXIT_YEL'].mean()), 'relative': True,'valueformat':'.2%'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(title={
            'text' : 'Délai de sortie moyen jaune',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
#paper_bgcolor="lightgray",
height=70,  # Added parameter
)  
    return fig   

def Recap_delai_sortie_Rouge(dash_data,dash_data_1):
    recap_jaune=dash_data['REG_EXIT_RED'].mean()
    ref_recap_jaune=dash_data_1['REG_EXIT_RED'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['REG_EXIT_RED'].mean()),
    
    delta = {'reference': int(dash_data_1['REG_EXIT_RED'].mean()), 'relative': True,'valueformat':'.2%'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(title={
            'text' : 'Délai de sortie moyen rouge',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
#paper_bgcolor="lightgray",
height=70,  # Added parameter
)  
    return fig  
def Recap_delai_sortie_Vert(dash_data,dash_data_1):
    recap_jaune=dash_data['REG_EXIT_GREEN'].mean()
    ref_recap_jaune=dash_data_1['REG_EXIT_GREEN'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['REG_EXIT_GREEN'].mean()),
    
    delta = {'reference': int(dash_data_1['REG_EXIT_GREEN'].mean()), 'relative': True,'valueformat':'.2f'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(title={
            'text' : 'Délai de sortie moyen vert',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
#paper_bgcolor="lightgray",
height=70,  # Added parameter
)  
    return fig  

def Recap_tax_liq(dash_data,dash_data_1):
    data_prev=dash_data_1['TAX'].mean()
    data=dash_data['TAX'].mean()
    fig=go.Figure(go.Indicator(
    mode = "number+delta",
    number={'font':{'size':35},},
    value = int(dash_data['TAX'].mean()),
    
    delta = {'reference': int(dash_data_1['TAX'].mean()), 'relative': True,'valueformat':'.2%'},
    domain = {'x': [0, 0.5], 'y': [0.5, 1]}
    )
    )
    fig.update_layout(
    paper_bgcolor="lightgray",
    height=70,  # Added parameter
)  
    return fig 

def structure_tarifaire(dash_data,dash_data_1):
    Zero=dash_data['TAX_EXEMPT_PERC'].mean()
    Zero_twenty=dash_data['ZERO_TWENTY_PERC'].mean()
    Five_twenty=dash_data['FIVE_TWENTY_PERC'].mean()
    Ten_twenty=dash_data['TEN_TWENTY_PERC'].mean()
    twenty_twenty=dash_data['TWENTY_TWENTY_PERC'].mean()
    struct=[Zero,Zero_twenty,Five_twenty,Ten_twenty,twenty_twenty]
    Zero_ref=dash_data_1['TAX_EXEMPT_PERC'].mean()
    Zero_twenty_ref=dash_data_1['ZERO_TWENTY_PERC'].mean()
    Five_twenty_ref=dash_data_1['FIVE_TWENTY_PERC'].mean()
    Ten_twenty_ref=dash_data_1['TEN_TWENTY_PERC'].mean()
    twenty_twenty_ref=dash_data_1['TWENTY_TWENTY_PERC'].mean()
    struct_ref=[Zero_ref,Zero_twenty_ref,Five_twenty_ref,Ten_twenty_ref,twenty_twenty_ref]
    #x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TAX'],name='Taxes liquidées 2023',
    fig = go.Figure([go.Bar(x=['0','0-20','5-20','10-20','20-20'], y=[Zero,Zero_twenty,Five_twenty,Ten_twenty,twenty_twenty],name='Structure tarifaire 2023',
    #text=y,
    hoverinfo='text',
    hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' #+
            #'<b>Moyenne</b>: ' + dash_data['TAX_2022'].astype(str) + '<br>' 
    ),
    go.Bar(x=['0','0-20','5-20','10-20','20-20'], y=[Zero_ref,Zero_twenty_ref,Five_twenty_ref,Ten_twenty_ref,twenty_twenty_ref],name='Structure tarifaire 2022',
    hoverinfo='text',
    hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' #+
            #'<b>Moyenne</b>: ' + dash_data['TAX_2022'].astype(str) + '<br>' 
    )
    ])
     
    fig.update_layout(title_text="Structure Tarifaire 2023(en termes de valeur)",
                  title_font_size=20)
                  
    return fig

def structure_tarifaire_bis(dash_data,dash_data_1):
    Zero=dash_data['zero_perc'].mean()
    Zero_twenty=dash_data['zero_twenty'].mean()
    Five_twenty=dash_data['five_twenty'].mean()
    Ten_twenty=dash_data['ten_twenty'].mean()
    twenty_twenty=dash_data['twenty_twenty'].mean()
    Zero_ref=dash_data_1['zero_perc'].mean()
    Zero_twenty_ref=dash_data_1['zero_twenty'].mean()
    Five_twenty_ref=dash_data_1['five_twenty'].mean()
    Ten_twenty_ref=dash_data_1['ten_twenty'].mean()
    twenty_twenty_ref=dash_data_1['twenty_twenty'].mean()
    #x=[dash_data['DASH_YEAR'],dash_data['DASH_MONTH']],y=dash_data['TAX'],name='Taxes liquidées 2023',
    fig = go.Figure([go.Bar(x=['0','0-20','5-20','10-20','20-20'], y=[Zero,Zero_twenty,Five_twenty,Ten_twenty,twenty_twenty],name='Structure tarifaire 2023',
    hoverinfo='text',
    hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' #+
            #'<b>Moyenne</b>: ' + dash_data['TAX_2022'].astype(str) + '<br>' 
    ),
    go.Bar(x=['0','0-20','5-20','10-20','20-20'], y=[Zero_ref,Zero_twenty_ref,Five_twenty_ref,Ten_twenty_ref,twenty_twenty_ref],name='Structure tarifaire 2022',
    hoverinfo='text',
    hovertext=
            '<b>Annee</b>: ' + dash_data['DASH_YEAR'].astype(str) + '<br>' #+
            #'<b>Moyenne</b>: ' + dash_data['TAX_2022'].astype(str) + '<br>' 
    )
    ])
     
    fig.update_layout(title_text="Structure Tarifaire 2023(en termes de volume)",
                  title_font_size=20)
                  
    return fig


def recap_taxes_liquidees(dash_data,dash_data_1):
    prev=dash_data_1['TAX'].sum()
    rec=dash_data['TAX'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
        mode = "number+delta",
        title = {'text': "Taxes liquidées"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title = 'Taxes liquidées',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig
def recap_volume(dash_data,dash_data_1):
    prev=dash_data_1['TOT_IMP'].sum()
    rec=dash_data['TOT_IMP'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(#"title":{"text":'Déclarations d''importation'},
                  title={
            'text' : 'Déclarations d''importation',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
                #heigth='80px',
                #width=2
            )
    return fig

def recap_ctn(dash_data,dash_data_1):
    prev=dash_data_1['RES_CTN'].sum()
    rec=dash_data['RES_CTN'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'Volume Conteneurs',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
        
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IM4(dash_data,dash_data_1):
    prev=dash_data_1['TOT_IM4'].sum()
    rec=dash_data['TOT_IM4'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'Déclarations IM4',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_OTH(dash_data,dash_data_1):
    prev=dash_data_1['TOT_OTH'].sum()
    rec=dash_data['TOT_OTH'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'Autres déclarations d''importation',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IM4_JAUNE(dash_data,dash_data_1):
    prev=dash_data_1['YELLOW_IM4'].sum()
    rec=dash_data['YELLOW_IM4'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  title={
            'text' : 'IM4 JAUNE',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def RECAP_IM4_ROUGE(dash_data,dash_data_1):
    prev=dash_data_1['RED_IM4'].sum()
    rec=dash_data['RED_IM4'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'IM4 ROUGE',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def RECAP_IM4_VERT(dash_data,dash_data_1):
    prev=dash_data_1['TOT_IM4'].sum()-dash_data_1['RED_IM4'].sum()-dash_data_1['YELLOW_IM4'].sum()
    rec=dash_data['TOT_IM4'].sum()-dash_data['RED_IM4'].sum()-dash_data['YELLOW_IM4'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'IM4 VERT',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig




def RECAP_VALEUR(dash_data,dash_data_1):
    prev=dash_data_1['VALEUR'].sum()
    rec=dash_data['VALEUR'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "VALEUR D'IMPORTATION",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig
def RECAP_FRANCHISE(dash_data,dash_data_1):
    prev=dash_data_1['Franchise'].sum()
    rec=dash_data['Franchise'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "FRANCHISE",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig



def RECAP_TAXE(dash_data,dash_data_1):
    prev=dash_data_1['TAX'].sum()
    rec=dash_data['TAX'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "Taxes liquidées",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_TAX_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['TAX_RATIO'].mean()
    rec=dash_data['TAX_RATIO'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : "Ratio de Taxation",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig    

def rec_previsions(dash_data,dash_data_1):
    prev=dash_data['PREVISION'].sum()
    rec=dash_data['RECETTES'].sum()
    rec_prev=dash_data_1['RECETTES'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
        mode = "gauge+number+delta",
        #title = {'text': "RECETTES"},
        delta = {'reference': rec_prev,'increasing': {'color': "#0353A4"},'relative': True,'valueformat':'.2%'},
        gauge = {'axis': {'range': [None, prev+50000000000],'tickcolor': "darkblue",'tickwidth': 1},
             'bar': {'color': "#BB1711"},
             'steps' : [
                 {'range': [0, 100000000000], #'color': "lightgray"
                  },
                 {'range': [100000000000, 500000000000], #'color': "gray"
                  }],
             'threshold' : {'line': {'color': "green", 'width': 10}, 'thickness': 0.75, 'value': prev}}))
    fig.update_layout(title={'text' : "Recettes et prévisions",
            'y':0.9,
            'x':0,
            'xanchor': 'center',
            'yanchor':'top'
    }
        #title = 'RECETTES ENREGISTREES',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_EVP(dash_data,dash_data_1):
    prev=dash_data_1['EVP'].mean()
    rec=dash_data['EVP'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'Taxe Moyenne EVP',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig 

def RECAP_TAX_DAU(dash_data,dash_data_1):
    prev=dash_data_1['TAX_PER_DAU'].mean()
    rec=dash_data['TAX_PER_DAU'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : 'Taxe moyenne par DAU',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig 

def RECAP_0(dash_data,dash_data_1):
    prev=dash_data_1['TAX_EXEMPT_PERC'].mean()
    rec=dash_data['TAX_EXEMPT_PERC'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(
        title={
            'text' : 'Quotité 0',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_0_20(dash_data,dash_data_1):
    prev=dash_data_1['ZERO_TWENTY_PERC'].mean()
    rec=dash_data['ZERO_TWENTY_PERC'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : 'Quotité 0-20',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_5_20(dash_data,dash_data_1):
    prev=dash_data_1['FIVE_TWENTY_PERC'].mean()
    rec=dash_data['FIVE_TWENTY_PERC'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : 'Quotité 5-20',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  },#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_10_20(dash_data,dash_data_1):
    prev=dash_data_1['TEN_TWENTY_PERC'].mean()
    rec=dash_data['TEN_TWENTY_PERC'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : 'Quotité 10-20',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_20_20(dash_data,dash_data_1):
    prev=dash_data_1['TWENTY_TWENTY_PERC'].mean()
    rec=dash_data['TWENTY_TWENTY_PERC'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : 'Quotité 20-20',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
        #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_SUSP_CONF(dash_data,dash_data_1):
    prev=dash_data_1['SUSP_CONF'].mean()
    rec=dash_data['SUSP_CONF'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2f'},
        ))
    fig.update_layout(title={
            'text' : 'Taux de suspects confirmés',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  } #title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IVALUE(dash_data,dash_data_1):
    prev=dash_data_1['I_VALUE_COUNT'].sum()
    rec=dash_data['I_VALUE_COUNT'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : ' TOTAL IVALUE ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IVALUE_VAL(dash_data,dash_data_1):
    prev=dash_data_1['VALEUR_IVALUE'].sum()
    rec=dash_data['VALEUR_IVALUE'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : ' VALEUR IVALUE EN USD',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IVALUE_ALIGN(dash_data,dash_data_1):
    prev=dash_data_1['I_VALUE_ALIGN'].sum()
    rec=dash_data['I_VALUE_ALIGN'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : ' ALIGNEMENT IVALUE ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IVALUE_ALIGN_VAL(dash_data,dash_data_1):
    prev=dash_data_1['I_VALUE_ALIGN_VAL'].sum()
    rec=dash_data['I_VALUE_ALIGN_VAL'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : ' VALEUR IVALUE ALIGNE en USD ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig


def RECAP_IVALUE_REDR(dash_data,dash_data_1):
    prev=dash_data_1['I_VALUE_REDRE'].sum()
    rec=dash_data['I_VALUE_REDRE'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  IVALUE redressés ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_IVALUE_REDR_VAL(dash_data,dash_data_1):
    prev=dash_data_1['VALEUR_REDR'].sum()
    rec=dash_data['VALEUR_REDR'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  VALEUR IVALUE redressés en USD ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig


def RECAP_DC(dash_data,dash_data_1):
    prev=dash_data_1['DC'].sum()
    rec=dash_data['DC'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : ' Montant DC ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def RECAP_CTX(dash_data,dash_data_1):
    prev=dash_data_1['CTX'].sum()
    rec=dash_data['CTX'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  Dossiers CTX ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig
def RECAP_CTX_J(dash_data,dash_data_1):
    prev=dash_data_1['CTX_JAUNE'].sum()
    rec=dash_data['CTX_JAUNE'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  Dossiers CTX jaune',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_CTX_R(dash_data,dash_data_1):
    prev=dash_data_1['CTX_ROUGE'].sum()
    rec=dash_data['CTX_ROUGE'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  Dossiers CTX Rouge',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig


def RECAP_DC_IVALUE(dash_data,dash_data_1):
    prev=dash_data_1['IVALUE_DC'].sum()
    rec=dash_data['IVALUE_DC'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : '  DC suite IVALUE ',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
                  
    return fig

def RECAP_DOWNGRADE(dash_data,dash_data_1):
    prev=dash_data_1['Downgrade'].sum()
    rec=dash_data['Downgrade'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_DOWNGRADE_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['RATIO_DOWN'].mean()
    rec=dash_data['RATIO_DOWN'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title = 'Taux de downgrade',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_UPGRADE(dash_data,dash_data_1):
    prev=dash_data_1['Upgrade'].sum()
    rec=dash_data['Upgrade'].sum()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(#title = 'Declarations d''importation',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def RECAP_UPGRADE_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['RATIO_UP'].mean()
    rec=dash_data['RATIO_UP'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title = 'Taux de upgrade',
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig

def Recap_appli_IVALUE(dash_data,dash_data_1):
    prev=dash_data_1['APPLI_IVALUE_RATIO'].mean()
    rec=dash_data['APPLI_IVALUE_RATIO'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = float(rec*100),
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': float(prev*100),'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "Taux d'application IVALUE",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  #xaxis_title = 'MONTH',
                  #yaxis_title = "VOLUME D'IMPORTATION", 
                  #barmode = 'stack'
                  )
    return fig    

def DAU_IND(INDI_TAB):
    fig=go.Figure([go.Bar(x=[INDI_TAB['Periode']],y=INDI_TAB['A'],
               text = INDI_TAB['IM.269334-DN'],
                #texttemplate='%{text:,.0f}',
                    #texttemplate='%{text:,.0f}', 
                textposition='auto',
                marker=dict(color='#F52314'),
                hoverinfo='text',
                hovertext=
                '<b>Annee</b>: ' + 'IM.269334-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.269334-DN'].astype(str) + '<br>'),
                
                go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.273342-DN'],
                text = INDI_TAB['IM.273342-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.269334-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.269334-DN'].astype(str) + '<br>' 
                           ),
               go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.273354-DN'],
                text = INDI_TAB['IM.273354-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.273354-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.273354-DN'].astype(str) + '<br>' 
                           ), 
                go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.282271-DN'],
                text = INDI_TAB['IM.282271-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.282271-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.282271-DN'].astype(str) + '<br>' 
                           ),                       
              go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.295774-DN'],
                text = INDI_TAB['IM.295774-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.295774-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.295774-DN'].astype(str) + '<br>' 
                           ),  
               go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.299553-DN'],
                text = INDI_TAB['IM.299553-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.299553-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.299553-DN'].astype(str) + '<br>' 
                           ),    
            go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.304426-DN'],
                text = INDI_TAB['IM.304426-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.304426-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.304426-DN'].astype(str) + '<br>' 
                           ), 
              go.Bar(
                x=[INDI_TAB['Periode']],
                y=INDI_TAB['IM.330998-DN'],
                text = INDI_TAB['IM.330998-DN'],
               #mode = 'markers+lines',
               #name='REG_LIQ_Rouge 2022',
               marker=dict(color='#880E07'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            hovertext=
            '<b>Annee</b>: ' + 'IM.330998-DN' + '<br>' +
                '<b>Mois</b>: ' + INDI_TAB['Periode'].astype(str) + '<br>' +
                '<b>Nombre</b>: ' + INDI_TAB['IM.330998-DN'].astype(str) + '<br>' 
                           ),              

                ])

    fig.update_layout(title = 'Total déclarations',
                  xaxis_title = 'IVL',
                  yaxis_title = "NOMBRE DAUS", 
                  #barmode = 'stack'
                  )
def DAU_ID(tab_ind):
    #fig=go.Figure(go.Bar(x=tab_ind['INSP_ID'],y=tab_ind['DAU_I_LIQ']
               #))
    fig = px.scatter(tab_ind, x=tab_ind['INSP_ID'], y=tab_ind['DAU_I_LIQ'],
	         color='DIV',size='DAU_I_LIQ')
    fig.update_layout(title = 'Total déclarations',
                  xaxis_title = 'IVL',
                  yaxis_title = "NOMBRE DAUS", 
                  barmode = 'stack'
                  )
    return fig


def DELAI_JAUNE_IND(tab_ind):
    
    fig=px.scatter(tab_ind,x=tab_ind['INSP_ID'],y=tab_ind['DELAI_JAUNE'],
               color='DIV',
               size=tab_ind['DELAI_JAUNE'])
    
    fig.update_layout(title = 'Délai jaune ',
                  xaxis_title = 'IVL',
                  yaxis_title = "Heures ouvrées", 
                  #barmode = 'stack'
                  )
    return fig
### REATTRIBUTION
def REAT(tab_21TO):
    
    fig=px.scatter(tab_21TO,x=tab_21TO['INSP_ID'],y=tab_21TO['REAT'],
               color='DIV',
               size='REAT')
    
    fig.update_layout(title = 'Total reattributions',
                  xaxis_title = 'IVL',
                  yaxis_title = "NOMBRE DAUS RECUS", 
                  barmode = 'group'
                  )
    return fig

def DELAI_ROUGE_IND(tab_ind):
    tab_rouge=tab_ind.query("DIV=='21TO'")  
    fig=go.Figure([ 
                    go.Bar(
                x=tab_rouge['INSP_ID'],
                y=tab_rouge['DELAI_JAUNE'],
                text = tab_rouge['DELAI_JAUNE'],
               #mode = 'markers+lines',
               name='Délai jaune',
               marker=dict(color='#FFE299'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            #hovertext=
            #'<b>Annee</b>: ' + tab_ind['DELAI_JAUNE'] + '<br>' +
                #'<b>Mois</b>: ' + tab_ind['Periode'].astype(str) + '<br>' +
                #'<b>Nombre</b>: ' + tab_ind['IM.304426-DN'].astype(str) + '<br>' 
                           ), 
              go.Bar(
                x=tab_rouge['INSP_ID'],
                y=tab_rouge['DELAI_ROUGE'],
                text = tab_rouge['DELAI_ROUGE'],
               #mode = 'markers+lines',
               name='Délai rouge',
               marker=dict(color='#D00000'),
            #line=dict(smoothing = 1.3, width = 3, color = '#F7D002'),
            #marker=dict(color='white', size = 10, symbol = 'circle',
                        #line=dict(color = '#F7D002', width = 2)),
            hoverinfo='text',
            #hovertext=
            #'<b>Annee</b>: ' + 'IM.330998-DN' + '<br>' +
                #'<b>Mois</b>: ' + tab_ind['Periode'].astype(str) + '<br>' +
                #'<b>Nombre</b>: ' + tab_ind['IM.330998-DN'].astype(str) + '<br>' 
                           ),
                ])
    
    fig.update_layout(title = 'Délai rouge',
                  xaxis_title = 'IVL',
                  yaxis_title = "Heures ouvrées", 
                  barmode = 'stack'
                  )
    return fig

def DELAI_ROUGE_SCAN_IND(tab_ind):
    tab_scan=tab_ind.query("DIV=='21TO'")
    fig=go.Figure(go.Bar(x=tab_scan['INSP_ID'],y=tab_scan['SCAN_LIQ'],name='Scan_liquidation',
          text = tab_scan['SCAN_LIQ'] ,  marker=dict(color='#D00000')            
               ))
    
    fig.update_layout(title = 'Délai Scan_liquidation',
                  xaxis_title = 'IVL',
                  yaxis_title = "Heures ouvrées", 
                  barmode = 'group'
                  )
    return fig

def DAU_ROUGE_IND(tab_ind):
    tab_scan=tab_ind.query("DIV=='21TO'").sort_values(by=['DAU_RED'],ascending=[True])
    fig=go.Figure(go.Bar(x=tab_scan['DAU_RED'],y=tab_scan['INSP_ID'],name='Daus Rouges',orientation='h',
          #text = tab_scan['SCAN_LIQ'] ,  
          marker=dict(color='#D00000')            
               ))
    
    fig.update_layout(title = 'Nombre DAU rouges',
                  xaxis_title = 'IVL',
                  yaxis_title = "Nombre", 
                  barmode = 'group'
                  )
    return fig


def ASSI_TAX_IND(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['ASSIETTE'],y=tab_ass['INSP_ID'],name='Assiette',
          text = tab_ass['ASSIETTE'] ,  marker=dict(color='#D00000') ,orientation='h'          
               ),go.Bar(x=tab_ass['TAX'],y=tab_ass['INSP_ID'],name='Taxes liquidées',
          text = tab_ass['TAX'] ,  marker=dict(color='#1C3144') ,orientation='h'          
               )
               ])
    
    fig.update_layout(title = 'Assiette',
                  xaxis_title = 'Montant en Ariary',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def TAX_RATIO_IND(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['INSP_ID'],y=tab_ass['TAX_RATIO'],name='Ratio taxation',
          text = tab_ass['TAX_RATIO'] ,  marker=dict(color='#0B5351')#,orientation='h'          
               )
               ])
    
    fig.update_layout(title = 'Ratio de taxation',
                  xaxis_title = 'IVL',
                  yaxis_title = "Taux", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_0_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['ZERO'],y=tab_ass['INSP_ID'],name='Quotité 0',
          #text = tab_ass['ZERO'] ,  
          marker=dict(color='#1C3144') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 0',
                 xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_0_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['ZERO_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 0_20',
          #text = tab_ass['ZERO_TWENTY'] ,  
          marker=dict(color='#80234A') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 0-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_5_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['FIVE_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 0_20',
          #text = tab_ass['FIVE_TWENTY'] , 
            marker=dict(color='#665255') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 5-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_5_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['FIVE_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 5_20',
          #text = tab_ass['FIVE_TWENTY'] ,  
          marker=dict(color='#D7335C') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 5-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_10_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['TEN_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 10_20',
          #text = tab_ass['TEN_TWENTY'] ,  
          marker=dict(color='#D90F08') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 10-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def struc_tar_20_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['TWENTY_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 20_20',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#3E6990') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 20-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def TAXE_EVP_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['EVP'],y=tab_ass['INSP_ID'],name='Taxe EVP',
          #text = tab_ass['EVP'] , 
            marker=dict(color='#0B5351') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Taxe EVP',
                  xaxis_title = 'EVP en AR',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def DC_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['DC'],y=tab_ass['INSP_ID'],name='DC',
          #text = tab_ass['DC'] ,  
          marker=dict(color='#4E8098') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'DC',
                  xaxis_title = 'DC en AR',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def SUSP_ind(tab_ind):
    tab_ass=tab_ind.query("DIV=='21TO'")
    fig=px.scatter(tab_ass,x=tab_ass['INSP_ID'],y=tab_ass['SUSP_CONF'],
               color='DIV',
               size='SUSP_CONF')
    
    fig.update_layout(title = 'TSC',
                  xaxis_title = 'Taux',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def RECAP_J6_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['JAUNE_RAT_6H'].mean()
    rec=dash_data['JAUNE_RAT_6H'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec*100,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev*100,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "Jaunes liquidés en moins de 6H",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def RECAP_J2_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['REG_EXIT_YEL_RAT'].mean()
    rec=dash_data['REG_EXIT_YEL_RAT'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec*100,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev*100,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "Sortie Jaune< 2 jours ",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def RECAP_R2_RATIO(dash_data,dash_data_1):
    prev=dash_data_1['REG_EXIT_RED_RAT'].mean()
    rec=dash_data['REG_EXIT_RED_RAT'].mean()
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = rec*100,
         number={'font':{'size':30},},
        mode = "number+delta",
        #title = {'text': "Nombre Déclarations Importation"},
        delta = {'reference': prev*100,'relative': True,'valueformat':'.2%'},
        ))
    fig.update_layout(title={
            'text' : "Sortie Rouge <2 Jours",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor':'top'
                  }
                  )
    return fig

def struc_tar_10_20_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['ASSIETTE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['TEN_TWENTY'],y=tab_ass['INSP_ID'],name='Quotité 10_20',
          #text = tab_ass['TEN_TWENTY'] ,  
          marker=dict(color='#D90F08') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Quotité 10-20',
                  xaxis_title = 'TAUX',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def TOT_IVALUE_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['TOT_IVALUE'],y=tab_ass['INSP_ID'],name='Total Ivalue',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#3E6990') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'Total Ivalue',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def TOT_IVALUE_CTX_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['IVALUE_CTX'],y=tab_ass['INSP_ID'],name='IVALUE CTX',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#281240') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'IVALUE CTX',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def TOT_IVALUE_CTX_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['IVALUE_CTX'],y=tab_ass['INSP_ID'],name='IVALUE CTX',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#281240') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'IVALUE CTX',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def YEL_IVALUE_CTX_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['I_VALUE_YEL_CTX'],y=tab_ass['INSP_ID'],name='IVALUE CTX Jaune',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#CCA43B') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'IVALUE CTX Jaune',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def RED_IVALUE_CTX_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['I_VALUE_RED_CTX'],y=tab_ass['INSP_ID'],name='IVALUE CTX Rouge',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#BA274A') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'IVALUE CTX Rouge',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

def APPLIED_IVALUE_ind(tab_ind):
    tab_ass=tab_ind.sort_values(by=['TOT_IVALUE'],ascending=[True])
    fig=go.Figure([go.Bar(x=tab_ass['APPLIED_IVALUE'],y=tab_ass['INSP_ID'],name='IVALUE appliqué',
          #text = tab_ass['TWENTY_TWENTY'] ,  
          marker=dict(color='#2892D7') ,orientation='h'           
               )
               ])
    
    fig.update_layout(title = 'IVALUE appliqué',
                  xaxis_title = 'Nombre',
                  yaxis_title = "IVL", 
                  barmode = 'group'
                  )
    return fig

tab1_content = dbc.Container([
    dbc.Row( html.H5(html.B(html.U("RECAPITULATION SUR LE VOLUME D'IMPORTATIONS")))),
    html.Br(),
    dbc.Row(
        [  dbc.Col([
            #html.P("Total Déclarations importations", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=recap_volume(dash_data,dash_data_1),style = {'height':'90px',}))]),
            html.Br(),
             dbc.Card([dbc.CardBody(dcc.Graph(figure=VOLUME(dash_data,dash_data_1),style = {'height':'350px',}))])      
        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
            dbc.Col([
            #html.P("Total Déclarations IM4", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IM4(dash_data,dash_data_1),style = {'height':'90px',}))]),      
            html.Br(),
             dbc.Card([dbc.CardBody(dcc.Graph(figure=IM4_TREND(dash_data,dash_data_1),style = {'height':'350px',}))])],xl=4,lg=6,md = 6,sm=12,xs = 12),
        dbc.Col([
            #html.P("Total Déclarations importations", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_OTH(dash_data,dash_data_1),style = {'height':'90px',}))]),
             html.Br(),
             dbc.Card([dbc.CardBody(dcc.Graph(figure=IM_IM4(dash_data),style = {'height':'350px',}))])     
        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
        ]
    )],
className="mt-3",fluid = True
)

tab2_content = dbc.Container([
    dbc.Row( html.H5(html.B(html.U("RECAPITULATION DES IM4 PAR CIRCUIT")))),
    html.Br(),
    dbc.Row(
        [  dbc.Col([
            #html.P("IM4 JAUNE", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IM4_JAUNE(dash_data,dash_data_1),style = {'height':'90px',}))]),
            
                
        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
            dbc.Col([
             #html.P("IM4 ROUGE", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IM4_ROUGE(dash_data,dash_data_1),style = {'height':'90px',}))]),
            html.Br(),  
            
            ],xl=4,lg=6,md = 6,sm=12,xs = 12),
        dbc.Col([
            #html.P("IM4 VERT", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IM4_VERT(dash_data,dash_data_1),style = {'height':'90px',}))]),
                  
        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
        ]
    ),
    dbc.Row(html.H5(html.B(html.U("DELAI DE DEDOUANEMENT")))),
    dbc.Row([ 
             dbc.Col(
             dbc.Card([
                 dbc.CardBody(dcc.Graph(figure=reg_liq_jaune(dash_data,dash_data_1),style = {'height':'300px',}))
                     ]),xl=6,lg=6,md = 6,sm=12,xs = 12
                    ),
             dbc.Col(
             dbc.Card([
                 dbc.CardBody(dcc.Graph(figure=reg_liq_rouge(dash_data,dash_data_1),style = {'height':'300px',}))
                     ]),xl=6,lg=6,md = 6,sm=12,xs = 12
                    )       
           ]), 
           html.Br(),
     dbc.Row( html.H6(html.B(html.U("RECAPITULATION DES DELAIS DE LIQUIDATION")))),      
    html.Br(),
    dbc.Row([ 
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=Recap_delai_jaune(dash_data,dash_data_1),style = {'height':'90px',})),html.H2('H')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=Recap_delai_rouge(dash_data,dash_data_1),style = {'height':'90px',})),html.H2('H')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),        
            ]),
            html.Br(),
     dbc.Row( html.H6(html.B(html.U("RECAPITULATION DES DELAIS DE SORTIE")))),
     html.Br(),
     dbc.Row([ 
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=Recap_delai_sortie_jaune(dash_data,dash_data_1),style = {'height':'90px',})),html.H2('J')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=Recap_delai_sortie_Rouge(dash_data,dash_data_1),style = {'height':'90px',})),html.H2('J')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ), 
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=Recap_delai_sortie_Vert(dash_data,dash_data_1),style = {'height':'90px',})),html.H2('J')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),                
            ]) ,
            html.Br(),
         dbc.Row( html.H5(html.B(html.U("RATIO ET OBJECTIF")))), 
 dbc.Row([ 
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=RECAP_J6_RATIO(dash_data,dash_data_1),style = {'height':'90px',})),html.H3('%')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=RECAP_J2_RATIO(dash_data,dash_data_1),style = {'height':'90px',})),html.H3('%')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ), 
        dbc.Col(
            dbc.Card([
               dbc.CardBody(dcc.Graph(figure=RECAP_R2_RATIO(dash_data,dash_data_1),style = {'height':'90px',})),html.H3('%')
                    ]),xl=3,lg=3,md = 6,sm=6,xs =6
                ),                
            ])


],className="mt-3",fluid = True
)

tab3_content = dbc.Container([
    dbc.Row(html.H5(html.B(html.U("TAXES ")))),

            dbc.Row([               
                dbc.Col([

                    #html.P("VALEUR D'IMPORTATION", className="card-text"),
                    dbc.Card([
                                dbc.CardBody(dcc.Graph(figure=RECAP_VALEUR(dash_data,dash_data_1),style = {'height':'90px',}))
                            ])
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                    dbc.Col([

                    #html.P("VALEUR D'IMPORTATION", className="card-text"),
                    dbc.Card([
                                dbc.CardBody(dcc.Graph(figure=RECAP_FRANCHISE(dash_data,dash_data_1),style = {'height':'90px',}))
                            ])
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("TAXES LIQUIDEES", className="card-text"),
                    dbc.Card([
                                dbc.CardBody(dcc.Graph(figure=RECAP_TAXE(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])
                       ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("RATIO TAXATION", className="card-text"),
                    dbc.Card([
                               dbc.CardBody([
                                                dcc.Graph(figure=RECAP_TAX_RATIO(dash_data,dash_data_1),style = {'height':'90px',}),html.H6('%')
                                            ])
                             ])      
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                   ]) ,   
    
                #className="mt-3", 
           html.Br(),
           dbc.Row(html.H5(html.B(html.U("AUTRES INDICATEURS ")))),     
          dbc.Row([               
                dbc.Col([
                    #html.P("Volume Conteneur ", className="card-text"),
                    
                                dbc.Card(dbc.CardBody(dcc.Graph(figure=recap_ctn(dash_data,dash_data_1),style = {'height':'90px',})))
                            
                        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("TAXE MOYENNE EVP", className="card-text"),
                    dbc.Card([
                                dbc.CardBody(dcc.Graph(figure=RECAP_EVP(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])
                       ],xl=4,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("TAXE MOYENNE PAR DECLARATION", className="card-text"),
                    dbc.Card([
                               dbc.CardBody(dcc.Graph(figure=RECAP_TAX_DAU(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])      
                        ],xl=4,lg=6,md = 6,sm=12,xs = 12),
                   ]) ,
                   html.Br(),
                dbc.Row(html.H5(html.B(html.U("STRUCTURE TARIFAIRE")))),
                   dbc.Row([               
                dbc.Col([
                    #html.P(" Quotité 0 ", className="card-text"),
                    
                                dbc.Card(dbc.CardBody(dcc.Graph(figure=RECAP_0(dash_data,dash_data_1),style = {'height':'90px',})))
                            
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("Quotité 0-20", className="card-text"),
                    dbc.Card([
                                dbc.CardBody(dcc.Graph(figure=RECAP_0_20(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])
                       ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("Quotité 5-20", className="card-text"),
                    dbc.Card([
                               dbc.CardBody(dcc.Graph(figure=RECAP_5_20(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])      
                        ],xl=2,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("Quotité 10-20", className="card-text"),
                    dbc.Card([
                               dbc.CardBody(dcc.Graph(figure=RECAP_10_20(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])      
                        ],xl=2,lg=6,md = 6,sm=12,xs = 12),
                dbc.Col([
                    #html.P("Quotité 20-20", className="card-text"),
                    dbc.Card([
                               dbc.CardBody(dcc.Graph(figure=RECAP_20_20(dash_data,dash_data_1),style = {'height':'90px',}))
                             ])      
                        ],xl=2,lg=6,md = 6,sm=12,xs = 12),
                   ]) ,
                   html.Br(),
        dbc.Row(html.H5(html.B(html.U("RESUME GRAPHIQUE")))),        
          dbc.Row([
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=cours_devise(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=6,xs = 12),
                    dbc.Col([#html.P("Recettes", className="card-text"),
                             dcc.Graph(figure=Valeur(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=12,xs = 12),
                    dbc.Col([#html.P("Taxes liquidees", className="card-text"),
                             dcc.Graph(figure=Taxe_liq(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=12,xs = 12)
                  ]) , 
             dbc.Row([
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=rec_previsions(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=6,xs = 12),
                    dbc.Col([#html.P("Recettes", className="card-text"),
                             dcc.Graph(figure=EVP(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=12,xs = 12),
                    dbc.Col([#html.P("Taxes liquidees", className="card-text"),
                             dcc.Graph(figure=DAU(dash_data,dash_data_1))],xl=4,lg=4,md = 6,sm=12,xs = 12)
                  ]) ,  
                  dbc.Row([
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=structure_tarifaire(dash_data,dash_data_1))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=structure_tarifaire_bis(dash_data,dash_data_1))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                  ]) , 
                dbc.Row(html.H5(html.B(html.U("REGIME DE FRANCHISE")))),
                html.Br(),
                dbc.Row(dbc.Col([html.Div(id = 'dropdown-div', children =
             [dcc.Dropdown(id = 'franchise-dropdown',
                 options = [{'label':i, 'value':i} for i in np.append(['All'],tab_data['Nature'].unique()) ],
                 value = 'All',
                 placeholder = 'Nature franchise'
                 )], style = {'width':'100%', 'display':'inline-block'}),

                      html.Div(id = 'world-table-output')
                      ],style = {'height':'450px','text-align':'center'},xs = 12, sm = 12, md = 12, lg = 12, xl = 12))      
        ],fluid = True) 

tab4_content = dbc.Container([
    dbc.Row(html.H5(html.B(html.U("DOWNGRADE-UPGRADE")))),
    html.Br(),
    dbc.Row([
            dbc.Col([
            #html.P("TAUX DE DOWNGRADE", className="card-text"),
                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_DOWNGRADE_RATIO(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                    ],xl=4,lg=6,md = 6,sm=12,xs = 12),
            dbc.Col([
            #html.P("TAUX DE UPGRADE", className="card-text"),
                    dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_UPGRADE_RATIO(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                    ],xl=4,lg=6,md = 6,sm=12,xs = 12),
          dbc.Col([
            #html.P("TAUX DE SUSPICION CONFIRME", className="card-text"),
                    dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_SUSP_CONF(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                    ],xl=4,lg=6,md = 6,sm=12,xs = 12)
                    ,
            ]),
    html.Br(),
    dbc.Row(html.H5(html.B(html.U("SITUATION IVALUE")))),
    dbc.Row([
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE_REDR(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
        
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE_VAL(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                    dbc.Col([
            #html.P("TAUX D'APPLICATION I-VALUE", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE_REDR_VAL(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
        
                    ]
                   ),
                   html.Br(),
        dbc.Row([
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE_ALIGN(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_IVALUE_ALIGN_VAL(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
        
                    dbc.Col([
                                dbc.Card([dbc.CardBody(dcc.Graph(figure=Recap_appli_IVALUE(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
                    dbc.Col([
            #html.P("TAUX D'APPLICATION I-VALUE", className="card-text"),
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_DC_IVALUE(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
                            ],xl=3,lg=6,md = 6,sm=12,xs = 12),
        
                    ]
                   ),
                   html.Br(),
    dbc.Row(html.H5(html.B(html.U("DROITS COMPROMIS")))),
    dbc.Row(
 [  dbc.Col([
           
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_CTX(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
    dbc.Col([
           
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_CTX_J(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
        dbc.Col([
           
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_CTX_R(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
     
        dbc.Col([
           
            dbc.Card([dbc.CardBody(dcc.Graph(figure=RECAP_DC(dash_data,dash_data_1),style = {'height':'90px',}))]),
                 
        ],xl=3,lg=6,md = 6,sm=12,xs = 12),
          
           
        ]
    )],
    className="mt-3",fluid = True
)


tab5_content = dbc.Container([
    dbc.Row("Répartitions Déclarations"),
    dbc.Row([
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=DAU_ID(tab_ind))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                    dbc.Col([#html.P("Cours devise", className="card-text"),
                             dcc.Graph(figure=REAT(tab_ind))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                  ]) ,
    dbc.Row("Traitment des Déclarations"),
    dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=DELAI_JAUNE_IND(tab_ind))],xl=4,lg=4,md = 6,sm=6,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=DELAI_ROUGE_IND(tab_ind))],xl=4,lg=4,md = 6,sm=6,xs = 12),
                     dbc.Col(     
                             dcc.Graph(figure=DELAI_ROUGE_SCAN_IND(tab_ind)),xl=4,lg=4,md = 6,sm=6,xs = 12),
                             
             ]) ,   

     dbc.Row("Valeur et Taxes"), 
        dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=ASSI_TAX_IND(tab_ind))],xl=6,lg=12,md = 12,sm=12,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=TAX_RATIO_IND(tab_ind))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                     
                             
             ]) ,
      dbc.Row("Structure tarifaire"), 
         dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=struc_tar_0_ind(tab_ind))],xl=3,lg=12,md = 12,sm=12,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=struc_tar_0_20_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12),
                     
                    dbc.Col([
                             dcc.Graph(figure=struc_tar_5_20_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12), 
                    dbc.Col([
                             dcc.Graph(figure=struc_tar_10_20_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12), 
                    dbc.Col([
                             dcc.Graph(figure=struc_tar_20_20_ind(tab_ind))],xl=3,lg=12,md = 6,sm=6,xs = 12),                        
             ]) ,
        dbc.Row("Taxe Moyenne par EVP"), 
           dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=TAXE_EVP_ind(tab_ind))],xl=6,lg=12,md = 12,sm=12,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=DC_ind(tab_ind))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                     
                             
             ]) ,
        dbc.Row("Taux de suspects confirmés"), 
             dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=DAU_ROUGE_IND(tab_ind))],xl=6,lg=12,md = 12,sm=12,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=SUSP_ind(tab_ind))],xl=6,lg=4,md = 6,sm=6,xs = 12),
                     
                             
             ]) ,
             html.Br(),
        dbc.Row("Traitement dossiers IVALUE"), 
        dbc.Row([
                    dbc.Col([
                             dcc.Graph(figure=TOT_IVALUE_ind(tab_ind))],xl=3,lg=12,md = 12,sm=12,xs = 12),
                    dbc.Col([
                             dcc.Graph(figure=TOT_IVALUE_CTX_ind(tab_ind))],xl=3,lg=12,md = 6,sm=6,xs = 12),
                     
                    dbc.Col([
                             dcc.Graph(figure=YEL_IVALUE_CTX_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12), 
                    dbc.Col([
                             dcc.Graph(figure=RED_IVALUE_CTX_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12), 
                    dbc.Col([
                             dcc.Graph(figure=APPLIED_IVALUE_ind(tab_ind))],xl=2,lg=12,md = 6,sm=6,xs = 12),                        
             ]) ,

              ],className="mt-3",fluid = True)
         
        
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Volume de déclarations"),
        dbc.Tab(tab2_content, label="Délai de dédouanement"),
        dbc.Tab(tab3_content, label="Valeur et taxes", disabled=False
        ),
        dbc.Tab(tab4_content, label="Qualité de contrôle"),
        dbc.Tab(tab5_content, label="Revue par vérificateur"),
    ]
)

@app.callback(Output(component_id='world-table-output', component_property= 'children'),
              [Input(component_id='franchise-dropdown', component_property='value')])

def table_country(Nature):
    if Nature == 'All':
        df_final = tab_data
    else:
        df_final = tab_data.loc[tab_data['Nature'] == '{}'.format(Nature)]

    return dash_table.DataTable(
    data = df_final.to_dict('records'),
    columns = [{'id':c , 'name':c} for c in df_final[['Nature','Janvier','Février','Mars','Avril','Mai','Juin','Juillet']].columns],
    fixed_rows = {'headers':True},

    sort_action = 'native',

    style_table = {
                   'maxHeight':'450px'
                   },

    style_header = {'backgroundColor':'rgb(224,224,224)',
                    'fontWeight':'bold',
                    'border':'4px solid white',
                    'fontSize':'12px'
                    },

    style_data_conditional = [

              {
                'if': {'row_index': 'odd',
                       # 'column_id': 'ratio',
                       },
                'backgroundColor': 'rgb(240,240,240)',
                'fontSize':'12px',
                },

            {
                  'if': {'row_index': 'even'},
                  'backgroundColor': 'rgb(255, 255, 255)',
                'fontSize':'14px',

            }

        ],

    style_cell = {
        'textAlign':'left',
        'fontFamily':'Times New Roman',
        'border':'4px solid white',
        'width' :'20%',
        # 'whiteSpace':'normal',
        # 'overflow':'hidden',
        'textOverflow': 'ellipsis',



        }

    # style_data

  )



app.layout = html.Div(id ='parent', children = [navbar,tabs])
if __name__ == "__main__":
    app.run_server(debug='True')
