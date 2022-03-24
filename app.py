import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd

# Read in the USA counties shape files
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

########### Define a few variables ######
state = "New York"

tabtitle = f'{state} Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/amakarewycz/dash-virginia-counties'
varlist=['TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'RUCC_2013']

varlist=['CountyId', 'State', 'County', 'TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment']

#df=pd.read_pickle('resources/va-stats.pkl')
df=pd.read_csv('resources/acs2017_county_data.csv')
df=df[df['State']=="New York"]

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1(f'{state} Census Data 2017'),
            html.Div(children=[
            html.Div([
                html.H6('Select census variable:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='MeanCommute'
                ),
                ], className='three columns'),
                html.Br(),
                html.A('Code on Github', href=githublink),
                html.Br(),
                html.A("Data Source", href=sourceurl),],
                className='nine columns'),
    # Dropdownsa
            html.Div([
              dcc.Graph(id='va-map')
            ], className='nine columns')
    # Footer
    ]
)

############ Callbacks
@app.callback(Output('va-map', 'figure'),
              [Input('stats-drop', 'value')])
def display_results(selected_value):
    valmin=df[selected_value].min()
    valmax=df[selected_value].max()
    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                    locations=df['CountyId'],
                                    z=df[selected_value],
                                    colorscale='Blues',
                                    text=df['County'],
                                    zmin=valmin,
                                    zmax=valmax,
                                    marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.8,
                      mapbox_center = {"lat": 43.29, "lon": -73.93})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
