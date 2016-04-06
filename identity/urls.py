"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include

from identity.pessoa import views


app_name = 'identity'

urlpatterns = [
	url(r'^$', views.CurrentUserDetailView.as_view(), name = 'index'),
	url('^', include('django.contrib.auth.urls')),
	url("^", include("identity.pessoa.urls")),
]
