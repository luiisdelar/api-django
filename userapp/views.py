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
from .decorators import email_verified, verified_permission
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage

# Create your views here.

def verifiedEmail(request):
    user = User.objects.get(id=request.user.id)
    verified = False

    if request.method == 'POST':
        if request.POST.get('verified_code') == request.user.verified_code:
            user.user_verified = True
            user.save()
            verified = True
        return render(request, 'verified-email.html', {'verified': verified})
    return render(request, 'verified-email.html')

@email_verified
def users(request):
    #token = Token.objects.get(user=request.user)
    #headers = {'Authorization': 'Token '+token.key}
    
    response = requests.get('http://127.0.0.1:8000/api/users/').json()
    return render(request, 'users.html', {'response': response})
    
@email_verified
@verified_permission(flag='add_user')
def createUser(request): 
    rols = Rol.objects.all()
    
    if request.method == 'POST':
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/users/create/', data=datos)            
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols, 'band': band, 'response': response})
        else:
            return render(request, 'create-user.html', {'form': miFormulario, 'rols': rols})
    else:
        return render(request, 'create-user.html', {'rols': rols})

def registerUser(request):
    band = True

    if request.method == 'POST':
        miFormulario = FormRegisterUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            
            response = requests.post('http://127.0.0.1:8000/api/users/create/', data=datos)                        
            
            if response.status_code != 200 and response.status_code != 201:
                band = False

            return render(request, 'register.html', {'response': response, 'band': band, 'form': miFormulario})
        else:
            return render(request, 'register.html', {'band': band, 'form': miFormulario})
    else:
        return render(request, 'register.html')

@email_verified
@verified_permission(flag='delete_user')
def deleteUser(request, pk):
    if request.method == 'GET':
        response = requests.delete('http://127.0.0.1:8000/api/users/delete/'+str(pk)+'/')
        return render(request, 'delete.html')

@email_verified
@verified_permission(flag='changue_user')
def editUser(request, pk):
    user = User.objects.get(id=pk)
    rols = Rol.objects.all()

    if request.method == 'POST':
       
        miFormulario = FormUser(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data

            response = requests.put('http://127.0.0.1:8000/api/users/update/'+str(pk)+'/', data=datos)
            user = User.objects.get(id=pk)
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'edit-user.html', {'userr': user, 'response': response.json(), 'band': band, 'rols': rols})
        else:
            return render(request, 'edit-user.html', {'user': user, 'form': miFormulario, 'rols': rols})
    
    return render(request, 'edit-user.html', {'userr': user, 'rols': rols})

#probar con internet OOOOOOOJJJJJJOOOOOOOOO
def forgotPassword(request):
    error = False

    if request.method == 'POST':
        miFormulario = FormForgotPassword(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
        
            try:
                user = User.objects.get(email=datos['email'])
                new_pass = get_random_string(length=10)
                user.set_password(new_pass)
                user.save()
                body = 'Su nueva contraseña es: '+new_pass
                email = EmailMessage('Restauración de contraseña', body, to=[user.email])
                email.send()
            except:
                error = True 
                user = None
            
            return render(request, 'forgot-password.html', {'user_': user, 'error': error})
        else:
            error = True
            return render(request, 'forgot-password.html', {'error': error})
        
    else:
        return render(request, 'forgot-password.html', {'error': error})

def profile(request):
    return render(request, 'profile.html', {'userr': request.user})

def permission_denied(request):
    return render(request, 'permission-denied.html')