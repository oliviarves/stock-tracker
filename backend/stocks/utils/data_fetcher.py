from stocks.models import Stock
from stocks.utils.trend_analysis import fetch_stock_trends
import yfinance as yf

def fetch_stock_data(ticker):
    """Fetch stock fundamentals and trends, then update the database."""
    stock = yf.Ticker(ticker)
    info = stock.info

    trends = fetch_stock_trends(ticker)

    stock_obj, created = Stock.objects.update_or_create(
        symbol=ticker,
        defaults={
            "name": info.get("longName", ticker),
            "current_price": trends["current_price"] if trends else None,
            "SMA_50": trends["SMA_50"] if trends else None,
            "SMA_200": trends["SMA_200"] if trends else None,
            "RSI_14": trends["RSI_14"] if trends else None,
            "WMA_30_week": trends["WMA_30_week"] if trends else None,
            "SMA_50_week": trends["SMA_50_week"] if trends else None,
            "SMA_200_week": trends["SMA_200_week"] if trends else None,
            "RS_SP500": trends["RS_SP500"] if trends else None,
            "new_high": trends["new_high"] if trends else False,
            "new_low": trends["new_low"] if trends else False,
            "volume_spike": trends["volume_spike"] if trends else False,
        }
    )

    return stock_obj
