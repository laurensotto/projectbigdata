import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv("datacleaning/covid_land.csv", sep=";")
df_zorg = pd.read_csv("datacleaning/zorg_fixed.csv", sep=";")

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
                dbc.NavLink("Bedden", href="/bedden-bezet-absolute", active="exact"),
                dbc.NavLink("Uitgaven", href="/uitgaven-absolute", active="exact"),
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
        figureCases = px.line(
            df,
            x='Datum publicatie',
            y=["Aantal besmettingen VK",
               "Aantal besmettingen NL",
               ],
        )
        figureCases.update_layout(
            yaxis_title="Aantal besmettingen",
            xaxis_title="Datum",
            legend_title="Land",
        )
        figureCases.update_yaxes(range=[0, 250000])
        figureDeaths = px.line(
            df,
            x='Datum publicatie',
            y=["Aantal doden VK",
               "Aantal doden NL",
               ],
        )
        figureDeaths.update_layout(
            yaxis_title="Aantal sterftes",
            xaxis_title="Datum",
            legend_title="Land",
        )
        return [
            html.H1('Coronacijfers sinds 2020',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Algemeen (Absoluut)", href="/", active="exact"),
                    dbc.NavLink("Algemeen (Relatief)", href="/relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureCases),
            dcc.Graph(figure=figureDeaths),
        ]
    elif pathname == "/relative":
        figureCases = px.line(
            df,
            x='Datum publicatie',
            y=["Aantal besmettingen VK per 100.000 inwoners",
               "Aantal besmettingen NL per 100.000 inwoners",
               ],
        )
        figureCases.update_layout(
            yaxis_title="Aantal besmettingen per 100.000 inwoners",
            xaxis_title="Datum",
            legend_title="Land",
        )
        figureCases.update_yaxes(range=[0, 600])
        figureDeaths = px.line(
            df,
            x='Datum publicatie',
            y=["Aantal doden VK per 100.000 inwoners",
               "Aantal doden NL per 100.000 inwoners",
               ],
        )
        figureDeaths.update_layout(
            yaxis_title="Aantal sterftes per 100.000 inwoners",
            xaxis_title="Datum",
            legend_title="Land",
        )
        return [
            html.H1('Coronacijfers sinds 2020',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Algemeen (Absoluut)", href="/", active="exact"),
                    dbc.NavLink("Algemeen (Relatief)", href="/relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureCases),
            dcc.Graph(figure=figureDeaths),
        ]
    elif pathname == "/bedden-bezet-absolute":
        figureICBeds = px.line(
            df,
            x='Datum publicatie',
            y=["IC-bedden VK bezet",
               "IC-bedden NL bezet",
               ],
        )
        figureICBeds.update_layout(
            yaxis_title="Aantal IC-bedden bezet",
            xaxis_title="Datum",
            legend_title="Land",
        )
        figureBeds = px.line(
            df,
            x='Datum publicatie',
            y=["Ziekenhuisbedden VK bezet",
               "Ziekenhuisbedden NL bezet",
               ],
        )
        figureBeds.update_layout(
            yaxis_title="Aantal Ziekenhuisbedden bezet",
            xaxis_title="Datum",
            legend_title="Land",
        )
        return [
            html.H1('Bedden in het ziekenhuis',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Bezet (Absoluut)", href="/bedden-bezet-absolute", active="exact"),
                    dbc.NavLink("Bezet (Relatief)", href="/bedden-bezet-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Beschikbaar (Absoluut)", href="/bedden-beschikbaar-absolute", active="exact"),
                    dbc.NavLink("Beschikbaar (Relatief)", href="/bedden-beschikbaar-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureICBeds),
            dcc.Graph(figure=figureBeds),
        ]
    elif pathname == "/bedden-bezet-relative":
        figureICBeds = px.line(
            df,
            x='Datum publicatie',
            y=["IC-bedden VK bezet per 100.000 inwoners",
               "IC-bedden NL bezet per 100.000 inwoners",
               ],
        )
        figureICBeds.update_layout(
            yaxis_title="Aantal IC-bedden bezet per 100.000 inwoners",
            xaxis_title="Datum",
            legend_title="Land",
        )
        figureBeds = px.line(
            df,
            x='Datum publicatie',
            y=["Ziekenhuisbedden VK bezet per 100.000 inwoners",
               "Ziekenhuisbedden NL bezet per 100.000 inwoners",
               ],
        )
        figureBeds.update_layout(
            yaxis_title="Aantal Ziekenhuisbedden per 100.000 inwoners",
            xaxis_title="Datum",
            legend_title="Land",
        )
        return [
            html.H1('Bedden in het ziekenhuis',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Bezet (Absoluut)", href="/bedden-bezet-absolute", active="exact"),
                    dbc.NavLink("Bezet (Relatief)", href="/bedden-bezet-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Beschikbaar (Absoluut)", href="/bedden-beschikbaar-absolute", active="exact"),
                    dbc.NavLink("Beschikbaar (Relatief)", href="/bedden-beschikbaar-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureICBeds),
            dcc.Graph(figure=figureBeds),
        ]
    elif pathname == "/bedden-beschikbaar-absolute":
        figureICBeds = px.line(
            df_zorg,
            x='Year',
            y=["IC-bedden VK",
               "IC-bedden NL",
               ],
        )
        figureICBeds.update_layout(
            yaxis_title="Aantal IC-bedden",
            xaxis_title="Jaar",
            legend_title="Land",
        )
        figureBeds = px.line(
            df_zorg,
            x='Year',
            y=["Ziekenhuisbedden VK",
               "Ziekenhuisbedden NL",
               ],
        )
        figureBeds.update_layout(
            yaxis_title="Aantal Ziekenhuisbedden",
            xaxis_title="Jaar",
            legend_title="Land",
        )
        return [
            html.H1('Bedden in het ziekenhuis',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Bezet (Absoluut)", href="/bedden-bezet-absolute", active="exact"),
                    dbc.NavLink("Bezet (Relatief)", href="/bedden-bezet-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Beschikbaar (Absoluut)", href="/bedden-beschikbaar-absolute", active="exact"),
                    dbc.NavLink("Beschikbaar (Relatief)", href="/bedden-beschikbaar-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureICBeds),
            dcc.Graph(figure=figureBeds),
        ]
    elif pathname == "/bedden-beschikbaar-relative":
        figureICBeds = px.line(
            df_zorg,
            x='Year',
            y=["IC-bedden VK per 100.000 inwoners",
               "IC-bedden NL per 100.000 inwoners",
               ],
        )
        figureICBeds.update_layout(
            yaxis_title="Aantal IC-bedden per 100.000 inwoners",
            xaxis_title="Jaar",
            legend_title="Land",
        )
        figureBeds = px.line(
            df_zorg,
            x='Year',
            y=["Ziekenhuisbedden VK per 100.000 inwoners",
               "Ziekenhuisbedden NL per 100.000 inwoners",
               ],
        )
        figureBeds.update_layout(
            yaxis_title="Aantal Ziekenhuisbedden per 100.000 inwoners",
            xaxis_title="Jaar",
            legend_title="Land",
        )
        return [
            html.H1('Bedden in het ziekenhuis',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Bezet (Absoluut)", href="/bedden-bezet-absolute", active="exact"),
                    dbc.NavLink("Bezet (Relatief)", href="/bedden-bezet-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Beschikbaar (Absoluut)", href="/bedden-beschikbaar-absolute", active="exact"),
                    dbc.NavLink("Beschikbaar (Relatief)", href="/bedden-beschikbaar-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(figure=figureICBeds),
            dcc.Graph(figure=figureBeds),
        ]
    elif pathname == "/uitgaven-absolute":
        figureSpending = px.bar(
            df_zorg,
            x='Year',
            y=["Uitgaven VK in Pond",
               "Uitgaven VK in Euro",
               "Uitgaven NL in Euro"],
            barmode="group",
            height=800,
        )
        figureSpending.update_layout(
            yaxis_title="Uitgaven (B = miljard)",
            xaxis_title="Jaar",
            legend_title="Land en valuta",
        )

        lines_to_hide = ["Uitgaven VK in Pond"]
        figureSpending.for_each_trace(lambda trace: trace.update(visible="legendonly")
        if trace.name in lines_to_hide else ())

        return [
            html.H1('Uitgaven aan zorg',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Absoluut", href="/uitgaven-absolute", active="exact"),
                    dbc.NavLink("Relatief", href="/uitgaven-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(
                figure=figureSpending),
        ]
    elif pathname == "/uitgaven-relative":
        figureSpending = px.bar(
            df_zorg,
            x='Year',
            y=["Uitgaven VK in Pond per inwoner",
               "Uitgaven VK in Euro per inwoner",
               "Uitgaven NL in Euro per inwoner"],
            barmode="group",
            height=800,
        )
        figureSpending.update_layout(
            yaxis_title="Uitgaven per inwoner",
            xaxis_title="Jaar",
            legend_title="Land en valuta",
        )

        lines_to_hide = ["Uitgaven VK in Pond per inwoner"]
        figureSpending.for_each_trace(lambda trace: trace.update(visible="legendonly")
        if trace.name in lines_to_hide else ())

        return [
            html.H1('Uitgaven aan zorg',
                    style={'textAlign': 'center'}),
            dbc.Nav(
                [
                    dbc.NavLink("Absoluut", href="/uitgaven-absolute", active="exact"),
                    dbc.NavLink("Relatief", href="/uitgaven-relative", active="exact"),
                ],
                vertical=False,
                pills=True,
            ),
            dcc.Graph(
                figure=figureSpending),
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
