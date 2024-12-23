# Automated Stock Selection and Backtest

This project is an automated framework designed to select stocks, construct portfolios, and backtest their performance over a 10-year period using four distinct strategies. It provides a systematic approach for financial research and analysis.

## Project Structure

The project comprises the following key components:

### 1. **Stock Selection**
The `stock_selection.py` script is responsible for:
- Selecting stocks to be used in the strategies.
- Leveraging specific filters and criteria to determine which stocks are eligible for portfolio inclusion.
- Passing the selected stocks to the portfolio construction process.

### 2. **Portfolio Construction**
The `portfolio_construction.py` script:
- Creates optimal portfolios based on the selected stocks.
- Implements portfolio allocation strategies to optimize returns.
- Calculates returns for the chosen period for four different strategies.

### 3. **Backtesting**
The `backtest.py` script:
- Utilizes the `stock_selection.py` script to run the algorithm across a 10-year historical period.
- Outputs the performance results for the four different strategies, including detailed metrics and insights.

## Features

- **Stock Selection**: Implements robust methodologies to filter and select stocks.
- **Portfolio Optimization**: Leverages various techniques to build and optimize portfolios.
- **Backtesting Framework**: Provides a comprehensive environment for testing strategies over long time horizons.
- **Performance Analysis**: Outputs key metrics for strategy evaluation and comparison.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/omersany002/automated_stock_selection_and_backtest.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the stock selection process:
   ```bash
   python stock_selection.py
   ```
4. Execute the backtest:
   ```bash
   python backtest.py
   ```

## Results

The backtesting process will generate outputs, including:
- Cumulative returns for each of the four strategies.
- Comparative performance metrics.
- Visualizations and reports summarizing the findings.

## Contributing
Contributions are welcome! Please feel free to fork the repository, submit issues, or create pull requests to improve the framework.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Feel free to explore the repository and modify the scripts to suit your own research and investment needs!

