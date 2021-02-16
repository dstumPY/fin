import joblib
from datetime import date
from src import config
from typing import Dict, List


class UserSession:
    """A class storing settings from the current user session.

    The attributes listed below are derived from the cufflinks.QuantFig package.
    For further details see https://github.com/santosjorge/cufflinks

    Args:
        ticker (List[str]):             list of available ticker symbols
        start_date (str):               first day the chart begins
        end_date (str):                 last day the chart ends
        bollinger_check (List[str]):    checklist value for Bollinger feature
        bollinger_input_periods (int):  periods setting for Bollinger feature
        bollinger_input_stddev (int):   standard deviation setting for Bollinger feature
        macd_check (List[str]):         checklist value for MACD feature
        macd_fast_period (int):         fast periods setting for MACD feature
        macd_slow_period (int):         slow periods setting for MACD feature
        macd_signal_period (int):       signal period setting for MACD feature
        rsi_check (List[str]):          checklist value for RSI feature
        rsi_periods (int):              periods setting for RSI feature
        rsi_lower (int):                lower setting for RSI feature
        rsi_upper (int):                upper setting for RSI feature
        sma_check (List[str]):          checklist value for SMA feature
        sma_periods (int):              periods setting for SMA feature
    """

    def __init__(self, dictionary: Dict = None):
        """Generate a session instance.

        A UserSession object can be instantiated with default values for initial page
        load or customized using a dictionary whose key-value mapping results in a
        attribute-value mapping.

        Args:
            dictionary (Dict, optional): [description]. Defaults to None.
        """
        if dictionary is not None:
            # create instance based on a provided dict
            for key, value in dictionary.items():
                setattr(self, key, value)
        else:
            self.ticker: List[str] = joblib.load(config.DATA_API / "tickers_list.lzma")
            self.start_date: str = str(date(2020, 1, 1))
            self.end_date: str = str(date.today())
            self.bollinger_check: List[str] = ["bollinger_bands"]
            self.bollinger_input_periods: int = 20
            self.bollinger_input_stddev: int = 2
            self.macd_check: List[str] = ["macd_check"]
            self.macd_fast_period: int = 12
            self.macd_slow_period: int = 26
            self.macd_signal_period: int = 9
            self.rsi_check: List[str] = ["rsi_check"]
            self.rsi_periods: int = 20
            self.rsi_lower: int = 70
            self.rsi_upper: int = 30
            self.sma_check: List[str] = ["sma_check"]
            self.sma_periods: int = 20


# create default session object for first page load
session_default = UserSession()
