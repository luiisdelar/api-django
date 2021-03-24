from django.shortcuts import render
import requests
from rolsapp.forms import FormRol
from django.contrib.auth.hashers import check_password
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.models import Rol, User
from django.http import HttpResponse
from django.contrib.auth.models import Permission
# Create your views here.

def rols(request):
    response = requests.get('http://127.0.0.1:8000/api/rols/').json()
    return render(request, 'rols.html', {'response': response})

def createRol(request):
    if request.method == 'POST':
        miFormulario = FormRol(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/rols/create', data=datos)            
            
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
            response = requests.put('http://127.0.0.1:8000/api/rols/update/'+str(pk)+'/', data=datos)
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
        response = requests.delete('http://127.0.0.1:8000/api/rols/delete/'+str(pk)+'/')
        return render(request, 'delete-rol.html') 

def permissionsRol(request, pk):
    rol = Rol.objects.get(id=pk)
    permisos = rol.permisos.all()

    dicc = {
        'add_user': False, 
        'change_user': False,
        'delete_user': False,
        'add_rol': False, 
        'change_rol': False,
        'delete_rol': False,
    }

    for permiso in permisos:
        if permiso.id == 21:
            dicc['add_rol'] = True
        if permiso.id == 22:
            dicc['change_rol'] = True
        if permiso.id == 23:
            dicc['delete_rol'] = True
        if permiso.id == 25:
            dicc['add_user'] = True
        if permiso.id == 26:
            dicc['change_user'] = True
        if permiso.id == 27:
            dicc['delete_user'] = True

    
    #rol.permisos.add(25)    
    #rol.save()
     
    if request.method == 'POST':
        
        if request.POST.get('add_rol') == 'on':
            rol.permisos.add(21)
            dicc['add_rol'] = True
        else:
            rol.permisos.remove(21)
            dicc['add_rol'] = False

        if request.POST.get('change_rol') == 'on':
            rol.permisos.add(22)
            dicc['change_rol'] = True
        else:
            rol.permisos.remove(22)
            dicc['change_rol'] = False

        if request.POST.get('delete_rol') == 'on':
            rol.permisos.add(23)
            dicc['delete_rol'] = True
        else:
            rol.permisos.remove(23)
            dicc['delete_rol'] = False

        if request.POST.get('add_user') == 'on':
            rol.permisos.add(25)
            dicc['add_user'] = True
        else:
            rol.permisos.remove(25)
            dicc['add_user'] = False

        if request.POST.get('change_user') == 'on':
            rol.permisos.add(26)
            dicc['change_user'] = True
        else:
            rol.permisos.remove(26)
            dicc['change_user'] = False

        if request.POST.get('delete_user') == 'on':
            rol.permisos.add(27)
            dicc['delete_user'] = True
        else:
            rol.permisos.remove(27)
            dicc['delete_user'] = False

        rol.save()        
        exito = True
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc, 'exito': exito})
    else:
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc})