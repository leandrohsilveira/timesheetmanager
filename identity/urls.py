"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from identity.pessoa import views

def index(request):
	return redirect("identity:current_user_detail")

app_name = 'identity'

urlpatterns = [
	url(r'^$', index, name = 'index'),
	url('^', include('django.contrib.auth.urls')),
	url("^", include("identity.pessoa.urls")),
]

