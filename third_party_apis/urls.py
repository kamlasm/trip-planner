from django.urls import path
from .views import CountryListView, CountryDetailView, ExchangeRateView, HotelView, FlightsView

urlpatterns = [
    path('countries/', CountryListView.as_view()),
    path('countries/<country>/', CountryDetailView.as_view()),
    path('exchange-rates/', ExchangeRateView.as_view()),
    path('hotels/', HotelView.as_view()),
    path('flights/', FlightsView.as_view()),
]