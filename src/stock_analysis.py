import cufflinks as cf
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as plyo
import yfinance as yf
from src import config
from datetime import date
from pylab import mpl, plt
from typing import Tuple
from ftplib import FTP


plt.style.use("seaborn")
mpl.rcParams["font.family"] = "serif"

# activate plotly only in a notebook environment
try:
    get_ipython
    plyo.init_notebook_mode(connected=True)
    print("Plotly activated.")
except NameError:
    pass


def get_quantfig(
    ticker_obj: yf.Ticker, start: date, end: date
) -> Tuple[pd.DataFrame, go.Figure]:
    """Generate yfinance data and generate QuantFig object.

    Args:
        ticker_obj (yf.Ticker): ticker symbol to request market data
        start (date): start date for stock data
        end (date): end date for stock data

    Returns:
        Tuple[pd.DataFrame, cf.QuantFig]:
                    - DF containing stock data
                    - QuantFig containing plotting information
    """
    # request api data
    data = ticker_obj.history(
        start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), interval="1d"
    ).drop(columns=["Volume", "Dividends", "Stock Splits"])

    # generate QuantFig object
    qf = cf.QuantFig(data, title="my_title", legend="right")
    # add financial metrics
    qf.add_bollinger_bands(
        periods=15, boll_std=2, colors=["magenta", "grey"], fill=True
    )
    qf.add_sma([10, 20], width=2, color=["green", "lightgreen"], legendgroup=True)
    qf.add_macd()
    qf.add_rsi(periods=14, showbands=False)

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
    return data, qf_fig


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
    fig = get_quantfig(yf.Ticker("PLUG"), date(2020, 1, 1), date.today())[1]
