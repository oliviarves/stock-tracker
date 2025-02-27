from django.db.models import Q, F

from stocks.models import Stock


def find_breakout_stocks():
    """
    Identify stocks that are showing strong technical breakout signals.
    """
    breakout_stocks = Stock.objects.filter(
        Q(current_price__gt=F("SMA_50")) &  # Price above 50-day MA
        Q(current_price__gt=F("SMA_200")) &  # Price above 200-day MA
        Q(RSI_14__gte=55) &  # RSI in bullish range
        Q(RSI_14__lte=70) &  # Avoid overbought zone
        Q(RS_SP500__gt=1) &  # Stronger than S&P 500
        Q(new_high=True) &  # Recently hit a new 52-week high
        Q(volume_spike=True)  # High trading volume
    )

    return breakout_stocks
