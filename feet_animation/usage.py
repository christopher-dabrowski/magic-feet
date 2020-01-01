import feet_animation
import dash
import dash_html_components as html

app = dash.Dash(__name__)

sensor_values_mock = [896, 568, 708, 23, 0, 5]

app.layout = html.Div([
    feet_animation.FeetAnimation(
        id='input',
        sensorValues=sensor_values_mock
    ),
    html.Div(id='output')
])


if __name__ == '__main__':
    app.run_server(debug=True)
