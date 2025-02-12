from django.shortcuts import render
from .serializers import (UserSerializers,
                          AuthTokenSerializers)
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import User
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
# Create your views here.

class RegisterView(generics.CreateAPIView):
    """User Register API"""
    serializer_class = UserSerializers

    # def post(self,request):
    #     serializer = UserSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return serializer.data

class LoginView(ObtainAuthToken):
    """CREATE TOKEN FOR THE REGISTER USER"""
    serializer_class = AuthTokenSerializers
    # def post(self,request):
        # email = request.data['email']
        # password = request.data['password']
        #
        # user = authenticate(username=email,password=password)
        # if user:
        #     token, created = Token.objects.get_or_create(user=user)
        #     result = {
        #         'token': token.key,
        #         'user_id': user.pk,
        #         'email': user.email
        #     }
        #     return Response(result,status=status.HTTP_201_CREATED)
        # else:
        #     return Response({"message":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializers

    def get_object(self):
        return self.request.user

    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     # print(User.objects.filter(id =pk))
    #     return User.objects.filter(id =pk)