from django.urls import path
from .views import HotelDetailView

urlpatterns = [
    path('<int:pk>/', HotelDetailView.as_view())
]