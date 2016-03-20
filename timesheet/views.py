import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import generic

from .models import Pessoa, Documento, TipoDocumento


class ListaPessoasView(generic.ListView):
	model = Pessoa
	paginate_by = 10
	queryset = Pessoa.objects.order_by('-usuario__date_joined')

class ListaUltimasPessoasCadastradasView(generic.ListView):
	model = Pessoa
	queryset = Pessoa.objects.order_by('-usuario__date_joined')[:5]

class DadosPessoaAutenticadaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"
	def get_object(self):
		return get_object_or_404(Pessoa, usuario__username = self.request.user.username)
	
class VisualizarPessoaView(generic.DetailView):
	model = Pessoa
	context_object_name = "pessoa"

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
				return redirect("timesheet:dados_pessoa_autenticada")
	return redirect("/timesheet/login?next=%s" % (nextUrl));

def fazer_logout(request):
	logout(request);
	return redirect("timesheet:dados_pessoa_autenticada");

def remover_pessoa(request, pk):
	pessoa = Pessoa.objects.get(id = pk)
	pessoa.delete()
	return redirect("timesheet:lista_pessoas", page = 1)

def nova_pessoa(request):
	pessoa = Pessoa()
	pessoa.pessoa = Pessoa()
	pessoa.pessoa.documento = Documento()
	tipos_documentos = TipoDocumento.objects.all()
	pessoa.pessoa.documento.tipo_documento = tipos_documentos[0]
	return render(request, 'timesheet/pessoa_form.html', {'pessoa': pessoa, 'tipos_documentos': tipos_documentos})

def cadastrar_pessoa(request):
	usuario = User()
	usuario.username = request.POST['login']
	usuario.set_password(request.POST['senha'])
	usuario.date_joined = timezone.now()
	usuario.first_name = request.POST['primeiro_nome']
	usuario.last_name = request.POST['sobrenome']
	usuario.email = request.POST['email']
	usuario.is_active = True
	User.save(usuario)

	group = Group.objects.get(name = "Usuario")
	usuario.groups.add(group)
	User.save(usuario)

	documento = Documento()
	documento.codigo = "".join(re.findall("\d+", request.POST['codigo']))
	documento.tipo_documento = TipoDocumento.objects.get(pk=request.POST['tipo_documento'])
	Documento.save(documento)

	pessoa = Pessoa()
	pessoa.usuario = usuario
	pessoa.documento = documento
	Pessoa.save(pessoa)
	return redirect('timesheet:dados_pessoa_autenticada')
