'''
Created on 1 de abr de 2016

@author: Leandro
'''
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User


class UserCreateForm(auth_forms.UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')

class UserUpdateForm(auth_forms.UserChangeForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password')