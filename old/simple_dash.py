from dash import Dash, dcc, html
import plotly.graph_objs as go

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Hello Dash"),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scatter(
                    x=[1, 2, 3],
                    y=[4, 1, 2],
                    mode='lines+markers'
                )
            ],
            'layout': go.Layout(
                title='Simple Graph'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
