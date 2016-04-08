"""timesheetmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns, urlpatterns as i18n_urlpatterns
from django.contrib import admin
from identity import views as identity_views
from identity.pessoa import views as user_views

user_urls = [
	url(r'^$', user_views.CurrentUserDetailView.as_view(), name = 'current_user_detail'),
	url(r'^new$', user_views.UserCreateView.as_view(), name = 'user_create'),
	url(r'^edit$', user_views.CurrentUserUpdateView.as_view(), name = 'current_user_update'),
	url(r'^password/$', user_views.CurrentUserPasswordUpdateView.as_view(), name = 'current_user_password_update'),

	url(r'^(?P<pk>\d+)/$', user_views.UserDetailView.as_view(), name = 'user_detail'),
	url(r'^(?P<pk>\d+)/edit$', user_views.UserUpdateView.as_view(), name = 'user_update'),
	url(r'^(?P<pk>\d+)/password/$', user_views.UserPasswordUpdateView.as_view(), name = 'user_password_update'),

    url(r'^list/(?P<page>\d+)$', user_views.UsersListView.as_view(), name = 'users_list'),
]

identity_urls = [

	url(r'^index$', identity_views.index, name = 'index'),

	url(r'^', include('django.contrib.auth.urls')),

	url(r'^', include(user_urls))

]

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
	url(r'^user/', include(identity_urls, namespace = 'identity')),
	url(r'^i18n/', include(i18n_urlpatterns, namespace = 'language')),

)
