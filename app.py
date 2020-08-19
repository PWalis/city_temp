import dash
import flask
import dash_bootstrap_components as dbc
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd 
from python.postgres_db.pg_database import database as db

# assigning df to object variable data 
data_object = db()

region_country, country_city, state_city = data_object.get_dict()

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/cyborg/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Temperature Data'
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('About', href='#vis')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem([html.I(className='linkedin'), ' LinkedIn'], href='https://www.linkedin.com/in/patrick-wilky/', target='_blank'),
                dbc.DropdownMenuItem([html.I(className='github'), ' GitHub'], href='https://github.com/PWalis/city_temp', target='_blank'),
            ],
            nav=True,
            in_navbar=True,
            label="Links",
        ),
    ],
    brand="Data Visualizer",
    brand_href="#",
    color="#343187",
    dark=True,
)

graph = html.Div([
    dcc.Graph(id='temp_graph'),
])

inputs = dbc.Row([
    dbc.Col(
        dbc.FormGroup([
            dbc.Label('Region', html_for='filter-region'),
            dcc.Dropdown(id='dropdown_region', options=[{'label':x, 'value':x} for x in region_country.keys()], value='North America')
        ]),
        width=3,
    ),
    dbc.Col(
        dbc.FormGroup([
            dbc.Label('Country', html_for='filter-country'),
            dcc.Dropdown(id='dropdown_country')
        ]),
        width=3,
    ),
    dbc.Col(
        dbc.FormGroup([
            dbc.Label('State', html_for='filter-state'),
            dcc.Dropdown(id='dropdown_state')
        ]),
        width=3,
    ),
    dbc.Col(
        dbc.FormGroup([
            dbc.Label('City', html_for='filter-city'),
            dcc.Dropdown(id='dropdown_city')
        ]),
        width=3,
    ),
],
form=True,)

card = html.Div(id='stats_card')

app.layout = dbc.Container(fluid=True, children=[
    navbar,
    inputs,
    graph,
    card,
    ])

@app.callback(
    Output('dropdown_country', 'options'),
    [Input('dropdown_region', 'value')]
)
def update_country_drop(selected_region):
    return [{'label':x, 'value':x} for x in region_country.get(selected_region)]

@app.callback(
    Output('dropdown_state', 'options'),
    [Input('dropdown_country', 'value')]
)
def update_state_drop(selected_country):
    if selected_country == 'US':
        return [{'label':x, 'value':x} for x in country_city.get(selected_country)]
    else:
        return [{'label':'None', 'value':'None'}]

@app.callback(
    Output('dropdown_city', 'options'),
    [Input('dropdown_country', 'value'),
     Input('dropdown_state', 'value')]
)
def update_city_drop(selected_country, selected_state):
    if selected_country and selected_state is not None:
        if selected_country != 'US':
            return [{'label':x, 'value':x} for x in country_city.get(selected_country)]
        elif selected_country == 'US' and selected_state != None:
            return [{'label':x, 'value':x} for x in state_city.get(selected_state)]
    else:
        return [{'label':'None', 'value':'None'}]


    
@app.callback(
    Output('stats_card', 'children'),
    [Input('dropdown_region', 'value'),
     Input('dropdown_country', 'value'),
     Input('dropdown_state', 'value'),
     Input('dropdown_city', 'value')]
)
def update_card(region, country, state, city):
    if city != None:
        count, minimum, maximum = data_object.get_stats(region, country, state, city)
        card = dbc.Row([
            dbc.Col(
                dbc.Card(body=True, className='stats-card', children=[
                    html.H5('Data Points'),
                    html.H5('{:,.0f}'.format(count), style={'color':'white'}), 
                ])
            ),
            dbc.Col(
                dbc.Card(body=True, className='stats-card', children=[
                    html.H5('Coldest Day'),
                    html.H5(minimum, style={'color':'white'}), 
                ])
            ),
            dbc.Col(
                dbc.Card(body=True, className='stats-card', children=[
                    html.H5('Hottest Day'),
                    html.H5(maximum, style={'color':'white'}), 
                ])
            )
        ])
        return card
    
@app.callback(
    Output('temp_graph', 'figure'),
    [Input('dropdown_region', 'value'),
     Input('dropdown_country', 'value'),
     Input('dropdown_state', 'value'),
     Input('dropdown_city', 'value')]
)
def update_graph(region, country, state, city):
    if city != None:
        return data_object.filter(region, country, state, city)
    else:
        return data_object.filter('None', 'None', 'None', 'None')
        
if __name__ == '__main__':
    app.server.run(debug=False)