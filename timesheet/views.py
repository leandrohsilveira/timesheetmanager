from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Usuario, Pessoa, Documento, TipoDocumento
from django.views import generic

# Create your views here.
class ListaUsuariosView(generic.ListView):
    context_object_name = 'usuarios'

    def get_queryset(self):
        """Return the last five published questions."""
        return Usuario.objects.order_by('-data_criacao')[:5]

class VisualizarUsuarioView(generic.DetailView):
	model=Usuario
	context_object_name="usuario"

def novo_usario(request):
	usuario = Usuario()
	usuario.pessoa = Pessoa()
	usuario.pessoa.documento = Documento()
	tipos_documentos = TipoDocumento.objects.all()
	usuario.pessoa.documento.tipo_documento = tipos_documentos[0]
	return render(request, 'timesheet/usuario_form.html', {'usuario': usuario, 'tipos_documentos': tipos_documentos, 'method': 'post'})

def salvar_usuario(request):
	pass
