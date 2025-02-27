import yfinance as yf
import pandas as pd


def fetch_stock_trends(ticker):
    """Fetch stock price trends and technical indicators."""
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")  # Last 6 months of data

    if df.empty:
        return None  # No data available

    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    df['RSI_14'] = compute_rsi(df['Close'], 14)

    new_high = df['Close'].iloc[-1] >= df['High'].rolling(window=52).max().iloc[-1]
    new_low = df['Close'].iloc[-1] <= df['Low'].rolling(window=52).min().iloc[-1]

    volume_spike = df['Volume'].iloc[-1] > df['Volume'].rolling(window=10).mean().iloc[-1] * 1.5

    return {
        "current_price": df['Close'].iloc[-1],
        "SMA_50": df['SMA_50'].iloc[-1],
        "SMA_200": df['SMA_200'].iloc[-1],
        "RSI_14": df['RSI_14'].iloc[-1],
        "new_high": new_high,
        "new_low": new_low,
        "volume_spike": volume_spike,
    }


def compute_rsi(series, period=14):
    """Compute Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
