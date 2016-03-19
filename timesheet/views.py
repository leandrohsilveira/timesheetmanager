from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic

from .models import Usuario, Pessoa, Documento, TipoDocumento


class ListaUsuariosView(generic.ListView):
	model = Usuario
	paginate_by = 10

class ListaUltimosUsuariosCadastradosView(generic.ListView):
	model = Usuario

	queryset = Usuario.objects.order_by('-data_criacao')[:5]

class VisualizarUsuarioView(generic.DetailView):
	model=Usuario
	context_object_name="usuario"

def remover_usuario(request, pk):
	usuario = Usuario.objects.get(id = pk)
	usuario.delete()
	return redirect("timesheet:lista_usuarios", page = 1)

def novo_usuario(request):
	usuario = Usuario()
	usuario.pessoa = Pessoa()
	usuario.pessoa.documento = Documento()
	tipos_documentos = TipoDocumento.objects.all()
	usuario.pessoa.documento.tipo_documento = tipos_documentos[0]
	return render(request, 'timesheet/usuario_form.html', {'usuario': usuario, 'tipos_documentos': tipos_documentos})

def cadastrar_usuario(request):
	usuario = Usuario()
	pessoa = Pessoa()
	documento = Documento()

	usuario.login = request.POST['login']
	usuario.senha = request.POST['senha']
	usuario.data_criacao = timezone.now()
	pessoa.nome = request.POST['nome']
	documento.codigo = request.POST['codigo']
	documento.tipo_documento = TipoDocumento.objects.get(pk=request.POST['tipo_documento'])

	Documento.save(documento)
	pessoa.documento = documento
	Pessoa.save(pessoa)
	usuario.pessoa = pessoa
	Usuario.save(usuario)
	return redirect('timesheet:visualizar_usuario', pk = usuario.id)
