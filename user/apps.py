from django.apps import AppConfig
from base.apps import register_site

class UserConfig(AppConfig):
	name = 'user'

register_site(name = "user manager", icon = "user", reverseUrl = "user:index")
