from django.urls import path
from .views import TripListView, TripDetailView, TripAddUser, TripRemoveUser
from costs.views import CostListView
from hotels.views import HotelListView

urlpatterns = [
    path('', TripListView.as_view()),
    path('<int:pk>/', TripDetailView.as_view()),
    path('<int:trip_id>/costs/', CostListView.as_view()),
    path('<int:trip_id>/hotels/', HotelListView.as_view()),
    path('<int:pk>/add-user/', TripAddUser.as_view()),
    path('<int:pk>/remove-user/', TripRemoveUser.as_view()),
]