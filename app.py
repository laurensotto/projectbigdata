import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv("datacleaning/covid_land.csv", sep=";")

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
                dbc.NavLink("Bedden", href="/pagina-1", active="exact"),
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
            dcc.Graph(figure=px.line(df, x='Date_of_publication', y=['Total_reported'],)),
            dcc.Graph(figure=px.line(df, x='Date_of_publication', y=['Deceased'], ))
        ]
    elif pathname == "/pagina-1":
        reported_fig = px.line(df, x='Date_of_publication', y=['Total_reported', 'IC_Bedden_COVID_Nederland', 'Kliniek_Bedden_Nederland'])
        reported_fig.update_yaxes(range=[0, 50000])
        return [
            html.H1('Coronacijfers vs. Bedden',
                    style={'textAlign': 'center'}),
            dcc.Graph(figure=reported_fig),
            dcc.Graph(figure=px.line(df, x='Date_of_publication', y=['Deceased', 'IC_Bedden_COVID_Nederland', 'Kliniek_Bedden_Nederland']))
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
