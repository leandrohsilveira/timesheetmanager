'''
Created on 14 de abr de 2016

@author: silveira
'''
from django.conf.urls import url, include
from user import views, apps
from history.apps import app_name
from base.site import BaseSiteConfig


class UserSiteConfig(BaseSiteConfig):
	app_name = apps.app_name
	namespace = apps.namespace
	urls = [
		url(r'^index$', views.index, name = 'index'),
	
		url(r'^', include('django.contrib.auth.urls')),
	
		url(r'^$', views.CurrentUserDetailView.as_view(), name = 'current_user_detail'),
		url(r'^signup$', views.UserSignUpView.as_view(), name = 'user_signup'),
		url(r'^new$', views.UserCreateView.as_view(), name = 'user_create'),
		url(r'^edit$', views.CurrentUserUpdateView.as_view(), name = 'current_user_update'),
		url(r'^password/$', views.CurrentUserPasswordUpdateView.as_view(), name = 'current_user_password_update'),
	
		url(r'^(?P<pk>\d+)/$', views.UserDetailView.as_view(), name = 'user_detail'),
		url(r'^(?P<pk>\d+)/edit$', views.UserUpdateView.as_view(), name = 'user_update'),
		url(r'^(?P<pk>\d+)/password/$', views.UserPasswordUpdateView.as_view(), name = 'user_password_update'),
		url(r'^list/(?P<page>\d+)/$', views.UsersListView.as_view(), name = 'users_list'),
	]