from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coin, PricePoint
from .serializers import CoinSerializer, PricePointSerializer
from django.shortcuts import get_object_or_404
from dateutil import parser
from django.conf import settings
import re
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class TopCoinsView(APIView):

    @method_decorator(cache_page(60 * 2))   # cache for 2 minutes
    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        sort_by = request.GET.get('sort_by', 'market_cap')
        coins = Coin.objects.all().order_by(f"-{sort_by}")[:limit]
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)


class CoinHistoryView(APIView):
    
    @method_decorator(cache_page(60 * 2))
    def get(self, request, cg_id):
        days = int(request.GET.get('days', 30))
        coin = get_object_or_404(Coin, cg_id=cg_id)
        prices = coin.prices.order_by('timestamp')
        serializer = PricePointSerializer(prices, many=True)
        return Response({'coin': coin.cg_id, 'prices': serializer.data})




class QAView(APIView):
    
    def find_coin_in_query(self, query: str):
        """Try to find a coin from the DB based on query text."""
        coins = Coin.objects.all()
        for coin in coins:
            if coin.name.lower() in query or coin.symbol.lower() in query:
                return coin
        return None


    @method_decorator(cache_page(60 * 2)) 
    def get(self, request):
        query = request.GET.get("q", "").lower()
        print(query)

        coin = self.find_coin_in_query(query)
        if not coin:
            return Response({"answer": "Sorry, I couldn’t identify the coin in your query."})

        # 1. Current price
        if "price" in query:
            url = f"{settings.COINGECKO_API}/simple/price"
            params = {"ids": coin.cg_id, "vs_currencies": "usd"}
            resp = requests.get(url, params=params)
            data = resp.json()
            price = data.get(coin.cg_id, {}).get("usd")
            if price:
                return Response({"answer": f"{coin.name} ({coin.symbol.upper()}) price is ${price}"})

        # 2. Trend / market chart
        if "trend" in query or "chart" in query or "history" in query:
            url = f"{settings.COINGECKO_API}/coins/{coin.cg_id}/market_chart"
            params = {"vs_currency": "usd", "days": 7}
            resp = requests.get(url, params=params)
            return Response(resp.json())

        # 3. Market cap
        if "market cap" in query:
            url = f"{settings.COINGECKO_API}/coins/markets"
            params = {"vs_currency": "usd", "ids": coin.cg_id}
            resp = requests.get(url, params=params)
            data = resp.json()
            if data:
                return Response({"answer": f"{coin.name} market cap is ${data[0]['market_cap']}"})

        # 4. Volume
        if "volume" in query:
            url = f"{settings.COINGECKO_API}/coins/markets"
            params = {"vs_currency": "usd", "ids": coin.cg_id}
            resp = requests.get(url, params=params)
            data = resp.json()
            if data:
                return Response({"answer": f"{coin.name} 24h volume is ${data[0]['total_volume']}"})

        return Response({"answer": "Sorry, I couldn’t understand your query."})