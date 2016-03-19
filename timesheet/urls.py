#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url

from . import views


app_name = 'timesheet'

urlpatterns = [
	url(r'^$', views.ListaUltimosUsuariosCadastradosView.as_view(), name = 'lista_ultimos_usuarios_cadastrados'),
    url(r'^usuarios/(?P<page>\d+)$', views.ListaUsuariosView.as_view(), name = 'lista_usuarios'),
	url(r'^usuario/$', views.novo_usuario, name = 'novo_usuario'),
	# url(r'^usuario/(?P<pk>[0-9]+)$', views.editar_usuario, name='editar_usuario'),
	url(r'^usuario/(?P<pk>\d+)/visualizar$', views.VisualizarUsuarioView.as_view(), name = 'visualizar_usuario'),
	url(r'^usuario/(?P<pk>\d+)/remover', views.remover_usuario, name = 'remover_usuario'),
	url(r'^usuario/cadastrar$', views.cadastrar_usuario, name = 'cadastrar_usuario'),
	# url(r'^usuario/atualizar$', views.cadastrar_usuario, name='atualizar_usuario'),

]
