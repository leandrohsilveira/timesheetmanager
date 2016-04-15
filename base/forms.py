'''
Created on 13 de abr de 2016

@author: Leandro
'''
from django.contrib import messages
from django.contrib.admin import models as log_models
from django.contrib.auth.mixins import AccessMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as __, ugettext as _
from django.views import generic


class PermissionDeniedInfoMessageMixin(AccessMixin):
	message_template = _("access denied, please provide the credentials of a user who has permission to %s.")
	def handle_no_permission(self):
		message = self.get_permission_denied_message()
		if message:
			messages.info(self.request, self.message_template % message)
		return super(PermissionDeniedInfoMessageMixin, self).handle_no_permission()

class ViewIdMixin:
	view_id = None
	view_verbose_name = None

	def get_view_id(self):
		return self.view_id

	def get_view_verbose_name(self):
		return self.view_verbose_name

	def get_context_data(self, **kwargs):
		if hasattr(self, "get_context_data"):
			context_data = super(ViewIdMixin, self).get_context_data(**kwargs)
			view_id = self.get_view_id()
			if view_id:
				context_data["view_id"] = view_id
			view_verbose_name = self.get_view_verbose_name()
			if view_verbose_name:
				context_data["view_verbose_name"] = view_verbose_name
			return context_data
		else:
			raise ImproperlyConfigured(_("ViewIdMixin must be mixed with an class that has a 'get_context_data' method."))

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
