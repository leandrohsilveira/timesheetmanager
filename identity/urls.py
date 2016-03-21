#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'identity'

urlpatterns = [
	url('^', include('django.contrib.auth.urls')),
	url(r'^login/autenticar$', views.fazer_login, name = 'autenticar'),
	url(r'^login/sair$', views.fazer_logout, name = 'sair'),


	url(r'^$', login_required(views.DadosPessoaAutenticadaView.as_view()), name = 'index'),
    url(r'^usuarios/(?P<page>\d+)$', login_required(views.ListaPessoasView.as_view()), name = 'lista_pessoas'),
	url(r'^usuario$', views.CadastrarPessoaView.as_view(), name = 'cadastrar_pessoa'),
	url(r'^usuario/visualizar$', login_required(views.DadosPessoaAutenticadaView.as_view()), name = 'dados_pessoa_autenticada'),
# 	url(r'^usuario/editar$', views.AtualizarPessoaView.as_view(), name = 'editar_pessoa_autenticada'),
	url(r'^usuario/(?P<pk>\d+)$', views.AtualizarPessoaView.as_view(), name = 'editar_pessoa'),
	url(r'^usuario/(?P<pk>\d+)/visualizar$', permission_required("identity.can_see_pessoas_list")(views.VisualizarPessoaView.as_view()), name = 'visualizar_pessoa'),
	url(r'^usuario/(?P<pk>\d+)/remover', login_required(views.remover_pessoa), name = 'remover_pessoa'),
	url(r'^usuario/cadastrar$', views.salvar_pessoa, name = 'salvar_pessoa'),

]
