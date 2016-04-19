from django.apps import AppConfig
from django.template.defaultfilters import register


class MaterialdesignConfig(AppConfig):
	name = 'materialdesign'

@register.inclusion_tag(name = "mdl_field", filename = "tagtemplates/mdl_field.html")
def mdl_field(bound_field):
	bound_field.field.widget.attrs = {"class": "form-control"}
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
