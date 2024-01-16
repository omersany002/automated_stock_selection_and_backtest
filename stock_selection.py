"""Stock Selection Local file"""
from portfolio_construction import get_optimal_weights
import pandas as pd
import numpy as np
import yfinance as yf

class SelectionStrategies:
    """This calss contains different stock selection strategies"""
    def __init__(self, target_year, rebalance_time, port_type):
        self.date = target_year
        self.rebalance = rebalance_time
        self.port_type = port_type
        self.price_path = r"csvs\optimized_csvs\opt_price.csv"
        self.ratios_path = r"csvs\optimized_csvs\opt_ratios.csv"
        self.price_df = pd.read_csv(self.price_path)
        self.ratio_df = pd.read_csv(self.ratios_path)
        self.value_tickers = self.value_stocks()
        self.growth_tickers = self.growth_stocks()
        self.dividend_tickers = self.dividend_stocks()
        self.quality_tickers = self.quality_stocks()

    def value_stocks(self):
        """This function returns twenty value stock tickers.
        Selection Criteria:
            - Price to Book Value(ptb) ratio of 1 or less
            - Lowest positive P/E ratio(pe_op_basic)
        """
        df = self.ratio_df
        date = self.date
        df['public_date'] = pd.to_datetime(df['public_date'])
        df = self.ratio_df[
            (self.ratio_df['public_date']==self.date) &
            (self.ratio_df['ptb'] <=1) &
            (self.ratio_df['pe_op_basic'] > 0)
            ]

        while df.empty:
            date = date-pd.DateOffset(days=1)
            df = self.ratio_df[
                (self.ratio_df['public_date']==date) &
                (self.ratio_df['ptb'] <=1) &
                (self.ratio_df['pe_op_basic'] > 0)
                ]

        result = df.sort_values(by='pe_op_basic')['TICKER']
        tickers = result.dropna().values[:20].tolist()
        return tickers

    def growth_stocks(self):
        """This function returns twenty growth stock tickers.
        Selection Criteria:
            - Highest growth in Revenue (revtq) in last four quarters.
            """
        df = self.ratio_df
        start_date = self.date-pd.DateOffset(years=1)
        df['public_date'] = pd.to_datetime(df['public_date'])
        filtered_df = df[(df['public_date'] >= start_date) & \
                         (df['public_date'] <= self.date)].copy()
        df_grouped = filtered_df.groupby('TICKER').agg({'aftret_invcapx': ['first', 'last']})
        df_grouped.columns = ['first', 'last']
        df_grouped['roic'] = df_grouped['last'] / df_grouped['first']
        df_grouped = df_grouped.replace([np.nan, -np.inf, np.inf],0)
        df_sorted = df_grouped.sort_values('roic', ascending=False)
        result = df_sorted.index
        tickers = result.dropna()[:20].tolist()
        return tickers

    def dividend_stocks(self):
        """This function returns twenty dividend stock tickers.
        Selection Criteria:
            - Highest Dividend Yield(divyield)
        """
        df = self.ratio_df
        df['public_date'] = pd.to_datetime(df['public_date'])
        filtered_df = df[df['public_date'] == self.date]
        while filtered_df.empty:
            self.date = self.date - pd.DateOffset(days=1)
            filtered_df = df[df['public_date'] == self.date]
        result = filtered_df.sort_values(by='divyield', ascending=False)['TICKER']
        tickers = result.dropna().values[:20].tolist()
        return tickers

    def quality_stocks(self):
        """This function returns twenty value stock tickers.
        Selection Criteria:
            - Highest return on equity(roe)
        """
        df = self.ratio_df
        df['public_date'] = pd.to_datetime(df['public_date'])
        filtered_df = df[df['public_date'] == self.date]
        if filtered_df.empty:
            self.date = self.date - pd.DateOffset(days=1)
            filtered_df = df[df['public_date'] == self.date]
        result = filtered_df.sort_values(by='roe', ascending=False)['TICKER']
        tickers = result.dropna().values[:20].tolist()
        return tickers

    def optimal_weights(self):
        """Backtesting the strategies"""
        value_weights = get_optimal_weights(
            self.value_tickers,self.price_df, self.date, self.port_type
            )
        growth_weights = get_optimal_weights(
            self.growth_tickers, self.price_df ,self.date, self.port_type
            )
        dividend_weights = get_optimal_weights(
            self.dividend_tickers, self.price_df ,self.date, self.port_type
            )
        quality_weights = get_optimal_weights(
            self.quality_tickers, self.price_df ,self.date, self.port_type
            )
        return value_weights, growth_weights, dividend_weights, quality_weights

    def calculate_portfolio_return(self, portfolio, start_date):
        """Function that can calculate the return a portfolio generates in next six months"""
        end_date = start_date + pd.DateOffset(months = self.rebalance)
        tickers = portfolio.index.tolist()
        weights = portfolio.values
        selected_df = self.price_df[self.price_df['TICKER'].isin(tickers)].copy()
        pre_filter = pd.pivot_table(selected_df, index = 'date', columns = 'TICKER', values = 'PRC')
        pre_filter.index = pd.to_datetime(pre_filter.index)
        filtered_df = pre_filter[(pre_filter.index>=start_date) & (pre_filter.index <= end_date)]
        # Calculate portfolio returns
        total_return = (filtered_df.iloc[-1] / filtered_df.iloc[0]) - 1
        portfolio_return = (total_return * weights).sum()
        return portfolio_return

    def performance_measure(self):
        """Measuring performance of each strategies"""
        sp500 = self.calculate_index_return('SPY', self.date)
        performance = [self.date+pd.DateOffset(months=self.rebalance), sp500]
        weights = self.optimal_weights()
        for wts in weights:
            port_rets = self.calculate_portfolio_return(wts, self.date)
            performance.append(port_rets)
        return performance

    def calculate_index_return(self, index, start_date):
        """function to calculate index return"""
        end_date = start_date + pd.DateOffset(months=self.rebalance)
        df = yf.Ticker(index).history(start=start_date, end=end_date)['Close']
        total_return = (df.iloc[-1] / df.iloc[0]) - 1
        return total_return
