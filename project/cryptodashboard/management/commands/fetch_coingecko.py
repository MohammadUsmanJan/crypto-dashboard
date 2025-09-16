from django.core.management.base import BaseCommand
from cryptodashboard.models import Coin, PricePoint
import requests, time
from datetime import datetime
from django.utils.dateparse import parse_datetime

COINGECKO_BASE = 'https://api.coingecko.com/api/v3'


class Command(BaseCommand):
    help = 'Fetch top coins and 30-day history from CoinGecko'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10)

    def fetch_with_retry(self, url, params=None, retries=3, delay=2):
        """Helper to fetch with retry + backoff if rate-limited"""
        for i in range(retries):
            resp = requests.get(url, params=params)
            if resp.status_code == 429:  # Too many requests
                self.stdout.write("Rate limited. Retrying...")
                time.sleep(delay * (i+1))  # exponential backoff
                continue
            resp.raise_for_status()
            return resp
        raise Exception(f"Failed to fetch {url} after retries")

    def handle(self, *args, **options):
        limit = options['limit']

        # 1) get top coins markets
        resp = self.fetch_with_retry(
            f"{COINGECKO_BASE}/coins/markets",
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
            },
        )
        data = resp.json()

        for item in data:
            cg_id = item['id']
            coin, _ = Coin.objects.update_or_create(
                cg_id=cg_id,
                defaults={
                    'symbol': item.get('symbol', ''),
                    'name': item.get('name', ''),
                    'current_price': item.get('current_price'),
                    'market_cap': item.get('market_cap'),
                    'total_volume': item.get('total_volume'),
                    'price_change_percentage_24h': item.get('price_change_percentage_24h'),
                    'last_updated': parse_datetime(item.get('last_updated'))
                    if item.get('last_updated')
                    else None,
                },
            )

            # 2) fetch market chart for 30 days (with retry + sleep)
            hist = self.fetch_with_retry(
                f"{COINGECKO_BASE}/coins/{cg_id}/market_chart",
                params={'vs_currency': 'usd', 'days': 30},
            )
            hdata = hist.json()
            prices = hdata.get('prices', [])  # list of [timestamp_ms, price]

            for ts_ms, price in prices:
                ts = datetime.utcfromtimestamp(ts_ms / 1000.0)
                PricePoint.objects.update_or_create(
                    coin=coin,
                    timestamp=ts,
                    defaults={'price': price},
                )

            time.sleep(1)  # prevent rate limiting

        self.stdout.write(self.style.SUCCESS('Fetched and stored coins'))
