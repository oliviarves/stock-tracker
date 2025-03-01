import yfinance as yf
from stocks.models import Stock, Sector, IndustryGroup

def populate_stocks(symbols):
    """
    Fetches sector and industry data for given stock symbols and saves them to the database.
    """
    for symbol in symbols:
        try:
            stock_info = yf.Ticker(symbol).info
            sector_name = stock_info.get("sector", "Unknown")
            industry_name = stock_info.get("industry", "Unknown")
            company_name = stock_info.get("longName", symbol)

            # Get or create the sector
            sector, _ = Sector.objects.get_or_create(name=sector_name)

            # Get or create the industry group
            industry_group, _ = IndustryGroup.objects.get_or_create(name=industry_name, sector=sector)

            # Create the stock entry
            Stock.objects.update_or_create(
                symbol=symbol,
                defaults={"name": company_name, "sector": sector, "industry_group": industry_group},
            )
            print(f"Added: {symbol} - {company_name}")

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

# Example usage
def populate_example_stocks():
    stock_list = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN"]
    populate_stocks(stock_list)
