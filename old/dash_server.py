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
        query = "SELECT * FROM iot_data ORDER BY device_timestamp DESC LIMIT 100;"
        df = pd.read_sql_query(query, conn)
    return df


# def get_data():
#     conn = psycopg2.connect(DATABASE_URL)
#     query = "SELECT * FROM iot_data ORDER BY device_timestamp DESC LIMIT 100;"
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
#     dcc.Graph(id='power-consumption')
# ])

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # Refresh every 2 seconds
        n_intervals=0
    ),
    html.Div([
        html.Div(dcc.Graph(id='free-heap-memory'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='network-traffic-volume'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='packet-size'), style={'width': '33%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='response-time'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='error-rate'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='power-consumption'), style={'width': '33%', 'display': 'inline-block'}),
    ], style={'display': 'flex'})
])

@app.callback(
    [Output('free-heap-memory', 'figure'),
     Output('network-traffic-volume', 'figure'),
     Output('packet-size', 'figure'),
     Output('response-time', 'figure'),
     Output('error-rate', 'figure'),
     Output('power-consumption', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    df = get_data()
    return (
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['freeheapmemory'], mode='lines', name='Free Heap Memory')],
            layout=go.Layout(title='Free Heap Memory', xaxis_title='device_timestamp', yaxis_title='Memory (Bytes)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['networktrafficvolume'], mode='lines', name='Network Traffic Volume')],
            layout=go.Layout(title='Network Traffic Volume', xaxis_title='device_timestamp', yaxis_title='Traffic Volume (Bytes)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['packetsize'], mode='lines', name='Packet Size')],
            layout=go.Layout(title='Packet Size', xaxis_title='device_timestamp', yaxis_title='Packet Size (Bytes)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['responsetime'], mode='lines', name='Response Time')],
            layout=go.Layout(title='Response Time', xaxis_title='device_timestamp', yaxis_title='Response Time (ms)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['errorrate'], mode='lines', name='Error Rate')],
            layout=go.Layout(title='Error Rate', xaxis_title='device_timestamp', yaxis_title='Error Rate (%)')
        ),
        go.Figure(
            data=[go.Scatter(x=df['device_timestamp'], y=df['powerconsumption'], mode='lines', name='Power Consumption')],
            layout=go.Layout(title='Power Consumption', xaxis_title='device_timestamp', yaxis_title='Power Consumption (Watts)')
        )
    )

# @app.callback(
#     [Output('memory-usage', 'figure'),
#      Output('network-traffic', 'figure'),
#      Output('power-consumption', 'figure')],
#     [Input('interval-component', 'n_intervals')]
# )

# def update_graph(n):
#     df = get_data()
#     return (
#         go.Figure(data=[go.Scatter(x=df['device_timestamp'], y=df['freeheapmemory'], mode='lines', name='Free Heap Memory')]),
#         go.Figure(data=[go.Scatter(x=df['device_timestamp'], y=df['networktrafficvolume'], mode='lines', name='Network Traffic Volume')]),
#         go.Figure(data=[go.Scatter(x=df['device_timestamp'], y=df['powerconsumption'], mode='lines', name='Power Consumption')])
#     )

if __name__ == '__main__':
    app.run_server(debug=True)
