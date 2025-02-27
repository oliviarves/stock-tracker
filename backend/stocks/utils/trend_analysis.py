import numpy as np
import yfinance as yf
import pandas as pd


def fetch_stock_trends(ticker):
    """Fetch stock price trends and technical indicators."""
    stock = yf.Ticker(ticker)
    df = stock.history(period="2y", interval="1d", auto_adjust=True, actions=False)

    if df.empty:
        return None  # No data available

    df_weekly = df.resample('W-FRI').agg(
        {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})

    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    df_weekly['SMA_50_week'] = df_weekly['Close'].rolling(window=50).mean()
    df_weekly['SMA_200_week'] = df_weekly['Close'].rolling(window=200).mean()
    df_weekly['WMA_30_week'] = df_weekly['Close'].ewm(span=30, adjust=False).mean()  # Weighted MA

    df['RSI_14'] = compute_rsi(df['Close'], 14)

    new_high = df['Close'].iloc[-1] >= df['High'].rolling(window=52).max().iloc[-1]
    new_low = df['Close'].iloc[-1] <= df['Low'].rolling(window=52).min().iloc[-1]

    volume_spike = df['Volume'].iloc[-1] > df['Volume'].rolling(window=10).mean().iloc[-1] * 1.5

    rs_sp500 = compute_relative_strength(ticker, "SPY")

    return {
        "current_price": df['Close'].iloc[-1],
        "SMA_50": float(df['SMA_50'].iloc[-1]) if not np.isnan(df['SMA_50'].iloc[-1]) else None,
        "SMA_200": float(df['SMA_200'].iloc[-1]) if not np.isnan(df['SMA_200'].iloc[-1]) else None,
        "RSI_14": float(df['RSI_14'].iloc[-1]) if not np.isnan(df['RSI_14'].iloc[-1]) else None,
        "WMA_30_week": float(df_weekly['WMA_30_week'].iloc[-1]) if not np.isnan(
            df_weekly['WMA_30_week'].iloc[-1]) else None,
        "SMA_50_week": float(df_weekly['SMA_50_week'].iloc[-1]) if not np.isnan(
            df_weekly['SMA_50_week'].iloc[-1]) else None,
        "SMA_200_week": float(df_weekly['SMA_200_week'].iloc[-1]) if not np.isnan(
            df_weekly['SMA_200_week'].iloc[-1]) else None,
        "RS_SP500": float(rs_sp500) if not np.isnan(rs_sp500) else None,
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


def compute_relative_strength(stock_ticker, benchmark_ticker):
    """Calculate the relative strength of a stock compared to a benchmark (SPY)."""
    stock_data = yf.Ticker(stock_ticker).history(period="6mo")['Close']
    spy_data = yf.Ticker(benchmark_ticker).history(period="6mo")['Close']

    if stock_data.empty or spy_data.empty:
        return None

    rs = stock_data.pct_change().mean() / spy_data.pct_change().mean()
    return rs
