from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RolSerializer
from .models import User, Rol

#
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
# 

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/user-list/',
        'Detail View': '/user-detail/<int:id>/',
        'Create': '/user-create/',
        'Update': '/user-update/<int:id>/',
        'Delete': '/user-delete/<int:id>/',
        'List-Rols': '/rol-list/',
        'Detail-rol': '/rol-datail/<int:id>',
        'Create-rol': '/rol-create/',
        'Update-rol': '/rol-update/<int:id>/',
        'Delete-rol': '/rol-delete/<int:id>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def showAll(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    

@api_view(['GET'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('¡User delete!.')

#
#
# methods Rol CRUD
#
#

@api_view(['GET'])
def showAllRols(request):
    rols = Rol.objects.all()
    serializer = RolSerializer(rols, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createRol(request):
    serializer = RolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def viewRol(request, pk):
    rol = Rol.objects.get(id=pk)
    serializer = RolSerializer(rol, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def updateRol(request, pk):
    rol = Rol.objects.get(id=pk)
    serializer = RolSerializer(instance=rol, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def deleteRol(request, pk):
    rol = Rol.objects.get(id=pk)
    rol.delete()
    return Response('¡Rol delete!.')

#
#
#   Login API
#
#

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
class Login(FormView):
    template_name = 'loginapi.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('user-list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login.self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)