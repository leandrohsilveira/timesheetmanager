from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import register
from django.utils.translation import ugettext_lazy as _l

class BaseConfig(AppConfig):
	name = 'base'

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
