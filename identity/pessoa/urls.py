"identity.can_see_pessoas_list"#from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url

from identity.pessoa import views


urlpatterns = [

	url(r'^user$', views.CurrentUserDetailView.as_view(), name = 'current_user_detail'),
	url(r'^user/new$', views.UserCreateView.as_view(), name = 'user_create'),
	url(r'^user/edit$', views.CurrentUserUpdateView.as_view(), name = 'current_user_update'),
    url(r'^users/(?P<page>\d+)$', views.UsersListView.as_view(), name = 'users_list'),

	url(r'^password/$', views.CurrentUserPasswordUpdateView.as_view(), name = 'current_user_password_update'),
	
]
