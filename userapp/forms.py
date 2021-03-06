from django import forms
from api.models import User

class FormUser(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    rol = forms.CharField(max_length=30)
    password = forms.CharField(max_length=80)
    confirm_password = forms.CharField(max_length=80)
    
    def clean(self):
        cleaned_data = super(FormUser, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password dont match")

class FormRegisterUser(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=30)
    confirm_password = forms.CharField(max_length=30)
    rol = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(FormRegisterUser, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password dont match") 

class FormForgotPassword(forms.Form):
    email = forms.EmailField()
    