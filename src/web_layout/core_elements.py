import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import joblib
from datetime import date, datetime
from src import config
from src.session.usersession import session_default
from typing import List, Tuple


def get_ticker_symbols(ticker_list: List[str] = None) -> dcc.Dropdown:
    """Generate a Dropdown list filled with Yahoo Finance ticker symbols.

    Args:
        ticker_list (List[str]): ticker symbols list

    Returns:
        dcc.Dropdown: dash Dropdown element containing ticker symbols
    """
    ticker_list = joblib.load(config.DATA_API / "tickers_list.lzma")
    return dcc.Dropdown(
        id="ticker_dropdown",
        options=[{"label": tick, "value": tick} for tick in ticker_list],
        style={"width": "65%"},
        # set initial page load value
        value=session_default.ticker[0],
    )


def feature_settings() -> Tuple[html.Div, html.Div]:
    """Generate web elements for statistical configuration (bollinger, MACD, RSI, SMA).

    The default_session variable is used for default page load initialization.

    Returns:
        Tuple[html.Div, html.Div]: Div (bollinger, SMA), Div (RSI, MACD)
    """
    # default layout setting for input elements
    input_default = {
        "type": "number",
        "min": 1,
        "step": 1,
        "style": {"margin-right": "10px", "width": "10%"},
    }

    # add bollinger band feature
    bollinger_band_check = dcc.Checklist(
        id="bollinger_check",
        options=[
            {"label": "Bollinger Bands", "value": "bollinger_bands"},
        ],
        value=session_default.bollinger_check,
    )
    bollinger_input = dbc.InputGroup(
        [
            dbc.InputGroupAddon("Periods", addon_type="prepend"),
            dbc.Input(
                id="bollinger_periods",
                placeholder=session_default.bollinger_input_periods,
                **input_default
            ),
            dbc.InputGroupAddon("Std deviation", addon_type="prepend"),
            dbc.Input(
                id="boll_std",
                placeholder=session_default.bollinger_input_stddev,
                **input_default
            ),
        ],
    )

    # add macd feature
    macd_check = dcc.Checklist(
        id="macd_check",
        options=[{"label": "MACD", "value": "macd_check"}],
        value=session_default.macd_check,
    )
    macd_input = dbc.InputGroup(
        [
            dbc.InputGroupAddon("FastPeriod"),
            dbc.Input(
                id="macd_fast_period",
                placeholder=session_default.macd_fast_period,
                **input_default
            ),
            dbc.InputGroupAddon("SlowPeriod"),
            dbc.Input(
                id="macd_slow_period",
                placeholder=session_default.macd_slow_period,
                **input_default
            ),
            dbc.InputGroupAddon("SignalPeriod"),
            dbc.Input(
                id="macd_signal_period",
                placeholder=session_default.macd_signal_period,
                **input_default
            ),
        ]
    )

    # RSI feature
    rsi_check = dcc.Checklist(
        id="rsi_check",
        options=[{"label": "RSI", "value": "rsi_check"}],
        value=session_default.rsi_check,
    )
    rsi_input = dbc.InputGroup(
        [
            dbc.InputGroupAddon("Periods"),
            dbc.Input(
                id="rsi_periods",
                placeholder=session_default.rsi_periods,
                **input_default
            ),
            dbc.InputGroupAddon("RSI lower"),
            dbc.Input(
                id="rsi_lower", placeholder=session_default.rsi_lower, **input_default
            ),
            dbc.InputGroupAddon("RSI upper"),
            dbc.Input(
                id="rsi_upper", placeholder=session_default.rsi_upper, **input_default
            ),
        ]
    )

    # add sma feature
    sma_check = dcc.Checklist(
        id="sma_check",
        options=[{"label": "SMA", "value": "sma_check"}],
        value=session_default.sma_check,
    )
    sma_input = dbc.InputGroup(
        [
            dbc.InputGroupAddon("Periods"),
            dbc.Input(
                id="sma_periods", placeholder=session_default.sma_periods, **input_default
            ),
        ]
    )

    # wrap features in div
    feature_table1 = html.Div(
        children=[
            html.Div(bollinger_band_check),
            html.Div([bollinger_input]),
            html.Div(sma_check),
            html.Div([sma_input]),
        ],
        style={"width": "400px", "display": "inline-block", "padding": "20px"},
    )
    feature_table2 = html.Div(
        children=[
            rsi_check,
            rsi_input,
            macd_check,
            macd_input,
        ],
        style={"width": "550px", "display": "inline-block"},
    )
    return feature_table1, feature_table2


def stock_settings() -> html.Div:
    """Generate web elt for stock and time window selection.

    Returns:
        html.Div: div elt containing dropdown menu and date picker.
    """
    # dropdown for stock selection and DatePickerRange for time window selection
    date_label, ticker_label = html.Label("Date Range"), html.Label("Dropdown")
    ticker_dropdown = get_ticker_symbols()
    date_range_picker = dcc.DatePickerRange(
        id="ticker_date_range",
        start_date=datetime.strptime(session_default.start_date, "%Y-%m-%d"),
        end_date=datetime.strftime(date.today(), "%Y-%m-%d"),
        clearable=True,
        first_day_of_week=1,
    )

    # arrange elts in div
    ticker_selection = html.Div(
        [ticker_label, ticker_dropdown, date_label, date_range_picker],
        style={"width": "350px", "display": "inline-block"},
    )
    return ticker_selection
