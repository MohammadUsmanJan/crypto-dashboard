from rest_framework import serializers
from .models import Coin, PricePoint


class PricePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePoint
        fields = ['timestamp', 'price']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['cg_id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h', 'last_updated']


class CoinWithPricesSerializer(serializers.ModelSerializer):
    prices = PricePointSerializer(many=True)
    
    class Meta:
        model = Coin
        fields = '__all__'