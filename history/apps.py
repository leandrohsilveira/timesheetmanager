from django.apps import AppConfig
from base.apps import register_site

class HistoryConfig(AppConfig):
    name = 'history'

register_site(name = "history entries manager", icon = "history", reverseUrl = "history:index", perms = ["history.change_history"])
