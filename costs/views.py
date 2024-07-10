from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Cost
from .serializers import CostSerializer

class CostListView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, _request, trip_id):
        costs = Cost.objects.filter(trip=trip_id)
        serialized_costs = CostSerializer(costs, many=True)
        return Response(serialized_costs.data, status=status.HTTP_200_OK) 
      
    def post(self, request, trip_id):
        request.data["trip"] = trip_id
        cost_to_add = CostSerializer(data=request.data)
        if cost_to_add.is_valid():
            cost_to_add.save()          
            return Response(cost_to_add.data, status=status.HTTP_201_CREATED)
        
        return Response(cost_to_add.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)    

class CostDetailView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get_cost(self, pk):
        try:
            return Cost.objects.get(pk=pk)
        except Cost.DoesNotExist:
            raise NotFound(detail="Can't find that cost!")
    
    def get(self, _request, pk):
        cost = self.get_cost(pk=pk)

        serialized_cost= CostSerializer(cost)
        return Response(serialized_cost.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        cost_to_edit = self.get_cost(pk=pk)

        updated_cost = CostSerializer(cost_to_edit, data=request.data)

        if updated_cost.is_valid():
            updated_cost.save()
            return Response(updated_cost.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(updated_cost.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        cost_to_delete = self.get_cost(pk=pk)

        cost_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)