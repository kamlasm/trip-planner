from django.urls import path
from .views import TripListView, TripDetailView
from costs.views import CostListView

urlpatterns = [
    path('', TripListView.as_view()),
    path('<int:pk>/', TripDetailView.as_view()),
    path('<int:trip_id>/costs/', CostListView.as_view()),
]