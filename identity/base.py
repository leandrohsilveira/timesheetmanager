'''
Created on 6 de abr de 2016

@author: Leandro
'''
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as __, ugettext as _
from django.views import generic


class FormUpdateView(generic.FormView):
	object = None
	def get_object(self, *args, **kwargs):
		if not self.object:
			if not self.model:
				raise ImproperlyConfigured(_("The model atribute is required."))
			pk = kwargs.get("pk")
			if not pk:
				raise ImproperlyConfigured(_("A 'pk' kwarg is required."))
			return self.model.objects.get(**kwargs)
		return self.object

	def get(self, request, *args, **kwargs):
		self.object = self.get_object(*args, **kwargs)
		return super(FormUpdateView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(*args, **kwargs)
		return super(FormUpdateView, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FormUpdateView, self).get_context_data(**kwargs)
		context["object"] = self.object
		return context

	def form_valid(self, form):
		form.save()
		return super(FormUpdateView, self).form_valid(form)

class PermissionDeniedInfoMessageMixin(AccessMixin):
	message_template = __("access denied, please provide the credentials of a user who has permission to %s.")
	def handle_no_permission(self):
		message = self.get_permission_denied_message()
		if message:
			messages.info(self.request, self.message_template % message)
		return super(PermissionDeniedInfoMessageMixin, self).handle_no_permission()
