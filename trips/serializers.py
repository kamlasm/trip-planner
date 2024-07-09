from rest_framework import serializers
from .models import Trip
from jwt_auth.serializers import UserSerializer
from costs.serializers import CostSerializer

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        
class PopulatedTripSerializer(TripSerializer):
    owners = UserSerializer(many=True)
    costs = CostSerializer(many=True)