import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import n_colors


import redis
import json
import datetime as dt
import time
import requests
from typing import Tuple
import pandas as pd
import numpy as np
from itertools import repeat
# Custom component
from feet_animation import FeetAnimation

REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
store = redis.Redis(REDIS_HOST)


def map_value_to_RGB(value: float) -> Tuple[float, float, float]:
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
    table = go.Figure(
        layout=dict(
            title=dict(
                text='Sensor values over last period',
                font=dict(
                    size=30,
                    color='black'
                )
            )
        ),
        data=[
            go.Table(
                header=dict(values=[c.replace('_', ' ') for c in values.keys()],
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=list(values.values()),
                           fill=dict(color=cell_colors))
            )]
    )

    return table


def make_anomaly_histogram(transformed):
    fig = go.Figure(
        data=[go.Histogram(x=transformed['time'])])
    return fig


def make_foot_pressure_indicator(sensor_number, value, previous_value=None) -> dict:
    """Create figure of analog meter displaying value of singe pressure sensor"""

    return dict(
        data=[
            dict(
                type='indicator',
                mode='number+delta+gauge',
                title=f'Foot pressure sensor {sensor_number}',
                value=value,
                delta=dict(reference=previous_value, relative=False),
                gauge=dict(
                    axis=dict(visible=True, range=[0, 1023])
                ),
                # domain=dict(x=[0, .6])
            )
        ],
        layout=dict(width=500, height=370)
    )


external_scripts = ['https://kit.fontawesome.com/620ce16426.js']
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], external_scripts=external_scripts)

app.layout = html.Div(
    className='wrapper',
    children=[
        # Store current person id
        dcc.Store(id='current-id', storage_type='session'),
        # Store last anomaly
        dcc.Store(id='last-anomaly'),

        dcc.Interval(id='interval-component',
                     interval=1*1000,
                     n_intervals=0),

        html.Nav(className='navbar navbar-dark bg-primary',
                 children=[
                     html.A(className='navbar-brand', children=[
                         html.I(className='fas fa-shoe-prints fa-rotate-270 mr-1'),
                         'Magic feet'
                     ]),
                     html.A(className='nav-item', style={'color': 'white'}, href='https://github.com/SiwyKrzysiek/magic-foots', children=[
                         'See it on Github',
                         html.I(className='fab fa-github ml-1'),
                     ])
                 ]
                 ),

        html.Main(className='container-fluid mb-4', children=[

            # Project description
            html.Section(className='text-center my-4', children=[
                html.H3(
                    'Final project for Python programming and data visualization'),
                html.Div(
                    [
                        dbc.Button(
                            ['More info', html.I(
                                className='ml-2 fas fa-info-circle')],
                            id='collapse-button',
                            className='mb-3',
                            color='info'
                        ),
                        dbc.Collapse(
                            dbc.Card(dbc.CardBody(
                                'This project attempts to visualize data gathered live from pressure sensors placed on feet of 6 participants.')),
                            id='collapse',
                        ),
                    ],
                    className='my-3'
                )
            ]
            ),

            # Select person
            dcc.Tabs(id="tabs", className='nav-item', value='1', children=[
                dcc.Tab(label='Person one', value='1'),
                dcc.Tab(label='Person two', value='2'),
                dcc.Tab(label='Person three', value='3'),
                dcc.Tab(label='Person four', value='4'),
                dcc.Tab(label='Person five', value='5'),
                dcc.Tab(label='Person six', value='6'),
            ]),

            html.Section(className='tabs-content', children=[

                # Person name
                html.H1(className='display-4', children=[
                        html.I(className='fas fa-user-circle mr-2'),
                        html.Span(id='person-name')
                        ]),

                html.Section(className='shadow bg-white rounded mt-5', children=[
                    dcc.Graph(id='table', className='table-light'),
                ]),

                dbc.Row(justify="center", align="center", children=[
                    dbc.Col(className='shadow bg-white rounded', children=[
                        html.H4('Sensor placement',
                                className='text-center py-3'),
                        FeetAnimation(id='feet-animation')
                    ]),

                    dbc.Col(
                        html.Div(id='single-sensor-container', className='sensor', children=[  # Display single selected sensor
                            dcc.Tabs(id='single-sensor-tabs', value='1',
                                     children=[dcc.Tab(label=str(i), value=str(i), className='single-sensor-tab') for i in range(0, 6)]),
                            dcc.Graph(id='singe-sensor-indicator')
                        ])
                    )
                ]
                ),

                html.Section(className='shadow bg-white rounded container-fluid pt-3', children=[
                    html.H3('Anomaly accumulation histogram'),
                    html.Div(id='last_anomaly_mess'),
                    dcc.Graph(id='anomaly_graph', className='anomaly_graph')
                ]),
            ]),

        ]),

        html.Footer(className='footer', children=[
            html.H1('PW EE'),
            html.P('© 2020', className='mb-1'),
            html.P('Authors: Mara Kruk and Krzysztof Dąbrowski', className='mb-0')
        ])
    ])


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



