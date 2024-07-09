from django.urls import path
from .views import CostDetailView

urlpatterns = [
    path('<int:pk>/', CostDetailView.as_view())
]