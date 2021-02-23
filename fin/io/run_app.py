import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import dash_html_components as html
import json
from pkg_resources import compatible_platforms
import plotly.express as px
import pandas as pd
import yfinance as yf
import joblib
from dash.dependencies import Input, Output, State
from fin import config
from fin.domain.session.usersession import session_default
from fin.domain.web_layout import core_elements
from fin.domain.logic.stocks import get_quantfig, stocks_data, stocks_chart
from typing import Dict, List


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

data_store = dcc.Store(id="data_store")


dropdown_state = ["ticker_dropdown_state"]
ticker_date_range_state = [
    "ticker_date_range_start_state",
    "ticker_date_range_end_state",
]
check_state = [
    "bollinger_check_state",
    "macd_check_state",
    "rsi_check_state",
    "sma_check_state",
]
input_state = [
    "bollinger_periods_state",
    "boll_std_state",
    "macd_fast_period_state",
    "macd_slow_period_state",
    "macd_signal_period_state",
    "rsi_periods_state",
    "rsi_lower_state",
    "rsi_upper_state",
    "sma_periods_state",
]

state_ids = dropdown_state + ticker_date_range_state + check_state + input_state

# create html.Div store objects whose ids indicate their corresponding source using
# their id name followed by a trailing "_state"

state_store = html.Div(
    children=[html.Div(id=state, style={"display": "none"}) for state in state_ids]
)


@app.callback(
    Output("bollinger_check_state", "children"),
    Input("bollinger_check", "value"),
)
def store_bollinger_check_state(check_state: List):
    return check_state


@app.callback(
    Output("macd_check_state", "children"),
    Input("macd_check", "value"),
)
def store_macd_check_state(check_state: List):
    return check_state


@app.callback(
    Output("rsi_check_state", "children"),
    Input("rsi_check", "value"),
)
def store_rsi_check_state(check_state: List):
    return check_state


@app.callback(
    Output("sma_check_state", "children"),
    Input("sma_check", "value"),
)
def store_sma_check_state(check_state: List):
    return check_state


@app.callback(
    Output("bollinger_periods_state", "children"),
    Input("bollinger_periods", "value"),
    Input("bollinger_periods", "placeholder"),
)
def store_boll_periods_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("boll_std_state", "children"),
    Input("boll_std", "value"),
    Input("boll_std", "placeholder"),
)
def store_boll_std_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("ticker_dropdown_state", "children"),
    Input("ticker_dropdown", "value"),
)
def ticker_dropdown_state(setting_val):
    return setting_val


@app.callback(
    Output("ticker_date_range_start_state", "children"),
    Input("ticker_date_range", "start_date"),
)
def ticker_date_range_start_state(setting_val):
    return setting_val


@app.callback(
    Output("ticker_date_range_end_state", "children"),
    Input("ticker_date_range", "end_date"),
)
def ticker_date_range_end_state(setting_val):
    return setting_val


@app.callback(
    Output("macd_fast_period_state", "children"),
    Input("macd_fast_period", "value"),
    Input("macd_fast_period", "placeholder"),
)
def macd_fast_period_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("macd_slow_period_state", "children"),
    Input("macd_slow_period", "value"),
    Input("macd_slow_period", "placeholder"),
)
def macd_slow_period_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("macd_signal_period_state", "children"),
    Input("macd_signal_period", "value"),
    Input("macd_signal_period", "placeholder"),
)
def macd_signal_period_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("rsi_periods_state", "children"),
    Input("rsi_periods", "value"),
    Input("rsi_periods", "placeholder"),
)
def rsi_periods_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("rsi_lower_state", "children"),
    Input("rsi_lower", "value"),
    Input("rsi_lower", "placeholder"),
)
def rsi_lower_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("rsi_upper_state", "children"),
    Input("rsi_upper", "value"),
    Input("rsi_upper", "placeholder"),
)
def rsi_upper_state(setting_val, setting_default):
    return setting_val or setting_default


@app.callback(
    Output("sma_periods_state", "children"),
    Input("sma_periods", "value"),
    Input("sma_periods", "placeholder"),
)
def sma_periods_state(setting_val, setting_default):
    return setting_val or setting_default


states = [State(state_id, "children") for state_id in state_ids]


@app.callback(
    Output(component_id="stock-graph", component_property="figure"),
    # Output(component_id="data_store", component_property="data"),
    Input(component_id="generate_button", component_property="n_clicks"),
    states,
)
def store_chart_settings(n_clicks, *args):
    # TODO: Add docstring
    # TODO: read out chart settings
    if n_clicks is None:
        # create initial user session on start up
        # data = session_default
        raise PreventUpdate
    else:
        # make component properties  values accessable by their component id name
        input_names = [state_item.component_id for state_item in states]
        kwargs_dict = dict(zip(input_names, args))

        # request stock data from yf API
        stocks_df = stocks_data(
            kwargs_dict["ticker_dropdown_state"],
            kwargs_dict["ticker_date_range_start_state"],
            kwargs_dict["ticker_date_range_end_state"],
        )
        # generate graph
        fig = stocks_chart(stocks_df, kwargs_dict)

    return fig


test_div = html.Div(id="store_point")
app.layout = html.Div(
    children=[
        headline,
        description,
        html.Div(children=[stocks_div, features1_div, feature2_div]),
        button,
        graph,
        test_div,
        state_store,
        data_store,
    ]
)
