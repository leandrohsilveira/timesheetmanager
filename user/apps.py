from django.apps import AppConfig
from base.apps import register_site
from history.apps import app_name

namespace = "user"
app_name = "user manager"

class UserConfig(AppConfig):
	name = 'user'

register_site(site_id = namespace, name = app_name, icon = "group", reverseUrl = "%s:index" % namespace)
