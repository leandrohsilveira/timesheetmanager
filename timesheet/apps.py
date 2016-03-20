from django.apps import AppConfig
from django.template.defaultfilters import register


class TimesheetConfig(AppConfig):
    name = 'timesheet'

@register.filter(name = 'mask')
def mask(value, arg):
	strValue = str(value)
	m = str(arg)
	for c in strValue:
		m = m.replace("X", c, 1)
	return m.replace("X", "");
