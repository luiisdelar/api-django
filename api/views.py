from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RolSerializer, ForgotPasswordSerializer, RolNameSerializer
from .models import User, Rol 
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    
class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class ForgotPassword(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer


#
# rols
#
class RolList(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class RolView(generics.RetrieveAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class RolCreate(generics.CreateAPIView):
    serializer_class = RolSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class RolUpdate(generics.UpdateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class RolDelete(generics.DestroyAPIView):
    queryset = Rol.objects.all()
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)

class RolViewName(generics.RetrieveAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolNameSerializer
    lookup_field = 'name'
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
#
#  permisos
#