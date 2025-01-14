from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer
import jwt

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)

        if user_to_create.is_valid():
            new_user = user_to_create.save()
            
            dt = datetime.now() + timedelta(days=7)
            
            token = jwt.encode(
            {'sub': new_user.id, 'exp': int(dt.strftime('%s')), 'username': new_user.username },
            settings.SECRET_KEY,
            algorithm='HS256'
            )
            return Response({'message': 'Registration successful', 'token': token}, status=status.HTTP_201_CREATED)

        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)

        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid credentials')
        
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid credentials')
        
        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode(
            {'sub': user_to_login.id, 'exp': int(dt.strftime('%s')), 'username': user_to_login.username },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f'Welcome back {user_to_login.username}'})