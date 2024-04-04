from rest_framework.views import APIView
from django.contrib.auth.models import User
from prueba.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

class UsersList(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many = True)

        
        return Response({"user":request.user.get_username(),"data":users_serializer.data}, status = status.HTTP_200_OK)


class SingUp(APIView):

    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            user = User.objects.get(username = request.data['username'])
            token = Token.objects.create(user = user)

            return Response({"user":user_serializer.data,
                             "token":token.key
                            }, status = status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
class Login(APIView):
    
    def post(self, request):
        user = get_object_or_404(User, username = request.data['username'])
        
        if not user.check_password(request.data['password']):
            return Response({"detail":"Not Found"}, status = status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user = user)
        user_serializer = UserSerializer(user)
        if created:
            return Response({"newToken": True, "token":token.key}, status = status.HTTP_201_CREATED)
        
        return Response({"user":user_serializer.data,
                             "token":token.key
                            }, status = status.HTTP_200_OK)


class LogOut(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)