from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stocks.models import Stock, Sector, Tag, StockList
import random


class Command(BaseCommand):
    help = 'Loads sample data for development'

    def handle(self, *args, **options):
        # Create test user if it doesn't exist
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
        else:
            user = User.objects.get(username='testuser')
            self.stdout.write(f'Using existing test user: {user.username}')

        # Create sectors
        sectors = [
            'Technology',
            'Healthcare',
            'Financial Services',
            'Consumer Cyclical',
            'Communication Services',
            'Industrials',
            'Consumer Defensive',
            'Energy',
            'Basic Materials',
            'Real Estate',
            'Utilities'
        ]

        sector_objects = []
        for sector_name in sectors:
            sector, created = Sector.objects.get_or_create(name=sector_name)
            sector_objects.append(sector)
            if created:
                self.stdout.write(f'Created sector: {sector.name}')
            else:
                self.stdout.write(f'Sector already exists: {sector.name}')

        # Create sample stocks
        sample_stocks = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'sector': 'Technology'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Communication Services'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Cyclical'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'sector': 'Communication Services'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Consumer Cyclical'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'sector': 'Technology'},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.', 'sector': 'Financial Services'},
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'sector': 'Healthcare'},
            {'symbol': 'V', 'name': 'Visa Inc.', 'sector': 'Financial Services'},
        ]

        for stock_data in sample_stocks:
            sector = Sector.objects.get(name=stock_data['sector'])
            stock, created = Stock.objects.get_or_create(
                symbol=stock_data['symbol'],
                defaults={
                    'name': stock_data['name'],
                    'sector': sector
                }
            )
            if created:
                self.stdout.write(f'Created stock: {stock.symbol} - {stock.name}')
            else:
                self.stdout.write(f'Stock already exists: {stock.symbol}')

        # Create sample tags
        tags = ['Dividend', 'Growth', 'Value', 'Blue Chip', 'Speculative', 'ESG', 'Small Cap', 'Large Cap']
        tag_objects = []

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
            else:
                self.stdout.write(f'Tag already exists: {tag.name}')

        # Assign random tags to stocks
        stocks = Stock.objects.all()
        for stock in stocks:
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(tag_objects, num_tags)
            stock.tags.set(selected_tags)
            self.stdout.write(f'Assigned {num_tags} tags to {stock.symbol}')

        # Create a watchlist for the test user
        watchlist, created = StockList.objects.get_or_create(
            name='Watchlist',
            user=user
        )
        if created:
            self.stdout.write(f'Created watchlist for {user.username}')

            # Add random stocks to watchlist
            watchlist_stocks = random.sample(list(stocks), 5)
            watchlist.stocks.set(watchlist_stocks)
            self.stdout.write(f'Added 5 stocks to {user.username}\'s watchlist')
        else:
            self.stdout.write(f'Watchlist already exists for {user.username}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))