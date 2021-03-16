from django import forms
from api.models import Rol

class FormRol(forms.Form):
    name = forms.CharField(max_length=30)
