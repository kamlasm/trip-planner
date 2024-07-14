from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Hotel
from .serializers import HotelSerializer

class HotelListView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, _request, trip_id):
        hotels = Hotel.objects.filter(trip=trip_id)
        serialized_hotels = HotelSerializer(hotels, many=True)
        return Response(serialized_hotels.data, status=status.HTTP_200_OK) 
      
    def post(self, request, trip_id):
        request.data["trip"] = trip_id
        hotel_to_add = HotelSerializer(data=request.data)
        if hotel_to_add.is_valid():
            hotel_to_add.save()          
            return Response(hotel_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(hotel_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    

class HotelDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get_hotel(self, pk):
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise NotFound(detail="Can't find that hotel!")
    
    def get(self, _request, pk):
        hotel = self.get_hotel(pk=pk)

        serialized_hotel = HotelSerializer(hotel)
        return Response(serialized_hotel.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        hotel_to_edit = self.get_hotel(pk=pk)

        updated_hotel = HotelSerializer(hotel_to_edit, data=request.data)

        if updated_hotel.is_valid():
            updated_hotel.save()
            return Response(updated_hotel.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_hotel.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        hotel_to_delete = self.get_hotel(pk=pk)

        hotel_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)