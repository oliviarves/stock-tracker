from django.db.models import Avg, Count, F, Case, When, IntegerField
from stocks.models import Stock, Sector, IndustryGroup

def rank_sectors():
    """Ranks broad sectors by average relative strength and uptrend percentage."""
    sector_stats = (
        Stock.objects.values("sector__name")
        .annotate(
            avg_rs=Avg("RS_SP500"),
            count_above_sma50=Count(Case(
                When(current_price__gt=F("SMA_50"), then=1),
                output_field=IntegerField()
            )),
            count_above_sma200=Count(Case(
                When(current_price__gt=F("SMA_200"), then=1),
                output_field=IntegerField()
            )),
            total_stocks=Count("id")
        )
        .order_by("-avg_rs")  # Rank by highest relative strength
    )
    return sector_stats

def rank_industry_groups():
    """Ranks industry groups (more specific than sectors) by strength."""
    industry_stats = (
        Stock.objects.values("industry_group__name", "sector__name")
        .annotate(
            avg_rs=Avg("RS_SP500"),
            count_above_sma50=Count(Case(
                When(current_price__gt=F("SMA_50"), then=1),
                output_field=IntegerField()
            )),
            count_above_sma200=Count(Case(
                When(current_price__gt=F("SMA_200"), then=1),
                output_field=IntegerField()
            )),
            total_stocks=Count("id")
        )
        .order_by("-avg_rs")
    )
    return industry_stats
