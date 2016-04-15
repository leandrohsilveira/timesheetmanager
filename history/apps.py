from django.apps import AppConfig
from base.apps import register_site


app_name = "history manager"
namespace = "history"

class HistoryConfig(AppConfig):
    name = namespace

register_site(site_id = namespace, name = app_name, icon = "history", reverseUrl = "%s:index" % namespace)
