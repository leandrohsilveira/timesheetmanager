'''
Created on 2 de mai de 2016

@author: Leandro
'''
from django.conf.urls import url

from base.site import BaseSiteConfig
from checklist import apps, views


class ChecklistSiteConfig(BaseSiteConfig):
	app_name = apps.app_name
	namespace = apps.namespace
	urls = [
		url(r'^index$', views.index, name = 'index'),
		views.CompanyDetailView.as_url_import(),
		views.CompanyCreateView.as_url_import(),
	]
