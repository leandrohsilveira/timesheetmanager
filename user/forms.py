'''
Created on 1 de abr de 2016

@author: Leandro
'''
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserCreateForm(auth_forms.UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')

class UserUpdateForm(auth_forms.UserChangeForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password')
	password = ReadOnlyPasswordHashField(label = _("Password"),
		help_text = _("Raw passwords are not stored, so there is no way to see "
					"this user's password, but you can change the password "
					"using <a href=\"password\">this form</a>."))
# 		help_text = _("Não são armazenadas senhas desprotegidas e, por isso, "
# 						"não há como visualizar a senha de um usuário, mas você "
# 						"pode alterá-la utilizando <a href=\"password\">este formulário</a>."))
