import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.colors import n_colors
from dash.dependencies import Input, Output, State
import pandas as pd
import redis
import json
import datetime as dt
import time
import requests
from typing import Tuple
import numpy as np

store = redis.Redis()


def map_value_to_RGB(value: float) -> Tuple[float, float, float]:
    # FIXME: Move those functions to some other module
    """Linear interpolation from sensor value to RGB color"""

    smallest, biggest = 0, 1023  # From doctor Zawadzki's documentation
    value_range = [smallest, biggest]

    # Mapping from white to green
    red_range = [255, 85]
    green_range = [255, 255]
    blue_range = [255, 85]

    r = np.interp(value, value_range, red_range)
    g = np.interp(value, value_range, green_range)
    b = np.interp(value, value_range, blue_range)

    return r, g, b


def create_RGB_string(rgb: Tuple[float, float, float]) -> str:
    """Create rgb string for Plotly"""

    value = ', '.join((str(c) for c in rgb))
    return f'rgb({value})'


def map_value_to_RGB_string(value: float) -> str:
    """Support function to join mapping value and converting to Ploty string"""

    return create_RGB_string(map_value_to_RGB(value))


def make_table(values, cell_colors=None):
    table = go.Figure(data=[go.Table(
        header=dict(values=[c.replace('_', ' ') for c in values.keys()],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=list(values.values()),
                   fill=dict(color=cell_colors))
    )])

    return table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Tabs(id="tabs", value='1', children=[
        dcc.Tab(label='Person one', value='1'),
        dcc.Tab(label='Person two', value='2'),
        dcc.Tab(label='Person three', value='3'),
        dcc.Tab(label='Person four', value='4'),
        dcc.Tab(label='Person five', value='5'),
        dcc.Tab(label='Person six', value='6'),
    ]),

    html.Div(id='tabs-content'),

    dcc.Graph(id='table'),

    html.Div(id='current_id', style={'display': 'none'}),

    dcc.Interval(id='interval-component',
                 interval=1*1000,
                 n_intervals=0)
])


@app.callback([Output('current_id', 'children'),
               Output('tabs-content', 'children')
               ],
              [Input('tabs', 'value')],
              [State('current_id', 'children')])
def render_tab(tab, current_id):

    # Tab value is in format "tab-1"
    print(tab, current_id)
    new_id = tab

    key = f'personData{new_id}'
    data = json.loads(store.lrange(key, 0, 0)[0])

    firstName, lastName, birthdate = data['firstname'], data['lastname'], data['birthdate']
    cont = f'{firstName} {lastName} {birthdate}'

    return new_id, html.Div([
        html.H3(str(cont))
    ])


@app.callback(Output('table', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [State('current_id', 'children')])
def update_table(n_intervals, current_id):
    if current_id == None:
        current_id = 1
    TABLE_SIZE = 20
    key = f'personData{current_id}'

    rawList = store.lrange(key, 0, TABLE_SIZE)
    data = [json.loads(d.decode()) for d in rawList]

    values = {'time': [], 'sensor_0': [], 'sensor_1': [],
              'sensor_2': [], 'sensor_3': [], 'sensor_4': [], 'sensor_5': []}

    for value in data:
        datetime = dt.datetime.fromtimestamp(value['timestamp'])
        values['time'].append(datetime.strftime("%m/%d/%Y, %H:%M:%S"))
        sensors = value['trace']['sensors']

        for s in sensors:
            id = s['id']
            key = f'sensor_{id}'
            values[key].append(s['value'])

    colors = {}
    for key in values.keys():
        if key == 'time':
            colors[key] = ['white'] * len(values[key])
        else:
            colors[key] = [map_value_to_RGB_string(v) for v in values[key]]

    return make_table(values, list(colors.values()))


if __name__ == '__main__':
    app.run_server(debug=True)
