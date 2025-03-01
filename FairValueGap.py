import yfinance as yf
import pandas as pd
import numpy as np

class SimpleFVG:
    def __init__(self, ticker, start, end, gap_size = 10):
        """
        :param ticker: Ticker for the asset to analyze
        :type ticker: str
        :param start: Start date of the time frame you want to analyze
        :type start: str in form of YYYY-MM-DD
        :param end: End date of time frame you want to analyze
        :type end: str in form of YYYY-MM-DD
        :param gap_size: FVG gap size points, defaults to 10
        :type gap_size: int
        """
        self.ticker = ticker
        self.start = start
        self.end = end
        self.gap_size= gap_size
        self.data = self.__download_data()

        self.results = None

    def __download_data(self):
        df = yf.download(self.ticker, start=self.start, end=self.end)
        df.columns = df.columns.get_level_values(0)
        data = df[['Close', 'High', 'Low', 'Open']]

        data["Daily Return"] = np.log(data["Close"] / data["Close"].shift(1))
        data["Daily Return Buy and Hold"] = data["Daily Return"].cumsum().apply(np.exp)
        data.dropna(inplace=True)

        return data

    def plot_returns(self):
        """
        Plots buy and hold returns and FVG returns.
        """
        if self.data is None:
            print("No data to plot")
        else:
            title = "{} | Gap Size={}".format(self.ticker, self.gap_size)
            self.data[["Daily Return Buy and Hold"]].plot(title=title, figsize=(12,8))

    def get_data(self):
        """
        Returns current state of the dataset
        :return: Pandas DataFrame
        """
        return self.data

    def __find_bullish_fvg(self):

        #Shift "High" down 2 rows. For any given row in data, this value corresponds to the High of
        #the candle 2 periods earlier
        candle1_high = self.data['High'].shift(2)
        self.data['gap'] = self.data['Low'] - candle1_high

        #Condition we are looking for is when the imbalance is at least our set gap size
        pattern = (self.data['gap']) >= self.gap_size
        df_bullish = self.data[pattern]
        print("Bullish FVG found on these dates")
        print(df_bullish[['gap']].head())

    def __bullish_backtest_helper(self):
        #Numerical Comparisons
        # Final cumulative returns:
        final_bh = self.data["Daily Return Buy and Hold"].iloc[-1]
        final_strategy = self.data["bullish_fvg_returns"].iloc[-1]

        print("Final Buy and Hold Return:", final_bh)
        print("Final Strategy Return:", final_strategy)
        # Convert growth factors to percent returns:
        pct_return_bh = (final_bh - 1) * 100
        pct_return_strategy = (final_strategy - 1) * 100

        print(f"Final Buy and Hold Percent Return: {pct_return_bh:.2f}%")
        print(f"Final Strategy Percent Return: {pct_return_strategy:.2f}%")

        # Let's assume these are the start and end dates of your backtest
        start_date = self.data.index[0]
        end_date = self.data.index[-1]
        years = (end_date - start_date).days / 365.25

        CAGR_bh = (final_bh) ** (1 / years) - 1
        CAGR_strategy = (final_strategy) ** (1 / years) - 1

        print(f"Buy-and-Hold CAGR: {CAGR_bh * 100:.2f}%")
        print(f"Strategy CAGR: {CAGR_strategy * 100:.2f}%")

    def bullish_fvg_backtest(self, holding_days):
        """
        Finds bullish fair value gaps and plots the returns on instant long entry and specified holding time.
        Also calculates percent return and CAGR.
        
        :param holding_days: Amount of days to hold each position
        :type holding_days: int
        """

        #Will look for vectorized solutions in the future.
        self.__find_bullish_fvg()
        print("...")

        positions = []
        days_held = 0
        for index, row in self.data.iterrows():
            if days_held > 0:
                positions.append(1)
                days_held += 1

                if days_held >= holding_days:
                    days_held = 0
            else:
                if row['gap'] >= self.gap_size:
                    positions.append(1)
                    days_held = 1
                else:
                    positions.append(0)
        self.data['bullish_fvg_position'] = positions

        self.data["bullish_fvg_returns"] = (self.data["Daily Return"]
                                            * self.data["bullish_fvg_position"].shift(1)).cumsum().apply(np.exp)

        title = "{} | Gap Size={}".format(self.ticker, self.gap_size)
        self.data[["Daily Return Buy and Hold", "bullish_fvg_returns"]].plot(title=title, figsize=(12,8))

        #Print out our numerical comparisons
        self.__bullish_backtest_helper()

    def __find_bearish_fvg(self):
        candle1_low = self.data['Low'].shift(2)
        self.data['gap'] = candle1_low - self.data['High']

        pattern = (self.data['gap']) >= self.gap_size
        df_bearish = self.data[pattern]
        print("Bearish FVG found on these dates")
        print(df_bearish[['gap']].head())

    def __bearish_backtest_helper(self):
        #Numerical Comparisons
        # Final cumulative returns:
        final_bh = self.data["Daily Return Buy and Hold"].iloc[-1]
        final_strategy = self.data["bearish_fvg_returns"].iloc[-1]

        print("Final Buy and Hold Return:", final_bh)
        print("Final Strategy Return:", final_strategy)
        # Convert growth factors to percent returns:
        pct_return_bh = (final_bh - 1) * 100
        pct_return_strategy = (final_strategy - 1) * 100

        print(f"Final Buy and Hold Percent Return: {pct_return_bh:.2f}%")
        print(f"Final Strategy Percent Return: {pct_return_strategy:.2f}%")

        # Let's assume these are the start and end dates of your backtest
        start_date = self.data.index[0]
        end_date = self.data.index[-1]
        years = (end_date - start_date).days / 365.25

        CAGR_bh = (final_bh) ** (1 / years) - 1
        CAGR_strategy = (final_strategy) ** (1 / years) - 1

        print(f"Buy-and-Hold CAGR: {CAGR_bh * 100:.2f}%")
        print(f"Strategy CAGR: {CAGR_strategy * 100:.2f}%")

    def bearish_fvg_backtest(self, holding_days, wait_days=3):
        """
        Finds bearish fair value gaps, waits a set number of days for a price retracement, and enters for a specified
        number of holding days if price does retrace back to the fair value gap.

        Plots these returns.
        Also calculates percent return and CAGR.
        
        :param holding_days: Amount of days to hold each position
        :type holding_days: int
        :param wait_days: Amount of days to wait for a retracement (default = 3)
        :type wait_days: int
        """

        # Will look for vectorized solutions in the future.
        self.__find_bearish_fvg()

        #Temporary candle1_low row for tracking fvg price range
        self.data['candle1_low'] = self.data['Low'].shift(2)
        print("...")

        positions = []
        waiting = False
        waiting_days = 0

        gap_lower = None
        gap_upper = None
        days_held = 0
        for index, row in self.data.iterrows():
            if days_held > 0:
                positions.append(-1)
                days_held += 1

                if days_held >= holding_days:
                    days_held = 0
                continue
            if waiting:
                waiting_days += 1
                if gap_lower is not None and gap_upper is not None and gap_lower <= row['High'] <= gap_upper:
                    positions.append(-1)
                    days_held = 1
                    waiting = False
                    waiting_days = 0
                    continue
                else:
                    positions.append(0)
                if waiting_days >= wait_days:
                    waiting = False
                    waiting_days = 0
                continue
            if row['gap'] >= self.gap_size:
                waiting = True
                waiting_days = 0

                gap_lower = row['High']
                gap_upper = row['candle1_low']
                positions.append(0)
            else:
                positions.append(0)

        self.data['bearish_fvg_position'] = positions

        self.data["bearish_fvg_returns"] = (self.data["Daily Return"]
                                            * self.data["bearish_fvg_position"].shift(1)).cumsum().apply(np.exp)

        title = "{} | Gap Size={}".format(self.ticker, self.gap_size)
        self.data[["Daily Return Buy and Hold", "bearish_fvg_returns"]].plot(title=title, figsize=(12, 8))

        # Print out our numerical comparisons
        self.__bearish_backtest_helper()