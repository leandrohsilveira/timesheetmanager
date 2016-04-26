'''
Created on 14 de abr de 2016

@author: silveira
'''
from django.conf.urls import include

class BaseSiteConfig:
	app_name = None
	namespace = None
	urls = []
	
	@classmethod
	def as_include(cls):
		instance = cls()
		return include(instance.urls, namespace=instance.namespace, app_name=instance.app_name)