from django.apps import AppConfig
from django.template.defaultfilters import register


class IdentityConfig(AppConfig):
	name = 'identity'

@register.filter(name = 'mask')
def mask(value, arg):
	strValue = str(value)
	m = str(arg)
	for c in strValue:
		m = m.replace("X", c, 1)
	return m.replace("X", "");

@register.inclusion_tag(name = "bootstrap_field", filename="tagtemplates/bootstrap_field.html")
def bootstrap_field(bound_field):
	bound_field.field.widget.attrs = {"class": "form-control"}
	readonly_encoded = False
	from django.contrib.auth.forms import ReadOnlyPasswordHashField
	if type(bound_field.field) is ReadOnlyPasswordHashField:
		readonly_encoded = True

	return {"bound_field": bound_field, "readonly_encoded": readonly_encoded}

@register.inclusion_tag(name = "bootstrap_messages", filename="tagtemplates/bootstrap_messages.html")
def bootstrap_messages(messages):
	return {"messages": messages}

@register.inclusion_tag(name = "bootstrap_button", filename="tagtemplates/bootstrap_button.html")
def bootstrap_button(text="", href=None, link=None, icon=None, btype="submit", bclass="default"):
	return {"text": text, "link": link, "icon": icon, "btype": btype, "bclass": bclass, "href": href}

@register.inclusion_tag(name = "icon_text", filename="tagtemplates/icon_text.html")
def icon_text(icon, text="", size=""):
	return {"icon": icon, "text": text, "size": size}

@register.inclusion_tag(name = "campos_obrigatorios", filename = "tagtemplates/campos_obrigatorios.html")
def campos_obrigatorios():
	return {}
