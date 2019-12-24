import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.colors import n_colors
from dash.dependencies import Input, Output
import pandas as pd
import redis
import json
import datetime as dt
import time
import requests
store = redis.Redis()

current_id = 1
if_changed = False


def make_table(df):
    table = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[c] for c in df.columns])
    )])

    return table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Person one', value='tab-1'),
        dcc.Tab(label='Person two', value='tab-2'),
        dcc.Tab(label='Person three', value='tab-3'),
        dcc.Tab(label='Person four', value='tab-4'),
        dcc.Tab(label='Person five', value='tab-5'),
        dcc.Tab(label='Person six', value='tab-6'),
    ]),

    html.Div(id='tabs-content'),

    dcc.Graph(id='table'),

    dcc.Interval(id='interval-component',
                 interval=1*1000,
                 n_intervals=0)
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_tab(tab):

    # Tab value is in format "tab-1"
    current_id = int(tab[-1])

    key = f'personData{current_id}'
    data = json.loads(store.lrange(key, 0, 0)[0])

    firstName, lastName, birthdate = data['firstname'], data['lastname'], data['birthdate']
    cont = f'{firstName} {lastName} {birthdate}'

    return html.Div([
        html.H3(str(cont))
    ])


@app.callback(Output('table', 'figure'), [Input('interval-component', 'n_intervals')])
def update_table(n_intervals):
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

    df = pd.DataFrame(values)
    return make_table(df)


if __name__ == '__main__':
    app.run_server(debug=True)
