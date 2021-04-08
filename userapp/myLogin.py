from rest_framework.views import APIView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm 
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.views import LoginView, LogoutView


from userapp.expiring_token import ExpiringTokenAuthentication


class Login(LoginView):  
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('profile')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        #auth_login(self.request, form.get_user())
        if token:    
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

class Logout(LogoutView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

