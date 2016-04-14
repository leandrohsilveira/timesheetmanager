'''
Created on 14 de abr de 2016

@author: silveira
'''
from history import apps, views
from django.conf.urls import url
from base.site import BaseSiteConfig

class HistoryEntrySiteConfig(BaseSiteConfig):
	app_name = apps.app_name
	namespace = apps.namespace
	urls = [
		url(r'^$', views.index, name = 'index'),
		url(r'^(?P<pk>\d+)/delete$', views.delete_historyentry, name = 'historyentry_delete'),
		url(r'^list/(?P<page>\d+)/$', views.HistoryEntryListView.as_view(), name = 'historyentry_list'),
	]