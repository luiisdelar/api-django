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

            if request.user.rol == 'invitado':
                return HttpResponseRedirect(url)

            rol = Rol.objects.get(name=request.user.rol)
            
            for x in rol.permisos.all():
                if x.name == flag:
                    return f(request, *args, **kwargs)
            
            return HttpResponseRedirect(url)
        return wrapped_view
    return _verified_permission