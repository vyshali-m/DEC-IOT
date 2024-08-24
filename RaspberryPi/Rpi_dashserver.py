import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
#import psycopg2
from sqlalchemy import create_engine
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

DATABASE_URL = "postgresql://postgres.gxvqfyitftgzusocnxvo:Supabase2024$@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
# Create a connection pool
engine = create_engine(DATABASE_URL)

def get_data():
    with engine.connect() as conn:
        query = "SELECT * FROM rpi_iot_data ORDER BY devicetimestamp DESC LIMIT 100;"
        df = pd.read_sql_query(query, conn)
    return df


# def get_data():
#     conn = psycopg2.connect(DATABASE_URL)
#     query = "SELECT * FROM iot_data ORDER BY devicetimestamp DESC LIMIT 100;"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# app.layout = html.Div([
#     dcc.Interval(
#         id='interval-component',
#         interval=10*1000,  # Refresh every 10 seconds
#         n_intervals=0
#     ),
#     dcc.Graph(id='memory-usage'),
#     dcc.Graph(id='network-traffic'),
#     dcc.Graph(id='cpu_temperature')
# ])

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # Refresh every 5 seconds
        n_intervals=0
    ),
    html.Div([
        html.Div(dcc.Graph(id='cpu-usage'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='free-memory'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='packets-recv'), style={'width': '33%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='err-in'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='drop-in'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='cpu_temperature'), style={'width': '33%', 'display': 'inline-block'}),
    ], style={'display': 'flex'})
])

@app.callback(
    [Output('cpu-usage', 'figure'),
     Output('free-memory', 'figure'),
     Output('packets-recv', 'figure'),
     Output('err-in', 'figure'),
     Output('drop-in', 'figure'),
     Output('cpu_temperature', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    df = get_data()
    return (
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['cpusage'], mode='lines', name='cpusage')],
            layout=go.Layout(title='Free Heap Memory', xaxis_title='devicetimestamp', yaxis_title='cpusage (%)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['freememory'], mode='lines', name='freememory')],
            layout=go.Layout(title='Network Traffic Volume', xaxis_title='devicetimestamp', yaxis_title='freememory (%)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['packetsrecv'], mode='lines', name='packetsrecv')],
            layout=go.Layout(title='Power Consumption', xaxis_title='devicetimestamp', yaxis_title='packetsrecv (count)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['errin'], mode='lines', name='errin')],
            layout=go.Layout(title='Response Time', xaxis_title='devicetimestamp', yaxis_title='errin (count)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['dropin'], mode='lines', name='dropin')],
            layout=go.Layout(title='Error Rate', xaxis_title='devicetimestamp', yaxis_title='dropin (count)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['devicetimestamp'], y=df['cputemperature'], mode='lines', name='Cpu Temperature')],
            layout=go.Layout(title='Packet Size', xaxis_title='devicetimestamp', yaxis_title='cputemperature (Celsius)')
        )
    )

# @app.callback(
#     [Output('memory-usage', 'figure'),
#      Output('network-traffic', 'figure'),
#      Output('cpu_temperature', 'figure')],
#     [Input('interval-component', 'n_intervals')]
# )

# def update_graph(n):
#     df = get_data()
#     return (
#         go.Figure(data=[go.Scatter(x=df['devicetimestamp'], y=df['cpusage'], mode='lines', name='Free Heap Memory')]),
#         go.Figure(data=[go.Scatter(x=df['devicetimestamp'], y=df['networktrafficvolume'], mode='lines', name='Network Traffic Volume')]),
#         go.Figure(data=[go.Scatter(x=df['devicetimestamp'], y=df['powerconsumption'], mode='lines', name='Power Consumption')])
#     )

if __name__ == '__main__':
    app.run_server(debug=True)

# python dash_server_devicetimestamp.py