from functools import wraps
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.models import Rol

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