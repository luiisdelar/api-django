from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RolSerializer
from .models import User, Rol 
import requests
#
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)
 
class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class Login(FormView):  
    template_name = 'loginapi.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('user_list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

class Logout(APIView):
    def get(self, request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)


#
# roles
#
class RolList(generics.ListCreateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class RolCreate(generics.CreateAPIView):
    serializer_class = RolSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class RolUpdate(generics.UpdateAPIView):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

class RolDelete(generics.DestroyAPIView):
    queryset = Rol.objects.all()