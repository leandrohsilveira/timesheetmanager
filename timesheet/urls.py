from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
	url(r'^usuario/novo$', views.novo_usario, name='novo_usuario'),
	url(r'^usuario/salvar$', views.salvar_usuario, name='salvar_usuario'),
	url(r'^usuario/(?P<pk>[0-9]+)/$', views.VisualizarUsuarioView.as_view(), name='visualizar_usuario'),
]
