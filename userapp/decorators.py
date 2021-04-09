import requests
from functools import wraps
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.models import Rol
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from userapp.expiring_token import ExpiringTokenAuthentication


def token_venc(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        token = request.user.auth_token
        url = reverse('logouttoken')
        if token:
            token_expire = ExpiringTokenAuthentication()
            user, token, message = token_expire.authenticate_credentials(token)
            if message == 'Token expired':
                request.user.auth_token.delete()
                auth_logout(request)
                return HttpResponseRedirect(url)
         
        return view_func(request, *args, **kwargs)
    return wrapped_view

def email_verified(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        url = reverse('verfiedemail')
        
        if user.is_authenticated and user.user_verified == True:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(url)
    return wrapped_view
    
def verified_permission(flag):
    def _verified_permission(f):
        def wrapped_view(request, *args, **kwargs):
            url = reverse('permission_denied')

            try: 
                headers = {'Authorization': 'Token '+str(request.user.auth_token)}
                rol = requests.get('https://localhost:8000/api/rols/view-name/'+request.user.rol+'/', headers=headers, verify=False).json()
            except:
                return HttpResponseRedirect(url)

            if request.user.rol == 'invitado':
                return HttpResponseRedirect(url)
            
            band = permiso_a_int(flag)

            for x in rol['permisos']:
                if x == band:
                    return f(request, *args, **kwargs)
            
            return HttpResponseRedirect(url)
        return wrapped_view
    return _verified_permission


def permiso_a_int(flag):
    if flag == 'add_rol':
        flag = 4
    if flag == 'changue_rol':
        flag = 5
    if flag == 'delete_rol':
        flag = 6
    if flag == 'add_user':
        flag = 1
    if flag == 'delete_user':
        flag = 3
    if flag == 'changue_user':
        flag = 2
    
    return flag