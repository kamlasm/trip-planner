from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
import hashlib
import time

class CountryListView(APIView):
    def get(self, _request):        
        try: 
            response = requests.get('https://restcountries.com/v3.1/all')
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)

        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)

class CountryDetailView(APIView):  
    def get(self, _request, country):        
        try: 
            response = requests.get(f'https://restcountries.com/v3.1/name/{country}')
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)

        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)

class ExchangeRateView(APIView):     
    def get(self, _request):  
        try: 
            api_key = settings.EXCHANGE_RATE_API_KEY
            response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP')
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)

        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)   
        
class HotelView(APIView):
    def generate_signature(self, api_key, api_secret):
        timestamp = str(int(time.time()))
        signature = api_key + api_secret + timestamp
        hash_signature = hashlib.sha256(signature.encode()).hexdigest()
        return hash_signature

    def post(self, request):
        country = request.data['country']
        city = request.data['city']
        
        try: 
            response = requests.get(f'https://restcountries.com/v3.1/name/{country}')
            data = response.json()           
            countryCode = data[0]['cca2']
        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)
        
        api_key = settings.HOTELBEDS_API_KEY
        api_secret = settings.HOTELBEDS_API_SECRET
        hash_signature = self.generate_signature(api_key, api_secret)

        headers = {
            'Api-Key': api_key,
            'X-Signature': hash_signature,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        params = {
            'fields': 'all',
            'language': 'ENG',
            'from': 1,
            'to': 100,
            'countryCodes': countryCode
        }
        
        try:
            response = requests.get('https://api.test.hotelbeds.com/hotel-content-api/1.0/locations/destinations', headers=headers, params=params)
            data = response.json()
            destinations = data['destinations']
        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)       

        for destination in destinations:
            if destination.get('name') != None and destination['name']['content'] == city:
                destinationCode = destination['code']
                break

        params = {
            'destinationCode': destinationCode,
            'fields': 'all',
            'language': 'ENG',
            'from': 1,
            'to': 100,
        }
        
        try:
            response = requests.get('https://api.test.hotelbeds.com/hotel-content-api/1.0/hotels', headers=headers, params=params)
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except: 
            return Response(data.errors, status=status.HTTP_404_NOT_FOUND)  
