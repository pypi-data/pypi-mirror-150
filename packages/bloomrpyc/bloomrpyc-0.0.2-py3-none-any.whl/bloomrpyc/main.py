# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present Jinho Kim
"""
import rpyc
import functools
import pandas as pd
from typing import Union, List, Optional


class Bloomberg(object):
    """ Bloomberg API Client
    
    This class communicates with the server running on the Bloomberg Terminal PC to parse the Bloomberg API data.
    Note that you must have the server running on your Bloomberg Terminal PC.
    Bloomberg functionality implemented in this class is the same as xbbg.
    
    Attributes
    ----------
    ip_address: str
        ip address of bloomberg terminal PC server
    port: int
        port number of bloomberg terminal PC server

    Examples
    --------      
    >>> BLOOOMBERG_IP_ADDRESS = '192.168.112.46'
    >>> BLOOMBERG_PORT = 18861
    >>> cli = Bloomberg(BLOOOMBERG_IP_ADDRESS, BLOOOMBERG_PORT)
    >>> cli.bdh('MSFT US Equity', 'PX_LAST', '2022-01-01', '2022-03-23')

    References
    ----------
    [1] xbbg: Intuitive Bloomberg data API, https://github.com/alpha-xone/xbbg
    [2] RPyC: Transparent, Symmetric Distributed Computing, https://rpyc.readthedocs.io/en/latest/
    """
    def __init__(self, ip_address: str, port: int):
        # server configuration
        self.ip_address = ip_address
        self.port = port

        # connection
        self._con = rpyc.connect(self.ip_address, self.port)
        self._root = self._con.root

    def deep_copy_rpyc_df(func, orient='split'):
        """Wrapper to makes a deep copy of netref objects that come as a result of RPyC remote method calls.

        When RPyC client obtains a result from the remote method call, this result may contain
        non-scalar types (List, Dict, ...) which are given as a wrapper class (a netref object). 
        This class does not have all the standard attributes (e.g. dict.tems() does not work) 
        and in addition the objects only exist while the connection is active. 
        To have a retuned value represented by python's native datatypes and to by able to use it 
        after the connection is terminated, this routine makes a recursive copy of the given object. 

        Parameters
        ----------
        func: function
            RPyC remote method call function
        orient: str
            Indication of expected JSON string format
        """
        @functools.wraps(func)
        def wrapping(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                col_nlevels = result.columns.nlevels
                # accept only dataframe up to level 2
                if col_nlevels == 1:
                    result_json = result.to_json(orient=orient) # rpyc obj to json
                    result = pd.read_json(result_json, orient=orient) # json to df

                elif col_nlevels == 2:
                    # rpyc obj to json
                    result_dict = {}
                    for top_level_col in result.columns.levels[0]:
                        result_dict[top_level_col] = result[top_level_col].to_json(orient=orient)

                    # json to df
                    result = pd.DataFrame()
                    for top_level_col, top_level_json in result_dict.items():
                        top_level_df = pd.read_json(top_level_json, orient=orient)
                        top_level_df.columns = pd.MultiIndex.from_product([[top_level_col], top_level_df.columns])
                        result = pd.concat([result, top_level_df], axis=1)

                else:
                    raise ("Check data types")
            return result
        return wrapping

    @deep_copy_rpyc_df
    def bdp(self, tickers: Union[str, List], flds: Union[str, List], **kwargs) -> pd.DataFrame:
        """Bloomberg reference data

        Parameters
        ----------
        tickers: Union[str, List] 
            tickers
        flds: Union[str, List] 
            fields to query
        **kwargs: dict
            other overrides for query

        Returns
        -------
        pd.DataFrame
        """
        return self._root.bdp(tickers, flds, **kwargs)

    @deep_copy_rpyc_df
    def bds(self, tickers: Union[str, List], flds: Union[str, List], use_port: bool = False, **kwargs) -> pd.DataFrame:
        """Bloomberg block data

        Parameters
        ----------
        tickers: Union[str, List] 
            tickers
        flds: Union[str, List] 
            fields to query
        use_port: bool
            use `PortfolioDataRequest`
        **kwargs: dict
            other overrides for query

        Returns
        -------
        pd.DataFrame
        """
        return self._root.bds(tickers, flds, use_port, **kwargs)

    @deep_copy_rpyc_df
    def bdh(self, tickers: Union[str, List], flds: Union[str, List], start_date: str, end_date: str = 'today', adjust: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Bloomberg historical data

        Parameters
        ----------
        tickers: Union[str, List] 
            ticker(s)
        flds: Union[str, List] 
            field(s) to query
        start_date: str
            start date
        end_date: str
            end date - default today
        adjust: Optional[str]
                `all`, `dvd`, `normal`, `abn` (=abnormal), `split`, `-` or None
                exact match of above words will adjust for corresponding events
                Case 0: `-` no adjustment for dividend or split
                Case 1: `dvd` or `normal|abn` will adjust for all dividends except splits
                Case 2: `adjust` will adjust for splits and ignore all dividends
                Case 3: `all` == `dvd|split` == adjust for all
                Case 4: None == Bloomberg default OR use kwargs
        **kwargs: dict
            other overrides for query

        Returns
        -------
        pd.DataFrame
        """
        return self._root.bdh(tickers, flds, start_date, end_date, adjust, **kwargs)

    @deep_copy_rpyc_df
    def bdib(self, ticker: str, dt: str, session: str = 'allday', typ:str = 'TRADE', **kwargs) -> pd.DataFrame:
        """Bloomberg intraday bar data

        Parameters
        ----------
        tickers: str
            ticker
        dt: str
            date to download
        session: str
            [allday, day, am, pm, pre, post]
        typ: str
            [TRADE, BID, ASK, BID_BEST, ASK_BEST, BEST_BID, BEST_ASK]
        **kwargs: dict
            ref: reference ticker or exchange
                 used as supplement if exchange info is not defined for `ticker`
            batch: whether is batch process to download data
            log: level of logs

        Returns
        -------
        pd.DataFrame
        """
        return self._root.bdib(ticker, dt, session, typ, **kwargs)

    @deep_copy_rpyc_df
    def bdtick(self, ticker: str, dt: str, session: str = 'allday', time_range: Optional[str] = None, types: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Bloomberg tick data

        Parameters
        ----------
        tickers: str
            ticker
        dt: str
            date to download
        session: str
            [allday, day, am, pm, pre, post]
        time_range: Optional[str]
            tuple of start and end time (must be converted into UTC)
            if this is given, `dt` and `session` will be ignored
        types: Optional[str]
            str or list, one or combinations of [
            TRADE, AT_TRADE, BID, ASK, MID_PRICE,
            BID_BEST, ASK_BEST, BEST_BID, BEST_ASK,
        ]

        Returns
        -------
        pd.DataFrame
        """
        return self._root.bdtick(ticker, dt, session, time_range, types, **kwargs)

    @deep_copy_rpyc_df
    def earning(self, ticker: str, by: str ='Product', typ: str ='Revenue', ccy: Optional[str] = None, level: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Earning exposures by Geo or Products

        Parameters
        ----------
        ticker: str
            ticker
        by: str
            [G(eo), P(roduct)]
        typ: str
            type of earning, start with `PG_` in Bloomberg FLDS - default `Revenue`
            `Revenue` - Revenue of the company
            `Operating_Income` - Operating Income (also named as EBIT) of the company
            `Assets` - Assets of the company
            `Gross_Profit` - Gross profit of the company
            `Capital_Expenditures` - Capital expenditures of the company
        ccy: Optional[str]
            currency of earnings
        level: Optional[str]
            hierarchy level of earnings

        Returns
        -------
        pd.DataFrame
        """
        return self._root.earning(ticker, by, typ, ccy, level, **kwargs)

    @deep_copy_rpyc_df
    def dividend(self, tickers: Union[str, List], typ: str = 'all', start_date: Optional[str] = None, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Bloomberg dividend / split history

        Parameters
        ----------
        tickers: Union[str, List] 
            ticker(s)
        typ: str
            dividend adjustment type
                `all`:       `DVD_Hist_All`
                `dvd`:       `DVD_Hist`
                `split`:     `Eqy_DVD_Hist_Splits`
                `gross`:     `Eqy_DVD_Hist_Gross`
                `adjust`:    `Eqy_DVD_Adjust_Fact`
                `adj_fund`:  `Eqy_DVD_Adj_Fund`
                `with_amt`:  `DVD_Hist_All_with_Amt_Status`
                `dvd_amt`:   `DVD_Hist_with_Amt_Status`
                `gross_amt`: `DVD_Hist_Gross_with_Amt_Stat`
                `projected`: `BDVD_Pr_Ex_Dts_DVD_Amts_w_Ann`
        start_date: Optional[str]
            start date
        end_date: Optional[str]
            end date
        **kwargs: dict
            overrides

        Returns
        -------
        pd.DataFrame
        """
        return self._root.dividend(tickers, typ, start_date, end_date, **kwargs)

    @deep_copy_rpyc_df
    def beqs(self, screen: str, asof: Optional[str] = None, typ: str ='PRIVATE', group: str ='General', **kwargs) -> pd.DataFrame:
        """Bloomberg equity screening

        Parameters
        ----------
        screen: str
            screen name
        asof: Optional[str]
            as of date
        typ: str
            GLOBAL/B (Bloomberg) or PRIVATE/C (Custom, default)
        group: str
            group name if screen is organized into groups

        Returns
        -------
        pd.DataFrame
        """
        return self._root.beqs(screen, asof, typ, group, **kwargs)
    
    def active_futures(self, ticker: str, dt: str, **kwargs) -> str:
        """Active futures contract

        Parameters
        ----------
        ticker: str
            futures ticker, i.e., ESA Index, Z A Index, CLA Comdty, etc.
        dt: str
            date

        Returns
        -------
        str
            ticker name
        """
        return self._root.active_futures(ticker, dt, **kwargs)
    
    def fut_ticker(self, gen_ticker: str, dt, freq: str, **kwargs) -> str:
        """Get proper ticker from generic ticker

        Parameters
        ----------
        gen_ticker: str
            generic ticker
        dt: str
            date
        freq: str
            futures contract frequency

        Returns
        -------
        str
            exact futures ticker
        """
        return self._root.fut_ticker(gen_ticker, dt, freq, **kwargs)
    
    @deep_copy_rpyc_df
    def adjust_ccy(self, data: pd.DataFrame, ccy: str = 'USD') -> pd.DataFrame:
        """Adjust

        Parameters
        ----------
        data: pd.DataFrame
            daily price / turnover / etc. to adjust
        ccy: str
            currency to adjust to

        Returns
        -------
        pd.DataFrame
        """
        return self._root.adjust_ccy(data, ccy)

    @deep_copy_rpyc_df
    def turnover(self, tickers: Union[str, List], flds: str = 'Turnover', start_date: Optional[str] = None, end_date: Optional[str] = None, ccy: str = 'USD', factor: float = 1e6) -> pd.DataFrame:
        """Currency adjusted turnover (in million)

        Parameters
        ----------
        tickers: Union[str, List]
            ticker(s)
        flds: str
            override `flds`
        start_date: Optional[str]
            start date, default 1 month prior to `end_date`
        end_date: Optional[str]
            end date, default T - 1
        ccy: str
            currency - 'USD' (default), any currency, or 'local' (no adjustment)
        factor: float
            adjustment factor, default 1e6 - return values in millions

        Returns
        -------
        pd.DataFrame
        """
        return self._root.turnover(tickers, flds, start_date, end_date, ccy, factor)

