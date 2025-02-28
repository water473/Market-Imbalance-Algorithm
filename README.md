# Market Imbalance Trading Algorithm/Strategy

Financial markets are filled with complexities and noise, where price action can seem completely random. Yet, beneath the surface, we can often observe price imbalances — moments when price moves quickly through an area with low liquidity. These  discrepancies, which traders have come to term **Fair Value Gaps (FVGs)**, offer a unique window into this supposed market inefficiency.

In this project I have attempted to use python to create a trading algorithm that is based on these Fair Value Gaps. I use historical price data (downloaded via [yfinance](https://pypi.org/project/yfinance/)) and python libraries such as pandas and numpy to generate trading signals for both bullish and bearish Fair Value Gaps, backtests the strategies, and compare the performance to a buy-and-hold benchmark.

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
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The **Simple FVG** strategy aims to exploit market imbalances by identifying periods where recent price action suggests that the market has deviated from its “fair value.”  
- **Bullish FVG:** A gap where the current candle’s low is significantly above the high of a candle two periods earlier.  
- **Bearish FVG:** A gap where the current candle’s high is significantly below the low of a candle two periods earlier.

For each signal, the algorithm enters a position and holds it for a predetermined period. In the bearish case, the strategy includes a waiting period for a retracement before entering a short position.

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
    git clone https://github.com/yourusername/simple-fvg-trading.git
    cd simple-fvg-trading
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

Import and instantiate the `SimpleFVG` class with your desired parameters. For example, to analyze SPY from 2010 to 2020 with a gap threshold of 10 points:

```
from SimpleFVG import SimpleFVG

# Initialize the strategy for SPY
strategy = SimpleFVG(ticker="SPY", start="2010-01-01", end="2020-01-01", gap_size=10)
```
### Running the Bullish FVG Backtest

To run a bullish backtest (entering long when a bullish FVG is identified and holding for a specified number of days):

```
# Run bullish FVG backtest with a 2-day holding period
strategy.bullish_fvg_backtest(holding_days=2)
```

### Running the Bearish FVG Backtest

The bearish strategy waits up to 3 days for a price retracement before entering a short position, then holds for a specified number of days:

```
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
  - For **Bullish FVG**, the strategy enters long immediately when the gap condition is met.
  - For **Bearish FVG**, it waits for a retracement before entering short.

- **Holding Period:**  
  Positions are held for a fixed number of days (e.g., 2 days) before exiting.

- **Return Calculations:**  
  Daily log returns are accumulated and exponentiated to yield cumulative returns, which are then compared with a buy-and-hold benchmark.

## Example Output

The backtest methods produce visual plots comparing the cumulative returns of the strategy with a buy-and-hold approach. For example, a plot might look like:

...

Additionally, the terminal output provides key performance metrics:
- Final cumulative returns
- Percentage returns
- Compound Annual Growth Rate (CAGR)

## Future Enhancements

- **Vectorized Backtesting:** Replace loops with vectorized operations for improved performance.
- **Advanced Risk Management:** Implement stop-loss, take-profit, and dynamic position sizing.
- **Live Trading Integration:** Extend the algorithm for paper or live trading environments.
- **Parameter Optimization:** Automate the tuning of gap thresholds, holding, and waiting periods.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests. For major changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or further information, please contact [dimitriosmah@gmail.com] or open an issue on GitHub.
