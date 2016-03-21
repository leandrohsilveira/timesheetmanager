import re

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from identity.models import Pessoa, Documento, TipoDocumento


class CadastrarPessoaView(generic.CreateView):
	model = Pessoa
	context_object_name = "pessoa"
	fields = ["usuario", "documento"]
	def get_context_data(self, **kwargs):
		context = super(CadastrarPessoaView, self).get_context_data(**kwargs)
		context['tipos_documentos'] = TipoDocumento.objects.filter(documento_empresa = False)
		context['save_action'] = reverse('identity:salvar_nova_pessoa')
		return context
	
	
class VisualizarPessoaAutenticadaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"
	def get_object(self):
		return get_object_or_404(Pessoa, usuario__username = self.request.user.username)

class EditarPessoaAutenticadaView(generic.UpdateView):
	model = Pessoa
	context_object_name = "pessoa"
	fields = ["usuario", "documento"]
	
	def get_object(self):
		return get_object_or_404(Pessoa, usuario__username = self.request.user.username)
	
	def get_context_data(self, **kwargs):
		context = super(EditarPessoaAutenticadaView, self).get_context_data(**kwargs)
		context['tipos_documentos'] = TipoDocumento.objects.filter(documento_empresa = False)
		context['save_action'] = reverse('identity:salvar_pessoa_autenticada')
		return context

class VisualizarPessoaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"


class EditarPessoaView(generic.UpdateView):
	model = Pessoa
	context_object_name = "pessoa"
	fields = ["usuario", "documento"]
	def get_context_data(self, **kwargs):
		context = super(EditarPessoaView, self).get_context_data(**kwargs)
		context['tipos_documentos'] = TipoDocumento.objects.filter(documento_empresa = False)
		context['save_action'] = reverse('identity:salvar_pessoa', args=(context["pessoa"].id,))
		return context
	
class ListaPessoasView(generic.ListView):
	model = Pessoa
	paginate_by = 10
	queryset = Pessoa.objects.order_by('-usuario__date_joined')

def cadastrar_pessoa(request):
	usuario = User()
	usuario.is_active = True
	usuario.first_name = request.POST['primeiro_nome']
	usuario.username = request.POST['login']
	usuario.last_name = request.POST['sobrenome']
	usuario.set_password(request.POST['senha'])
	usuario.email = request.POST['email']
	User.save(usuario)
	usuario.groups.add(Group.objects.get(name = "Usuario"))
	User.save(usuario)
	documento = Documento()
	documento.codigo = "".join(re.findall("\d+", request.POST['codigo']))
	documento.tipo_documento = TipoDocumento.objects.get(pk = request.POST['tipo_documento'])
	Documento.save(documento)
	pessoa = Pessoa()
	pessoa.documento = documento
	pessoa.usuario = usuario
	Pessoa.save(pessoa)
	if pessoa.usuario.has_perm("identity.can_see_pessoas_list"):
		return redirect("identity:visualizar_pessoa", pk = pessoa.id)
	return redirect("identity:visualizar_pessoa_autenticada")

def atualizar_pessoa_autenticada(request):
	pessoa = get_object_or_404(Pessoa, usuario__username = request.user.username)
	__atualizar_pessoa(request, pessoa)
	return redirect('identity:visualizar_pessoa_autenticada')

def atualizar_pessoa(request, pk):
	pessoa = get_object_or_404(Pessoa, pk = pk)
	__atualizar_pessoa(request, pessoa)
	return redirect('identity:visualizar_pessoa', pk = pessoa.id)

def __atualizar_pessoa(request, pessoa):
	pessoa.documento.codigo = "".join(re.findall("\d+", request.POST['codigo']))
	pessoa.documento.tipo_documento = TipoDocumento.objects.get(pk = request.POST['tipo_documento'])
	pessoa.usuario.is_active = True
	pessoa.usuario.first_name = request.POST['primeiro_nome']
	pessoa.usuario.last_name = request.POST['sobrenome']
	pessoa.usuario.email = request.POST['email']
	User.save(pessoa.usuario)
	Documento.save(pessoa.documento)
	Pessoa.save(pessoa)


def remover_pessoa_autenticada(request):
	pessoa = get_object_or_404(Pessoa, usuario__username = request.user.username)
	__remover_pessoa(request, pessoa)
	return redirect("identity:login")

def remover_pessoa(request, pk):
	pessoa = get_object_or_404(Pessoa, pk = pk)
	__remover_pessoa(request, pessoa)
	return redirect("identity:lista_pessoas", page = 1)

def __remover_pessoa(request, pessoa):
	if not pessoa.usuario.is_superuser:
		usuario = pessoa.usuario
		documento = pessoa.documento
		pessoa.delete()
		usuario.delete()
		documento.delete()
