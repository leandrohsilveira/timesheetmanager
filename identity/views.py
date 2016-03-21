import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views import generic

from identity.models import Pessoa, Documento, TipoDocumento


class ListaPessoasView(generic.ListView):
	model = Pessoa
	paginate_by = 10
	queryset = Pessoa.objects.order_by('-usuario__date_joined')

class DadosPessoaAutenticadaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"
	def get_object(self):
		return get_object_or_404(Pessoa, usuario__username = self.request.user.username)
	
class VisualizarPessoaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"

class CadastrarPessoaView(generic.CreateView):
	model = Pessoa
	context_object_name = "pessoa"
	fields = ["usuario", "documento"]
	def get_context_data(self, **kwargs):
		context = super(CadastrarPessoaView, self).get_context_data(**kwargs)
		context['tipos_documentos'] = TipoDocumento.objects.all()
		return context

class AtualizarPessoaView(generic.UpdateView):
	model = Pessoa
	context_object_name = "pessoa"
	fields = ["usuario", "documento"]
	def get_context_data(self, **kwargs):
		context = super(AtualizarPessoaView, self).get_context_data(**kwargs)
		context['tipos_documentos'] = TipoDocumento.objects.all()
		return context

def fazer_login(request):
	username = request.POST["username"];
	password = request.POST["password"];
	nextUrl = request.POST["next"];

	user = authenticate(username = username, password = password);
	if user:
		if user.is_active:
			login(request, user);
			if nextUrl:
				return redirect(nextUrl);
			else:
				return redirect("identity:dados_pessoa_autenticada")
	return redirect("/identity/login?next=%s" % (nextUrl));

def fazer_logout(request):
	return logout_then_login(request);

def salvar_pessoa(request):
	p = request.POST["p"]
	if p:
		pessoa = Pessoa.objects.get(id = p)
		usuario = pessoa.usuario
		documento = pessoa.documento
	else:
		usuario = User()
		documento = Documento()
		pessoa = Pessoa()
		usuario.date_joined = timezone.now()
		usuario.username = request.POST['login']
		usuario.set_password(request.POST['senha'])

	documento.codigo = "".join(re.findall("\d+", request.POST['codigo']))
	documento.tipo_documento = TipoDocumento.objects.get(pk = request.POST['tipo_documento'])
	Documento.save(documento)

	usuario.is_active = True
	usuario.first_name = request.POST['primeiro_nome']
	usuario.last_name = request.POST['sobrenome']
	usuario.email = request.POST['email']
	User.save(usuario)

	if not pessoa.id:
		group = Group.objects.get(name = "Usuario")
		usuario.groups.add(group)
		User.save(usuario)

	pessoa.usuario = usuario
	pessoa.documento = documento
	Pessoa.save(pessoa)
	return redirect('identity:dados_pessoa_autenticada')

def remover_pessoa(request, pk):
	pessoa = Pessoa.objects.get(id = pk)
	if not pessoa.usuario.is_superuser:
		usuario = pessoa.usuario
		documento = pessoa.documento
		pessoa.delete()
		usuario.delete()
		documento.delete()
	return redirect("identity:lista_pessoas", page = 1)
