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
from userapp.decorators import email_verified, verified_permission
# Create your views here.

@email_verified
def rols(request):
    response = requests.get('http://127.0.0.1:8000/api/rols/').json()
    return render(request, 'rols.html', {'response': response})

@email_verified
@verified_permission(flag='add_rol')
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

@email_verified
@verified_permission(flag='change_rol')
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

@email_verified
@verified_permission(flag='delete_rol')
def deleteRol(request, pk):
    if request.method == 'GET':
        response = requests.delete('http://127.0.0.1:8000/api/rols/delete/'+str(pk)+'/')
        return render(request, 'delete-rol.html') 

@email_verified
@verified_permission(flag='changue_rol')
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
        if permiso.id == 4:
            dicc['add_rol'] = True
        if permiso.id == 5:
            dicc['change_rol'] = True
        if permiso.id == 6:
            dicc['delete_rol'] = True
        if permiso.id == 1:
            dicc['add_user'] = True
        if permiso.id == 2:
            dicc['change_user'] = True
        if permiso.id == 3:
            dicc['delete_user'] = True

    if request.method == 'POST':
        
        if request.POST.get('add_rol') == 'on':
            rol.permisos.add(4)
            dicc['add_rol'] = True
        else:
            rol.permisos.remove(4)
            dicc['add_rol'] = False

        if request.POST.get('change_rol') == 'on':
            rol.permisos.add(5)
            dicc['change_rol'] = True
        else:
            rol.permisos.remove(5)
            dicc['change_rol'] = False

        if request.POST.get('delete_rol') == 'on':
            rol.permisos.add(6)
            dicc['delete_rol'] = True
        else:
            rol.permisos.remove(6)
            dicc['delete_rol'] = False

        if request.POST.get('add_user') == 'on':
            rol.permisos.add(1)
            dicc['add_user'] = True
        else:
            rol.permisos.remove(1)
            dicc['add_user'] = False

        if request.POST.get('change_user') == 'on':
            rol.permisos.add(2)
            dicc['change_user'] = True
        else:
            rol.permisos.remove(2)
            dicc['change_user'] = False

        if request.POST.get('delete_user') == 'on':
            rol.permisos.add(3)
            dicc['delete_user'] = True
        else:
            rol.permisos.remove(3)
            dicc['delete_user'] = False

        rol.save()        
        exito = True
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc, 'exito': exito})
    else:
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc})