from django.shortcuts import render
import requests
from userapp.forms import FormUser
from django.contrib.auth.hashers import check_password
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.models import User, Rol
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth
# Create your views here.

def users(request):
    #token = Token.objects.get(user=request.user)
    #headers = {'Authorization': 'Token '+token.key}
    #datos = {'username': 'lalo', 'password':'lalo'}

    response = requests.get('http://127.0.0.1:8000/api/users/').json()
    return render(request, 'users.html', {'response': response})

def createUser(request):
    rols = Rol.objects.all()
    
    if request.method == 'POST':
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/v2/crear/', data=datos)            
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols, 'band': band, 'response': response})
        else:
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols})
    else:
        return render(request, 'create-user.html', {'rols': rols})


def deleteUser(request, pk):
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:8000/api/user-delete/'+str(pk)+'/')
        return render(request, 'delete.html')

def editUser(request, pk):
    user = User.objects.get(id=pk)
    rols = Rol.objects.all()

    if request.method == 'POST':
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/user-update/'+str(pk)+'/', data=datos)
            user = User.objects.get(id=pk)
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'edit-user.html', {'user': user, 'response': response.json(), 'band': band, 'rols': rols})
        else:
            return render(request, 'edit-user.html', {'user': user, 'form': miFormulario, 'rols': rols})
    
    return render(request, 'edit-user.html', {'user': user, 'rols': rols})