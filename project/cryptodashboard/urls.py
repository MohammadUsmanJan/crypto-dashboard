from django.urls import path
from .views import TopCoinsView, CoinHistoryView, QAView


urlpatterns = [
path('coins/', TopCoinsView.as_view()),
path('coins/<str:cg_id>/history/', CoinHistoryView.as_view()),
path('qa/', QAView.as_view()),
]