from django.contrib import admin
from .models import (
    StockImage, StockNote, StockEvaluation,
    SectorImage, SectorNote, SectorEvaluation
)

@admin.register(StockImage)
class StockImageAdmin(admin.ModelAdmin):
    list_display = ('stock', 'user', 'title', 'created_at')
    search_fields = ('stock__symbol', 'stock__name', 'user__username', 'title')
    list_filter = ('analysis_type', 'timeframe', 'user')

@admin.register(StockNote)
class StockNoteAdmin(admin.ModelAdmin):
    list_display = ('stock', 'user', 'title', 'created_at')
    search_fields = ('stock__symbol', 'stock__name', 'user__username', 'title', 'content')
    list_filter = ('user',)

@admin.register(StockEvaluation)
class StockEvaluationAdmin(admin.ModelAdmin):
    list_display = ('stock', 'user', 'rating')
    search_fields = ('stock__symbol', 'stock__name', 'user__username')
    list_filter = ('rating', 'user')

@admin.register(SectorImage)
class SectorImageAdmin(admin.ModelAdmin):
    list_display = ('sector', 'user', 'title', 'created_at')
    search_fields = ('sector__name', 'user__username', 'title')
    list_filter = ('analysis_type', 'user')

@admin.register(SectorNote)
class SectorNoteAdmin(admin.ModelAdmin):
    list_display = ('sector', 'user', 'title', 'created_at')
    search_fields = ('sector__name', 'user__username', 'title', 'content')
    list_filter = ('user',)

@admin.register(SectorEvaluation)
class SectorEvaluationAdmin(admin.ModelAdmin):
    list_display = ('sector', 'user', 'rating')
    search_fields = ('sector__name', 'user__username')
    list_filter = ('rating', 'user')