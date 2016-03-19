from django import forms
from timesheet.models import TipoDocumento, Usuario

class UsuarioForm(forms.Form):
	nome = forms.CharField()
