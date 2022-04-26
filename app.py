import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# TODO
# df = hier een csv inladen

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#086c9c",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(src='./assets/download.jpeg'),
        html.Hr(),
        html.P(
            "Coronadashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Algemeen", href="/", active="exact"),
                dbc.NavLink("Pagina 1", href="/pagina-1", active="exact"),
                dbc.NavLink("Pagina 2", href="/pagina-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('Coronacijfers sinds 2020',
                    style={'textAlign': 'center'}),
            # todo Doe hier iets met dcc.Graph om een graph te importeren
            # dcc.Graph(id='bargraph',
            #           figure=px.bar(df, barmode='group', x='Years',
            #                         y=['Coronacijfers']))
        ]
    elif pathname == "/pagina-1":
        return [
            html.H1('Pagina 1 met coronacijfers',
                    style={'textAlign': 'center'}),
            # todo Doe hier iets met dcc.Graph om een graph te importeren
        ]
    elif pathname == "/pagina-2":
        return [
            html.H1('Pagina 2 met coronacijfers',
                    style={'textAlign': 'center'}),
            # todo Doe hier iets met dcc.Graph om een graph te importeren
        ]
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
