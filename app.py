# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import json
import ast
import plotly.graph_objs as go
import datetime
import flask

import math
import datetime
import statistics

from scipy.stats import nbinom
import matplotlib.pyplot as plt
import numpy as np
from itertools import groupby

import plotly.graph_objects as go
from plotly.offline import plot, iplot

from utils import *
from unit_test_gamestat import game_stat_test

sj = pd.read_csv("data/SanJoseSpiders2019-stats.csv")
sea = pd.read_csv("data/SeattleCascades2019-stats.csv")
la = pd.read_csv("data/LosAngelesAviators2019-stats.csv")
sd = pd.read_csv("data/SanDiegoGrowlers2019-stats.csv")

atl = pd.read_csv("data/AtlantaHustle2019-stats.csv")
aus = pd.read_csv("data/AustinSol2019-stats.csv")
dal = pd.read_csv("data/DallasRoughnecks2019-stats.csv")
ral = pd.read_csv("data/RaleighFlyers2019-stats.csv")
tb = pd.read_csv("data/TampaBayCannons2019-stats.csv")
ind = pd.read_csv("data/IndianapolisAlleyCats2019-stats.csv")

chi = pd.read_csv("data/ChicagoWildfire2019-stats.csv")
mad = pd.read_csv("data/MadisonRadicals2019-stats.csv")
mn = pd.read_csv("data/MinnesotaWindChill2019-stats.csv")
pit = pd.read_csv("data/PittsburghThunderbirds2019-stats.csv")
det = pd.read_csv("data/DetroitMechanix2019-stats.csv")

dc = pd.read_csv("data/DCBreeze2019-stats.csv")
phi = pd.read_csv("data/PhiladelphiaPhoenix2019-stats.csv")
ny = pd.read_csv("data/NewYorkEmpire2019-stats.csv")
tor = pd.read_csv("data/TorontoRush2019-stats.csv")
ott = pd.read_csv("data/OttawaOutlaws2019-stats.csv")
mon = pd.read_csv("data/MontrealRoyal2019-stats.csv")

teams_list = ["San Jose Spiders",
              "Seattle Cascades",
              "Los Angeles Aviators",
              "San Diego Growlers",
              "Atlanta Hustle",
              "Austin Sol",
              "Dallas Roughnecks",
              "Raleigh Flyers",
              "Tampa Bay Cannons",
              "Indianapolis AlleyCats",
              "Chicago Wildfire",
              "Madison Radicals",
              "Minnesota Wind Chill",
              "Pittsburgh Thunderbirds",
              "Detroit Mechanix",
              "DC Breeze",
              "Philadelphia Phoenix",
              "New York Empire",
              "Toronto Rush",
              "Ottawa Outlaws",
              "Montreal Royal"]

teams_dict = {"San Jose Spiders":sj,
              "Seattle Cascades":sea,
              "Los Angeles Aviators":la,
              "San Diego Growlers":sd,
              "Atlanta Hustle":atl,
              "Austin Sol":aus,
              "Dallas Roughnecks":dal,
              "Raleigh Flyers":ral,
              "Tampa Bay Cannons":tb,
              "Indianapolis AlleyCats":ind,
              "Chicago Wildfire":chi,
              "Madison Radicals":mad,
              "Minnesota Wind Chill":mn,
              "Pittsburgh Thunderbirds":pit,
              "Detroit Mechanix":det,
              "DC Breeze":dc,
              "Philadelphia Phoenix":phi,
              "New York Empire":ny,
              "Toronto Rush":tor,
              "Ottawa Outlaws":ott,
              "Montreal Royal":mon
             }

teams_col_dict = {"San Jose Spiders":'gold',
              "Seattle Cascades":'midnightblue',
              "Los Angeles Aviators":'crimson',
              "San Diego Growlers":'black',
              "Atlanta Hustle":'indigo',
              "Austin Sol":'blue',
              "Dallas Roughnecks":'whitesmoke',
              "Raleigh Flyers":'red',
              "Tampa Bay Cannons":'yellow',
              "Indianapolis AlleyCats":'darkgreen',
              "Chicago Wildfire":'orangered',
              "Madison Radicals":'goldenrod',
              "Minnesota Wind Chill":'lightsteelblue',
              "Pittsburgh Thunderbirds":'orange',
              "Detroit Mechanix":'maroon',
              "DC Breeze":'navy',
              "Philadelphia Phoenix":'firebrick',
              "New York Empire":'limegreen',
              "Toronto Rush":'tomato',
              "Ottawa Outlaws":'olivedrab',
              "Montreal Royal":'royalblue'
             }

external_stylesheets = ["https://codepen.io/amyoshino/pen/jzXypZ.css"]

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID], server=server)

game_dict, df_stats = get_game_stats(team_dict=teams_dict)
season_turnovers = get_season_total_turnovers(df_stats,teams_list)
bxplt = plot_turnovers(df_stats,teams_list,teams_col_dict,sort_by='offense')
brplt = plot_goals(teams_list,df_stats,teams_col_dict)

### Body of Dashboard
body = dbc.Container(
    [
        #dbc.Row(html.Img(src = app.get_asset_url('IMAGE.png'),style={'height':'25%', 'width':'25%'} )),
        
        dbc.Row(
            html.Div(
                                        html.H1("American Ultimate Disc League - Analytics",
                                            style={
                                                    'font-family': 'Arial, san-serif',
                                                    'textAlign':'center',
                                                    'color':'black',
                                            }
                                        )
                                    )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='plot_1', figure=bxplt, config={'displayModeBar': False})
                    ]
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='plot_2', figure=brplt, config={'displayModeBar': False})
                    ]
                )
            ]
        )

    ]
)

app.layout = html.Div([body],style={'border':'4px black solid','backgroundColor':'white'})

#@app.callback([ 
#                Output('vertical_bar', 'clickData') ],
#              [
#                Input( 'button_chart', 'n_clicks') ])
#def update_global_var(clicks):
#    return([None])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)