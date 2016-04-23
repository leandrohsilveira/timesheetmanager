from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import register
from django.utils.translation import ugettext_lazy as _l


class MaterialdesignConfig(AppConfig):
	name = 'materialdesign'

@register.inclusion_tag(name = "mdl_field", filename = "tagtemplates/mdl_field.html")
def mdl_field(bound_field):
	bound_field.field.widget.attrs = {"class": "mdl-textfield__input"}
	readonly_encoded = False
	from django.contrib.auth.forms import ReadOnlyPasswordHashField
	if type(bound_field.field) is ReadOnlyPasswordHashField:
		readonly_encoded = True

	return {"bound_field": bound_field, "readonly_encoded": readonly_encoded}

@register.inclusion_tag(name = "mdl_messages", filename = "tagtemplates/mdl_messages.html")
def mdl_messages(messages):
	return {"messages": messages}

@register.inclusion_tag(name = "mdl_button", filename = "tagtemplates/mdl_button.html")
def mdl_button(text = "", href = None, link = None, icon = None, btype = "submit", bclass = "default", confirm_message = None):
	return { "text": text, "link": link, "icon": icon, "btype": btype, "bclass": bclass, "href": href, "confirm_message": confirm_message }

@register.inclusion_tag(name = "mdl_paginator", filename = "tagtemplates/mdl_paginator.html")
def mdl_paginator(page_obj, link = None, href = None, page_dist = 2):
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
