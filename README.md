# Market Imbalance Trading Algorithm/Strategy

Financial markets are filled with complexities and noise, where price action can seem completely random. Yet, beneath the surface, we can often observe price imbalances — moments when price moves quickly through an area with low liquidity. These discrepancies, which traders have come to term **Fair Value Gaps (FVGs)**, offer a unique window into this supposed market inefficiency. 

In this project I use python to create a trading algorithm that is based on these Fair Value Gaps. I use historical price data (downloaded via [yfinance](https://pypi.org/project/yfinance/)) and python libraries such as pandas and numpy to generate trading signals for both bullish and bearish Fair Value Gaps, backtest the strategies, and compare the performance to a buy-and-hold benchmark.

In the overview below, you'll find a clear, visual explanation of what a FVG is, making the concept accessible even to those new to stock charts and financial markets.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Initializing the Strategy](#initializing-the-strategy)
  - [Running the Bullish FVG Backtest](#running-the-bullish-fvg-backtest)
  - [Running the Bearish FVG Backtest](#running-the-bearish-fvg-backtest)
  - [Viewing the Data](#viewing-the-data)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Results](#results)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This idea of imbalances is best implemented using the typical candlestick price chart for a stock or whichever market you would like to explore.

Note: My **Simple FVG** strategy is mainly a retracement tool, meaning after we identify a fair value gap, ideally we would wait for price to retrace back into the gap before opening a position.

Before understanding a fair value gap, it is essential to understand the classic candlestick charts that financial analysts and investors use. Pictured below is the Apple stock chart on the 1 minute timeframe:

  ![image](https://github.com/user-attachments/assets/8307230a-6b5b-4a06-b2fa-c041ec8a73a1)
Each red and green candlestick represents the the high, low, open, and close of Apple's share price during that specific timeframe, which in this case is 1 minute.

  <img width="260" alt="image" src="https://github.com/user-attachments/assets/fd9453fc-89e3-496e-94fe-88e5f512dc13" />


Now let's see what exactly a "fair value gap" is:
- A fair value gap is a three candlestick pattern.
  - **Bullish FVG:** A gap where the current candle’s low is above the high of a candle two periods earlier.
    
    <img width="227" alt="image" src="https://github.com/user-attachments/assets/32d67b3c-a8e5-4969-a67d-a8905887e027" />

  - **Bearish FVG:** A gap where the current candle’s high is below the low of a candle two periods earlier.
    
    <img width="232" alt="image" src="https://github.com/user-attachments/assets/20264da8-4d9a-4088-927b-e4564436fd59" />

For each signal, the algorithm enters a position and holds it for a predetermined period. In the bearish case, the strategy includes a waiting period for a retracement before entering a short position.

### Why are these gaps important?
Fair value gaps tie into the overall concept of what some traders called "smart money". Smart money represents large institutions that have the power to influence markets with their access to an extreme amount of capital. For conciseness, I won't explain all the details here, but the general idea is that a FVG forms because at that price range, there was a lack of orders, or "liquidity", to push price in the opposing direction. Price is likely to retrace into this zone and then continue further in the original direction.

## Features

- **Data Downloading:** Retrieves historical data using `yfinance`.
- **Market Imbalance Detection:** Computes fair value gaps for bullish and bearish scenarios.
- **Stateful Backtesting:** Implements waiting and holding periods for trade entries.
- **Performance Metrics:** Calculates cumulative returns, percentage returns, and CAGR.
- **Visualization:** Plots strategy performance against a buy-and-hold benchmark.
- **Modular Design:** Encapsulated in a Python class for easy integration and further development.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Market-Imbalance-Algorithm
    cd Market-Imbalance-Algorithm
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Initializing the Strategy

Import and instantiate the `FairValueGap` class with your desired parameters. For example, to analyze SPY from 2010 to 2020 with a gap threshold of 10 points:

```python
from FairValueGap import SimpleFVG

# Initialize the strategy for SPY
strategy = SimpleFVG(ticker="SPY", start="2010-01-01", end="2020-01-01", gap_size=10)
```
### Running the Bullish FVG Backtest

To run a bullish backtest (entering long when a bullish FVG is identified and holding for a specified number of days):

```python
# Run bullish FVG backtest with a 2-day holding period
strategy.bullish_fvg_backtest(holding_days=2)
```

### Running the Bearish FVG Backtest

The bearish strategy waits up to 3 days for a price retracement before entering a short position, then holds for a specified number of days:

```python
# Run bearish FVG backtest with a 2-day holding period and a 3-day waiting period
strategy.bearish_fvg_backtest(holding_days=2, wait_days=3)
```

### Viewing the Data

Retrieve the processed dataset to further analyze or visualize it:

```
data = strategy.get_data()
print(data.head())
```

## How It Works

### Fair Value Gap (FVG)

- **Bullish FVG:**  
  Calculated as the difference between the current candle’s **Low** and the **High** from two periods earlier. A gap above the specified threshold indicates a bullish imbalance.

- **Bearish FVG:**  
  Calculated as the difference between the **Low** from two periods earlier and the current candle’s **High**. A gap above the threshold signals a bearish imbalance. The strategy waits for a retracement for up to 3 days before entering short.

### Trading Signals and Backtesting

- **Entry Signals:**  
  - For **Bullish FVG**, the strategy enters long immediately when the gap condition is met. This strategy only allows one position to be open at a time.
  - For **Bearish FVG**, it waits for a retracement before entering short. This strategy also only allows one position to be open at a time.

- **Holding Period:**  
  Positions are held for a fixed number of days (e.g., 2 days) before exiting and allowing another position to be opened.

- **Return Calculations:**  
  Daily log returns are accumulated and exponentiated to yield cumulative returns, which are then compared with a buy-and-hold benchmark.

## Example Output

The backtest methods produce visual plots comparing the cumulative returns of the strategy with a buy-and-hold approach. For example, a plot might look like:

![image](https://github.com/user-attachments/assets/b5801d99-6ac6-4fca-b20b-8902afc3cd37) 


Additionally, the terminal output provides key performance metrics:
- Final cumulative returns
- Percentage returns
- Compound Annual Growth Rate (CAGR)
For example, this would be outputed along with the above plot:
```Bullish FVG found on these dates
Price            gap
Date                
2010-09-02  1.922261
2010-11-05  1.663085
2010-12-02  1.509073
2011-09-27  2.104410
2011-10-24  1.539047
...
Final Buy and Hold Return: 6.812790315703157
Final Strategy Return: 7.43361295699954
Final Buy and Hold Percent Return: 581.28%
Final Strategy Percent Return: 643.36%
Buy-and-Hold CAGR: 13.66%
Strategy CAGR: 14.32%
```

**I have included an ipynb file that shows examples of using the FairValueGap class!**

## Results

- These are just the baby steps of a full trading algorithm that focuses on this idea of imbalances, but backtesting has been fun and insightful. 
  - When dealing with a trading algorithm, the goal is to have not only positive returns, but a return greater than some sort of benchmark, like for example the S&P 500. The reason for this is simply that if your algorithm yields let's say an 8% yearly return, but the S&P 500 averages 10%, there would be no reason to deploy the strategy. You would be better off buying and holding the S&P 500, taking on less risk.

- What I have found is that with the correct parameters, the bullish fair value gap strategy I created can actually outperform the S&P 500 buy and hold benchmark on historical data. The example back test in the .ipynb file I provided yields a 14.32% compounded annual growth rate (CAGR) on the S&P 500 as opposed to 13.66% with the buy and hold benchmark. This is on daily price data from 2010 to 2025. Overall that is a return of over 60% more over the 10 year period.

- The bearish fair value gap strategy has proven to be much less effective, and at the time I am writing this I haven't found parameters that make the strategy returns come even close to those of the benchmark.

**Disclaimer**: It is important to note that even though a back test may yield positive returns, that is NOT an indication that the strategy is ready to be deployed on the live markets - due to many potential issues such as overfitting, it takes much more to be ready to deploy an algorithm live, but these are the first steps!

## Future Enhancements

- **Vectorized Backtesting:** Replace loops with vectorized operations for improved performance.
- **Advanced Risk Management:** Implement stop-loss, take-profit, and dynamic position sizing.
- **Live Trading Integration:** Extend the algorithm for paper or live trading environments.
- **Parameter Optimization:** Automate the tuning of gap thresholds, holding, and waiting periods.
- **Strategy Combination:** Combine our bearish and bullish strategies to allow us to go long and short over time.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests. For major changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or further information, please contact [dimitriosmah@gmail.com] or open an issue on GitHub.
