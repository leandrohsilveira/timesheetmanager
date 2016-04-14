from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import register
from django.utils.translation import ugettext_lazy as _l
import logging

class BaseConfig(AppConfig):
	name = 'base'

_LOGGER = logging.getLogger("timesheetmanager.base.apps")

_available_sites = []

def request_available_sites(request):
	_LOGGER.debug(_available_sites)
	return { "request_available_sites": [site for site in _available_sites if site["has_permission"](request, site["perms"]) ] }

def request_current_site(request):
	current_site = None
	namespace = request.resolver_match.namespace
	for site in _available_sites:
		if site["site_id"] == namespace:
			current_site = site
	return {"request_current_site": current_site}

def register_site(site_id, name, icon, reverseUrl, perms = [], has_permission = lambda request, required_perms: not required_perms or request.user.has_perms(required_perms)):
	_available_sites.append({ "site_id": site_id, "name": name, "icon": icon, "reverseUrl": reverseUrl, "perms": perms, "has_permission": has_permission })

register_site(site_id="admin", name = "administration", icon = "cogs", reverseUrl = "admin:index", has_permission = lambda request, required_perms: request.user.is_staff)

def mapped_languages(request):
	return {"mapped_languages": ["pt-br", "en"]}

@register.filter(name = 'mask')
def mask(value, arg):
	strValue = str(value)
	m = str(arg)
	for c in strValue:
		m = m.replace("X", c, 1)
	return m.replace("X", "");

@register.inclusion_tag(name = "bootstrap_field", filename = "tagtemplates/bootstrap_field.html")
def bootstrap_field(bound_field):
	bound_field.field.widget.attrs = {"class": "form-control"}
	readonly_encoded = False
	from django.contrib.auth.forms import ReadOnlyPasswordHashField
	if type(bound_field.field) is ReadOnlyPasswordHashField:
		readonly_encoded = True

	return {"bound_field": bound_field, "readonly_encoded": readonly_encoded}

@register.inclusion_tag(name = "bootstrap_messages", filename = "tagtemplates/bootstrap_messages.html")
def bootstrap_messages(messages):
	return {"messages": messages}

@register.inclusion_tag(name = "bootstrap_button", filename = "tagtemplates/bootstrap_button.html")
def bootstrap_button(text = "", href = None, link = None, icon = None, btype = "submit", bclass = "default"):
	return {"text": text, "link": link, "icon": icon, "btype": btype, "bclass": bclass, "href": href}

@register.inclusion_tag(name = "icon_text", filename = "tagtemplates/icon_text.html")
def icon_text(icon, text = "", size = ""):
	return {"icon": icon, "text": text, "size": size}

@register.inclusion_tag(name = "campos_obrigatorios", filename = "tagtemplates/campos_obrigatorios.html")
def campos_obrigatorios():
	return {}

@register.inclusion_tag(name = "bootstrap_paginator", filename = "tagtemplates/bootstrap_paginator.html")
def bootstrap_paginator(page_obj, link = None, href = None, page_dist = 2):
	control_last_page = page_obj.number + page_dist
	if control_last_page > page_obj.paginator.num_pages:
		control_last_page = page_obj.paginator.num_pages
	first_page = page_obj.number - 1 - page_dist
	if control_last_page - 1 - (page_dist * 2) < first_page:
		first_page = control_last_page - 1 - (page_dist * 2)
	if first_page < 0:
		first_page = 0

	last_page = first_page + (page_dist * 2) + 1
	page_range = page_obj.paginator.page_range[first_page:last_page]
	if not link and not href:
		raise ImproperlyConfigured(_l("both arguments \"link\" and \"href\" shouldn't be None. Please provide a \"link\" or \"href\" argument."))
	return {"page_obj": page_obj, "link": link, "href": href, "page_range": page_range}
