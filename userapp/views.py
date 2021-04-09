from django.shortcuts import render, redirect
import requests
from userapp.forms import FormUser, FormRegisterUser, FormForgotPassword
from django.contrib.auth.hashers import check_password
import json
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from api.models import User, Rol
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth
from .decorators import email_verified, verified_permission, token_venc
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage

# Create your views here.

def verifiedEmail(request):
    verified = False
    if request.method == 'POST':
        if request.POST.get('verified_code') == request.user.verified_code:
            datos = {'username': request.user.username, 'password': request.user.password, 'user_verified': True}
            headers = {'Authorization': 'Token '+str(request.user.auth_token)}
            requests.put('https://localhost:8000/api/users/update/'+str(request.user.id)+'/', data=datos, verify=False, headers=headers)
            verified = True
        return render(request, 'verified-email.html', {'verified': verified})
    return render(request, 'verified-email.html')


@email_verified
@token_venc
def users(request):
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}    
    response = requests.get('https://localhost:8000/api/users/', verify=False, headers=headers).json()
    return render(request, 'users.html', {'response': response})
    
@email_verified
@verified_permission(flag='add_user')
@token_venc
def createUser(request): 
    
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}    
    rols = requests.get('https://localhost:8000/api/rols/', verify=False, headers=headers).json()
    
    if request.method == 'POST':
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data        
            response = requests.post('https://localhost:8000/api/users/create/', data=datos, verify=False, headers=headers)            
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols, 'band': band, 'response': response})
        else:
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols})
    else:
        if request.user.rol != 'admin':
            print(rols)
        return render(request, 'create-user.html', {'rols': rols})

def registerUser(request):
    band = True

    if request.method == 'POST':
        miFormulario = FormRegisterUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            
            response = requests.post('https://localhost:8000/api/users/create/', data=datos, verify=False)                        
            
            if response.status_code != 200 and response.status_code != 201:
                band = False

            return render(request, 'register.html', {'response': response, 'band': band, 'form': miFormulario})
        else:
            return render(request, 'register.html', {'band': band, 'form': miFormulario})
    else:
        return render(request, 'register.html')

@email_verified
@verified_permission(flag='delete_user')
@token_venc
def deleteUser(request, pk):
    if request.method == 'GET':
        headers = {'Authorization': 'Token '+str(request.user.auth_token)}
        requests.delete('https://localhost:8000/api/users/delete/'+str(pk)+'/', headers=headers,verify=False)
        return render(request, 'delete.html')

@email_verified
@verified_permission(flag='changue_user')
@token_venc
def editUser(request, pk):
  
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}
    user = requests.get('https://localhost:8000/api/users/view/'+str(pk)+'/', verify=False, headers=headers).json()
    rols = requests.get('https://localhost:8000/api/rols/', verify=False, headers=headers).json()

    if request.method == 'POST':
       
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            
            response = requests.put('https://localhost:8000/api/users/update/'+str(pk)+'/', data=datos, verify=False, headers=headers)
            user = requests.get('https://localhost:8000/api/users/view/'+str(pk)+'/', verify=False, headers=headers).json()
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'edit-user.html', {'userr': user, 'response': response.json(), 'band': band, 'rols': rols})
        else:
            return render(request, 'edit-user.html', {'userr': user, 'form': miFormulario, 'rols': rols})
    
    return render(request, 'edit-user.html', {'userr': user, 'rols': rols})

#probar con internet OOOOOOOJJJJJJOOOOOOOOO
def forgotPassword(request):
    error = False

    if request.method == 'POST':
        miFormulario = FormForgotPassword(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data

            try:
                response = requests.post('https://localhost:8000/api/users/forgot-password/', data=datos, verify=False)
            except:
                error = True 
            
            if response.status_code != 201:
                error = True
            return render(request, 'forgot-password.html', {'error': error})
        else:
            error = True
            return render(request, 'forgot-password.html', {'error': error})
        
    else:
        return render(request, 'forgot-password.html', {'error': error})


def profile(request):

    #si el user viene del login social se activa y se le asigna rol de invitado
    if request.user.is_authenticated and request.user.verified_code == None:
        headers = {'Authorization': 'Token '+str(request.user.auth_token)}
        datos = {'username': request.user.username, 'password': request.user.password,'rol': 'invitado', 'user_verified': True}
        requests.put('https://localhost:8000/api/users/update/'+str(request.user.id)+'/', data=datos, verify=False, headers=headers)
        
    return render(request, 'profile.html', {'userr': request.user})

def permission_denied(request):
    return render(request, 'permission-denied.html')

def token_expired(request):
    return render(request, 'token-expired.html')