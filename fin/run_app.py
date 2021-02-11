# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
from dash_core_components.DatePickerRange import DatePickerRange
import dash_html_components as html
import plotly.express as px
import pandas as pd
import yfinance as yf
import joblib
from fin import config
from fin.stock_analysis import get_quantfig
from datetime import date
from typing import List

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(external_stylesheets=external_stylesheets)


def get_ticker_symbols(ticker_list: List[str]) -> dcc.Dropdown:
    """Generate a Dropdown list filled with Yahoo Finance ticker symbols.

    Args:
        ticker_list (List[str]): ticker symbols list

    Returns:
        dcc.Dropdown: dash Dropdown element containing ticker symbols
    """
    return dcc.Dropdown(
        options=[
            {"label": tick, "value": tick}
            for tick in joblib.load(config.DATA_API / "tickers_list.lzma")
        ]
    )


def features_checkbox():

    return dcc.Checklist(
        options=[
            {"label": "Bollinger Bands", "value": "bollinger_bands"},
            {"label": "MACD", "value": "macd"},
            {"label": "RSI", "value": "rsi"},
            {"label": "SMA", "value": "sma"},
        ]
    )


yf_ticker = yf.Ticker("PLUG")
start = date(2020, 1, 1)
end = date.today()
fig = joblib.load(config.DATA_FOLDER / "plug_fig.lzma")
ticker_list = ["A", "AA", "AAC", "PLUG"]

headline = html.H1("Stock Market Analysis")
description = html.Div(children="Choose your settings.")
ticker_selection = html.Div(
    [
        html.Label("Dropdown"),
        get_ticker_symbols(ticker_list),
        html.Label("Date Range"),
        dcc.DatePickerRange(start_date=date(1999, 1, 1), end_date=date.today()),
    ],
    style={"width": "16%", "display": "inline-block"},
)
date_selection = html.Div(children=[])
feature_selection = html.Div(children=[html.Label("Features"), features_checkbox()])
bollinger_band = dcc.Checklist(
    options=[
        {"label": "Bollinger Bands", "value": "bollinger_bands"},
    ]
)
bollinger_setting = dcc.Input(type="number", min=1, step=1)
macd = dcc.Checklist(options=[{"label": "MACD", "value": "macd"}])
rsi = dcc.Checklist(options=[{"label": "RSI", "value": "rsi"}])
sma = dcc.Checklist(options=[{"label": "SMA", "value": "sma"}])


feature_table1 = html.Div(
    children=[
        html.Div(bollinger_band),
        html.Div(bollinger_setting),
        html.Div(macd),
        html.Div(bollinger_setting),
    ],
    style={"width": "20%", "float": "right", "display": "inline-block"},
)
feature_table2 = html.Div(
    children=[
        html.Div(rsi),
        html.Div(bollinger_setting),
        html.Div(sma),
        html.Div(bollinger_setting),
    ],
    style={"width": "30%", "float": "right", "display": "inline-block"},
)
graph = dcc.Graph(
    id="stock-graph",
    figure=fig,
)


app.layout = html.Div(
    children=[
        headline,
        description,
        html.Div(
            children=[ticker_selection, feature_table1, feature_table2],
        ),
        # html.Div(graph),
    ]
)
