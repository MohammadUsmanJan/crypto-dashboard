from django.db import models


class Coin(models.Model):
    # store the CoinGecko id for lookups (e.g., 'bitcoin')
    cg_id = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    current_price = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    total_volume = models.FloatField(null=True)
    price_change_percentage_24h = models.FloatField(null=True)
    last_updated = models.DateTimeField(null=True)


    def __str__(self):
        return self.name


class PricePoint(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField()
    price = models.FloatField()


    class Meta:
        ordering = ['timestamp']
        unique_together = ('coin', 'timestamp')


    def __str__(self):
        return f"{self.coin.symbol} @ {self.timestamp} = {self.price}"