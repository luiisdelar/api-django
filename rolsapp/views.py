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
from userapp.decorators import email_verified, verified_permission, token_venc
# Create your views here.

@email_verified
@token_venc
def rols(request):
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}
    response = requests.get('https://localhost:8000/api/rols/', headers=headers, verify=False).json()
    return render(request, 'rols.html', {'response': response})

@email_verified
@verified_permission(flag='add_rol')
@token_venc
def createRol(request):
    if request.method == 'POST':
        miFormulario = FormRol(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data

            headers = {'Authorization': 'Token '+str(request.user.auth_token)}
            response = requests.post('https://localhost:8000/api/rols/create', data=datos, headers=headers, verify=False)            
            
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
@verified_permission(flag='changue_rol')
@token_venc
def editRol(request, pk):
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}
    rol = requests.get('https://localhost:8000/api/rols/view/'+str(pk)+'/', headers=headers, verify=False).json()
    
    if request.method == 'POST':
        miFormulario = FormRol(request.POST)
        if miFormulario.is_valid():
            datos = miFormulario.cleaned_data
            datos['permisos'] = rol['permisos']
            response = requests.put('https://localhost:8000/api/rols/update/'+str(pk)+'/', data=datos, headers=headers, verify=False)
            rol = requests.get('https://localhost:8000/api/rols/view/'+str(pk)+'/', headers=headers, verify=False).json()

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
@token_venc
def deleteRol(request, pk):
    if request.method == 'GET':
        headers = {'Authorization': 'Token '+str(request.user.auth_token)}
        response = requests.delete('https://localhost:8000/api/rols/delete/'+str(pk)+'/', headers=headers, verify=False)
        return render(request, 'delete-rol.html') 

@email_verified
@verified_permission(flag='changue_rol')
@token_venc
def permissionsRol(request, pk):
    headers = {'Authorization': 'Token '+str(request.user.auth_token)}
    rol = requests.get('https://localhost:8000/api/rols/view/'+str(pk)+'/', headers=headers, verify=False).json()
   
    dicc = {
        'add_user': False, 
        'changue_user': False,
        'delete_user': False,
        'add_rol': False, 
        'changue_rol': False,
        'delete_rol': False,
    }

    for permiso in rol['permisos']:
        if permiso == 1:
            dicc['add_user'] = True
        if permiso == 2:
            dicc['changue_user'] = True
        if permiso == 3:
            dicc['delete_user'] = True
        if permiso == 4:
            dicc['add_rol'] = True
        if permiso == 5:
            dicc['changue_rol'] = True
        if permiso == 6:
            dicc['delete_rol'] = True
    
    if request.method == 'POST':
        
        if request.POST.get('add_user') == 'on' and not dicc['add_user']:
            rol['permisos'].append(1)
            dicc['add_user'] = True
        if request.POST.get('add_user') == None and dicc['add_user']:
            dicc['add_user'] = False
            rol['permisos'].remove(1)
                
        if request.POST.get('changue_user') == 'on' and not dicc['changue_user']:
            rol['permisos'].append(2)
            dicc['changue_user'] = True
        if request.POST.get('changue_user') == None and dicc['changue_user']:
            dicc['changue_user'] = False
            rol['permisos'].remove(2)

        if request.POST.get('delete_user') == 'on' and not dicc['delete_user']:
            rol['permisos'].append(3)
            dicc['delete_user'] = True
        if request.POST.get('delete_user') == None and dicc['delete_user']:
            dicc['delete_user'] = False
            rol['permisos'].remove(3)

        if request.POST.get('add_rol') == 'on' and not dicc['add_rol']:
            rol['permisos'].append(4)
            dicc['add_rol'] = True
        if request.POST.get('add_rol') == None and dicc['add_rol']:
            dicc['add_rol'] = False
            rol['permisos'].remove(4)
                
        if request.POST.get('changue_rol') == 'on' and not dicc['changue_rol']:
            rol['permisos'].append(5)
            dicc['changue_rol'] = True
        if request.POST.get('changue_rol') == None and dicc['changue_rol']:
            dicc['changue_rol'] = False
            rol['permisos'].remove(5)    

        if request.POST.get('delete_rol') == 'on' and not dicc['delete_rol']:
            rol['permisos'].append(6)
            dicc['delete_rol'] = True
        if request.POST.get('delete_rol') == None and dicc['delete_rol']:
            dicc['delete_rol'] = False
            rol['permisos'].remove(6)
        
        datos={'name': rol['name'], 'permisos': rol['permisos']}
        response = requests.put('https://localhost:8000/api/rols/update/'+str(pk)+'/', data=datos, headers=headers, verify=False)
        exito = True
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc, 'exito': exito})
    else:
        return render(request, 'permissions-rol.html', {'rol': rol, 'permisos': dicc})