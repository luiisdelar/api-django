from django.shortcuts import render
import requests
from rolsapp.forms import FormRol
from django.contrib.auth.hashers import check_password
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.models import Rol
from django.http import HttpResponse

# Create your views here.

def rols(request):
    response = requests.get('http://127.0.0.1:8000/api/rol-list/').json()
    return render(request, 'rols.html', {'response': response})

def createRol(request):
    if request.method == 'POST':
        miFormulario = FormRol(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/rol-create/', data=datos)            
            
            if response.status_code == 400:
                band = False
            else:
                band = True
                
            return render(request, 'create-rol.html', {'form': miFormulario, 'band': band, 'response': response.json()})
        else:
            return render(request, 'create-rol.html', {'form': miFormulario})
    else:
        return render(request, 'create-rol.html')

def editRol(request, pk):
    rol = Rol.objects.get(id=pk)
    
    if request.method == 'POST':
        miFormulario = FormRol(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/rol-update/'+str(pk)+'/', data=datos)
            rol = Rol.objects.get(id=pk)
            
            if response.status_code == 400:
                band = False
            else:
                band = True
            
            return render(request, 'edit-rol.html', {'rol': rol, 'response': response.json(), 'band': band})
        else:
            return render(request, 'edit-rol.html', {'rol': rol, 'form': miFormulario})
    
    return render(request, 'edit-rol.html', {'rol': rol})
    
def deleteRol(request, pk):
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:8000/api/rol-delete/'+str(pk)+'/')
        return render(request, 'delete-rol.html') 
        