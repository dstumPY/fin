"""Load and visualize stock market data."""
from datetime import date
from ftplib import FTP
from typing import Dict

import cufflinks as cf
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as plyo
import yfinance as yf
from pylab import mpl, plt

from fin import config
from fin.domain.session.usersession import session_default

plt.style.use("seaborn")
mpl.rcParams["font.family"] = "serif"

# activate plotly only in a notebook environment
try:
    get_ipython  # type: ignore
    plyo.init_notebook_mode(connected=True)
    print("Plotly activated.")
except NameError:
    pass


def get_stocks_data(
    ticker_symbol: str = session_default.ticker[0],
    date_start: str = session_default.start_date,
    date_end: str = session_default.end_date,
) -> pd.DataFrame:
    """Request stock market DataFrame using yfinance.

    Args:
        ticker_symbol (str): ticker symbol string used to request market data
        date_start (str): include only dates later than date_start
        date_end (str): include only dates earlier than date_end

    Returns:
        pd.DataFrame: DataFrame containing stock data
    """
    stocks_df = (
        yf.Ticker(ticker_symbol)
        .history(start=date_start, end=date_end, interval="1d")
        .drop(columns=["Volume", "Dividends", "Stock Splits"])
    )

    return stocks_df


def stocks_chart(
    stock_data: pd.DataFrame = None, settings_dict: Dict = None
) -> go.Figure:
    """Generate plotly finance chart.

    Args:
        stocks_data (pd.DataFrame): stock data derived from yf
        settings (Dict): settings derived from the UI

    Returns:
        go.Figure: final stock chart
    """
    # setting default values
    data = get_stocks_data() if stock_data is None else stock_data
    if settings_dict is None:
        settings_dict = {
            key + "_state": value for key, value in session_default.__dict__.items()
        }
        settings_dict["ticker_dropdown_state"] = settings_dict["ticker"][0]
    # extract chart settings from settings_dict

    # if  UI checklists were deselected settings_dict values are empty lists
    add_boll_feature = bool(len(settings_dict["bollinger_check_state"]))
    add_macd_feature = bool(len(settings_dict["macd_check_state"]))
    add_rsi_feature = bool(len(settings_dict["rsi_check_state"]))
    add_sma_feature = bool(len(settings_dict["sma_check_state"]))

    # initialize QuantFig chart figure
    qf = cf.QuantFig(data, title=settings_dict["ticker_dropdown_state"], legend="right")

    if add_boll_feature is True:
        qf.add_bollinger_bands(
            periods=settings_dict["bollinger_periods_state"],
            boll_std=settings_dict["boll_std_state"],
        )

    if add_macd_feature is True:
        qf.add_macd(
            fast_period=settings_dict["macd_fast_period_state"],
            slow_period=settings_dict["macd_slow_period_state"],
            signal_period=settings_dict["macd_signal_period_state"],
        )

    if add_rsi_feature is True:
        qf.add_rsi(
            periods=settings_dict["rsi_periods_state"],
            rsi_lower=settings_dict["rsi_lower_state"],
            rsi_upper=settings_dict["rsi_upper_state"],
        )

    if add_sma_feature is True:
        qf.add_sma(periods=settings_dict["sma_periods_state"])

    # cast QuantFig object to plotly figure
    qf_fig = qf.figure()

    # add time slider to figure
    slider_dict = dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
    qf_fig.update_layout(xaxis=slider_dict)

    return qf_fig


def persist_figure(qf_fig: go.Figure, ticker: yf.Ticker):
    """Generate plot from QuantFig and store resulting chart as HTML file.

    Args:
        ticker (yf.Ticker): yfinance ticker symbol, from that qf was derived
        qf (cf.QuantFig): QuantFig object which contains chart data
    """
    # plot figure
    qf_fig.show()

    # store interactive HTML file
    qf_fig.write_html(f"""{ticker}_quantFig_{date.today().strftime("%Y_%m_%d")}.html""")


def load_ticker_data():
    """Load NASDAQ ticker information from ftp.nasdaqtrader.com FTP server."""
    # Create FTP connection, move to specific dir
    ftp = FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("symboldirectory")

    # read & store files from FTP server locally
    try:
        with open(config.DATA_API / "nasdaqlisted.csv", "wb") as fh:
            ftp.retrbinary("RETR nasdaqlisted.txt", fh.write)
    except Exception:
        print("Failed loading nasdaqlisted.txt")
    try:
        with open(config.DATA_API / "otherlisted.csv", "wb") as fh:
            ftp.retrbinary("RETR otherlisted.txt", fh.write)
    except Exception:
        print("Failed loading otherlisted.txt")


def extract_ticker_symbols():
    """Generate and store ticker symbol list from raw data."""
    # sep: separate cols by "|"
    # skipfooter: rm processing information on last line
    # usecols: use only ticker symbols
    nasdaq_listed = pd.read_csv(
        config.DATA_API / "nasdaqlisted.csv",
        sep="|",
        skipfooter=1,
        usecols=["Symbol"],
    )
    other_listed = pd.read_csv(
        config.DATA_API / "otherlisted.csv",
        sep="|",
        skipfooter=1,
        usecols=["ACT Symbol"],
    ).rename(columns={"ACT Symbol": "Symbol"})

    # store ticker list locally
    tickers_list = list(
        pd.concat([nasdaq_listed, other_listed], axis=0).Symbol.unique()
    )
    joblib.dump(tickers_list, config.DATA_API / "tickers_list.lzma")


if __name__ == "__main__":
    fig_data = get_stocks_data()
    fig = stocks_chart()
    print("Done.")
