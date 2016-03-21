"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'identity'

urlpatterns = [
	url('^', include('django.contrib.auth.urls')),
	url(r'^login/autenticar$', views.fazer_login, name = 'autenticar'),
	url(r'^login/sair$', views.fazer_logout, name = 'sair'),


	url(r'^$', login_required(views.VisualizarPessoaAutenticadaView.as_view()), name = 'index'),
	url(r'^usuario$', views.CadastrarPessoaView.as_view(), name = 'cadastrar_pessoa'),
	url(r'^usuario/cadastrar$', views.cadastrar_pessoa, name = 'salvar_nova_pessoa'),
	
	url(r'^usuario/salvar$', login_required(views.atualizar_pessoa_autenticada), name = 'salvar_pessoa_autenticada'),
	url(r'^usuario/visualizar$', login_required(views.VisualizarPessoaAutenticadaView.as_view()), name = 'visualizar_pessoa_autenticada'),
	url(r'^usuario/editar$', login_required(views.EditarPessoaAutenticadaView.as_view()), name = 'editar_pessoa_autenticada'),
	url(r'^usuario/remover$', login_required(views.remover_pessoa_autenticada), name = 'remover_pessoa_autenticada'),
	
    url(r'^usuarios/(?P<page>\d+)$', permission_required("identity.can_see_pessoas_list")(views.ListaPessoasView.as_view()), name = 'lista_pessoas'),
	url(r'^usuario/(?P<pk>\d+)/visualizar$', permission_required("identity.can_see_pessoas_list")(views.VisualizarPessoaView.as_view()), name = 'visualizar_pessoa'),
	
	url(r'^usuario/(?P<pk>\d+)$', permission_required('identity.can_change_pessoa')(views.EditarPessoaView.as_view()), name = 'editar_pessoa'),
	url(r'^usuario/(?P<pk>\d+)/salvar$', permission_required("identity.can_change_pessoa")(views.atualizar_pessoa), name = 'salvar_pessoa'),
	url(r'^usuario/(?P<pk>\d+)/remover$', permission_required("identity.can_delete_pessoa")(views.remover_pessoa), name = 'remover_pessoa'),

]
