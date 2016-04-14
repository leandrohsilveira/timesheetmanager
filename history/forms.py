'''
Created on 13 de abr de 2016

@author: Leandro
'''
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.views import generic

from history.models import HistoryEntry


class HistoryEntryMixin:
	history_message_template = None

	def get_history_message_template(self):
		return self.history_message_template

	def get_object_instance(self):
		form = self.get_form()
		if hasattr(form, "instance"):
			return form.instance
		return None

	def get_history_parameters(self):
		if self.object:
			return {
				"content_type_name": ContentType.objects.get_for_model(self.get_object_instance()).name,
				"object_str": self.object.__str__()
			}
		return {}

	def get_user(self):
		return self.request.user

	def form_valid(self, form):
		response = super(HistoryEntryMixin, self).form_valid(form = form)
		HistoryEntry.objects.register_history_entry(
			user = self.get_user(),
			model_object = self.get_object_instance(),
			message = self.get_history_message_template(),
			parameters = self.get_history_parameters()
		)
		return response

class CreateHistoryEntryMixin(HistoryEntryMixin, generic.CreateView):
	history_message_template = _("created new %(content_type_name)s: \"%(object_str)s\".")

class UpdateHistoryEntryMixin(HistoryEntryMixin, generic.UpdateView):
	history_message_template = _("modified %(content_type_name)s: \"%(object_str)s\".")
