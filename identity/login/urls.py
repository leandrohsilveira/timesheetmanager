"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include

from identity.login import views

urlpatterns = [
	url('^', include('django.contrib.auth.urls')),
	url(r'^login/autenticar$', views.fazer_login, name = 'autenticar'),
	url(r'^login/sair$', views.fazer_logout, name = 'sair'),

]
