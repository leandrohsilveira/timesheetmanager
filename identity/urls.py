"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from identity.pessoa import views


app_name = 'identity'

urlpatterns = [
	url(r'^$', login_required(views.VisualizarPessoaAutenticadaView.as_view()), name = 'index'),
	url('^', include('django.contrib.auth.urls')),
	url("^", include("identity.pessoa.urls")),
]
