from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Trip
from .serializers import TripSerializer, PopulatedTripSerializer

class TripListView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        trips = Trip.objects.filter(owners=request.user.id)
        serialized_trips = TripSerializer(trips, many=True)        
        return Response(serialized_trips.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        trip_to_add = TripSerializer(data=request.data)
        if trip_to_add.is_valid():
            new_trip = trip_to_add.save()
            request.user.trips.add(new_trip.id)            
            return Response(trip_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(trip_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class TripDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_trip(self, pk):
        try:
            return Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise NotFound(detail="Oh no, can't find that trip!")
        
    def get(self, request, pk):
        trip = self.get_trip(pk=pk)

        if trip not in request.user.trips.all():
            raise PermissionDenied(detail="You don't have permission to view this trip.")

        serialized_trip = PopulatedTripSerializer(trip)
        return Response(serialized_trip.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        trip_to_edit = self.get_trip(pk=pk)

        if trip_to_edit not in request.user.trips.all():
            raise PermissionDenied(detail="You don't have permission to edit this trip.")        

        updated_trip = TripSerializer(trip_to_edit, data=request.data)

        if updated_trip.is_valid():
            updated_trip.save()
            return Response(updated_trip.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_trip.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        trip_to_delete = self.get_trip(pk=pk)

        if trip_to_delete not in request.user.trips.all():
            raise PermissionDenied(detail="You don't have permission to delete this trip.")      

        trip_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
