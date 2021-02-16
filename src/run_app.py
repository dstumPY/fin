import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import json
import plotly.express as px
import pandas as pd
import yfinance as yf
import joblib
from dash.dependencies import Input, Output, State
from src import config
from src.session.usersession import session_default, UserSession
from src.web_layout import core_elements
from src.stock_analysis import get_quantfig


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)

fig = joblib.load(config.DATA_FOLDER / "plug_fig.lzma")


headline = html.H1("Stock Market Analysis")
description = html.Div(children="Choose your settings.")
stocks_div = core_elements.stock_settings()
features1_div, feature2_div = core_elements.feature_settings()
button = dbc.Button(
    "Generate chart", id="generate_button", color="primary", block=True, size="sm"
)
graph = dcc.Graph(id="stock-graph", figure=fig)
text_area = html.Div(id="store_point")
data_store = dcc.Store(id="data_store")


@app.callback(
    Output(component_id="bollinger_check", component_property="value"),
    Output(component_id="store_point", component_property="children"),
    Output(component_id="data_store", component_property="data"),
    Input(component_id="generate_button", component_property="n_clicks"),
    State(component_id="data_store", component_property="data"),
)
def show_session(n_clicks, data):
    if n_clicks is None:
        # create initial user session on start up
        data = session_default
    else:
        data = UserSession(json.loads(data))

    print("Zero")
    return (
        data.bollinger_check,
        json.dumps(data.__dict__),
        json.dumps(data.__dict__),
    )


app.layout = html.Div(
    children=[
        headline,
        description,
        html.Div(children=[stocks_div, features1_div, feature2_div]),
        button,
        text_area,
        data_store,
    ]
)
