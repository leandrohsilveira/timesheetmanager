'''
Created on 31 de mar de 2016

@author: silveira
'''
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from identity.forms import bootstrap_field
from django.forms import widgets

class LoginForm(AuthenticationForm):
	next = forms.CharField(max_length=255, widget=widgets.HiddenInput)
	username = bootstrap_field(forms.CharField(label="Login", max_length=180))
	password = bootstrap_field(forms.CharField(label="Senha", widget=widgets.PasswordInput))