from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RolSerializer
from .models import User, Rol 
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
 
class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    #authentication_classes = (TokenAuthentication,)

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

#
# rols
#
class RolList(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class RolCreate(generics.CreateAPIView):
    serializer_class = RolSerializer
    authentication_classes = (TokenAuthentication,)

class RolUpdate(generics.UpdateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    authentication_classes = (TokenAuthentication,)

class RolDelete(generics.DestroyAPIView):
    queryset = Rol.objects.all()
    authentication_classes = (TokenAuthentication,)