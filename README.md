# Stock Trading Simulator

A simple command-line stock trading simulator built with Python that allows users to practice trading stocks with virtual money.

## Team

**Team Name**: Let Us Python

**Team Members**:
- Bhavya Garg
- Harshit Khattar

## Features

- **User Account Management**: Create and login to your personal trading account
- **Virtual Money**: Start with Rs.100,000 virtual cash to trade
- **Buy & Sell Stocks**: Trade real stocks using live market data
- **Portfolio Tracking**: View your holdings, profits/losses, and overall portfolio performance
- **Persistent Data**: All user data is saved locally and persists between sessions

## Libraries Used

### yfinance
- **Purpose**: Fetches real-time stock market data from Yahoo Finance
- **Functions Used**:
  - `yf.Ticker(symbol)`: Creates a ticker object for a stock
  - `stock.history(period='1d')`: Gets historical price data
- **Usage**: Retrieves current stock prices for buying/selling

### json
- **Purpose**: Handles data serialization for storing user information
- **Functions Used**:
  - `json.load()`: Reads user data from file
  - `json.dump()`: Saves user data to file
- **Usage**: Stores user accounts, portfolios, and transaction history

### os
- **Purpose**: Interacts with the operating system
- **Functions Used**:
  - `os.path.exists()`: Checks if users data file exists
- **Usage**: Verifies if the database file is present before loading

### getpass
- **Purpose**: Provides secure password input
- **Functions Used**:
  - `getpass()`: Hides password input from terminal
- **Usage**: Ensures passwords aren't visible when typing

## Installation

1. Install required library:
```bash
pip install yfinance
```

2. Run the program:
```bash
python main.py
```

## How to Use

1. **Create Account**: Register with a username and password
2. **Login**: Access your account with credentials
3. **View Portfolio**: Check your cash balance and stock holdings
4. **Buy Stocks**: Enter stock symbol (e.g., AAPL, TSLA) and quantity
5. **Sell Stocks**: Sell owned shares and see your profit/loss
6. **Logout**: Exit safely and all data is saved

## Data Storage

User data is stored in `users.json` with the following structure:
- Username and password
- Cash balance
- Stock portfolio (symbol, shares, buy price)

