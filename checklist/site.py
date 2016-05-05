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
		url(r'^$', views.index, name = 'index'),
		url(r'^new$', views.CompanyCreateView.as_view(), name = "company_create")
	]