@app.callback([Output('last_anomaly_mess', 'children'),
              Output('last_anomaly_mess', 'style')],
              [Input('last-anomaly', 'modified_timestamp')],
              [State('last-anomaly', 'data')])
def update_last_anomaly(ts, data):
    if ts is None:
        PreventUpdate

    data = data or {'time': None, 'sensor': None}
    time_d = data['time']
    if time_d == None:
       return "", {'display': 'hidden'}   
    
    sensor = data['sensor']
    label = f'Last anomaly was {time_d} at sensors {sensor}'
    return label, {}

@app.callback([Output('current-id', 'data'),
               Output('person-name', 'children')
               ],
              [Input('tabs', 'value')])
def on_person_tab_change(new_id):
    key = f'personData{new_id}'
    preson = json.loads(store.lrange(key, 0, 0)[0])

    firstName, lastName, birthdate = preson['firstname'], preson['lastname'], preson['birthdate']
    person_description = f'{firstName} {lastName} {birthdate}'

    return (
        new_id,
        person_description
    )


@app.callback([Output('anomaly_graph', 'figure'),
               Output('last-anomaly', 'data')],
              [Input('interval-component', 'n_intervals'),
               Input('current-id', 'data')],
               [State('last-anomaly', 'data')])
def update_anomaly_histogram(n_intervals, current_id, last_anomaly_data):

    if current_id is None:
        raise PreventUpdate

    key = f'personData{current_id}'
    rawList = store.lrange(key, 0, -1) # -1 is the last element
    data = [json.loads(d.decode()) for d in rawList]

    last_anomaly_data = {'time': None, 'sensor': None}
    transformed = {'time': []}
    latest_anomalies = None

    for record in data:
        time = dt.datetime.fromtimestamp(record['timestamp'])
        anomalies = sum((s['anomaly'] for s in record['trace']['sensors']))
        if anomalies > 0 and (latest_anomalies is None or latest_anomalies['time'] < time):
            latest_anomalies = {
                'data': record['trace']['sensors'], 'time': time}
        transformed['time'].extend(repeat(time, anomalies))

    if latest_anomalies is not None:
        abnormal_sensors = (s['id']
                            for s in latest_anomalies['data'] if s['anomaly'])
        sensors_message = ' ,'.join((f'Sensor {i}' for i in abnormal_sensors))
        last_anomaly_data = {
            'time': latest_anomalies['time'].strftime("%m/%d/%Y, %H:%M:%S"), 
            'sensor': sensors_message
        }

    return make_anomaly_histogram(transformed), last_anomaly_data


@app.callback(Output('feet-animation', 'sensorValues'),
              [Input('interval-component', 'n_intervals'),
               Input('current-id', 'data')])
def update_feet_animation(_, current_id):
    if current_id is None:
        raise PreventUpdate

    key = f'personData{current_id}'
    rawList = store.lrange(key, 0, 0)
    data = [json.loads(d.decode()) for d in rawList][0]

    values = [sensor['value'] for sensor in data['trace']['sensors']]

    return values


@app.callback(Output('table', 'figure'),
              [Input('interval-component', 'n_intervals'),
               Input('current-id', 'data')],)
def update_table(n_intervals, current_id):
    if current_id is None:
        raise PreventUpdate

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


@app.callback(Output('singe-sensor-indicator', 'figure'),
              [Input('interval-component', 'n_intervals'),
               Input('single-sensor-tabs', 'value'),
               Input('current-id', 'data')])
def update_singe_sensor_indicator(_, selected_sensor, current_id):
    if current_id is None or selected_sensor is None:
        raise PreventUpdate

    key = f'personData{current_id}'
    rawList = store.lrange(key, 0, 1)
    data = [json.loads(d.decode()) for d in rawList]

    values = (value['trace']['sensors'][int(selected_sensor)]['value']
              for value in data)

    return make_foot_pressure_indicator(selected_sensor, *values)


if __name__ == '__main__':
    debug = False if os.environ.get('PRODUCTION') == 'true' else True
    app.run_server(debug=debug, host='0.0.0.0')
