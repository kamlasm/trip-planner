from django.urls import path
from .views import TripListView, TripDetailView

urlpatterns = [
    path('', TripListView.as_view()),
    path('<int:pk>/', TripDetailView.as_view()),
]