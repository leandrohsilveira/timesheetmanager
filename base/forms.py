'''
Created on 13 de abr de 2016

@author: Leandro
'''
from django.contrib import messages
from django.contrib.admin import models as log_models
from django.contrib.auth.mixins import AccessMixin
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.utils.translation import ugettext_lazy as _lazy, ugettext as _
from django.views import generic
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from history.models import HistoryEntry


class ProductivEnvModelFormView(SingleObjectTemplateResponseMixin, generic.FormView):

	form_object_name = "object"
	fields = None
	model = None
	object = None
	is_update = None
	view_id = None
	view_name = None
	pattern = None
	context_object_name = "object"
	template_name_suffix = "_form"
	
	def get_current_object(self):
		form = self.get_form()
		if hasattr(form, self.form_object_name):
			return getattr(form, self.form_object_name)
		elif hasattr(form, "object"):
			return form.object
		elif hasattr(form, "instance"):
			return form.instance
		elif hasattr(self, self.form_object_name):
			return getattr(self, self.form_object_name)
		elif hasattr(self, "object"):
			return form.object
		elif hasattr(self, "instance"):
			return form.instance



	def get_form_class(self):
		"""
		Returns the form class to use in this view.
		"""
		if self.fields is not None and self.form_class:
			raise ImproperlyConfigured(
				"Specifying both 'fields' and 'form_class' is not permitted."
			)
		if self.form_class:
			return self.form_class
		else:
			if self.model is not None:
				# If a model has been explicitly provided, use it
				model = self.model
			elif hasattr(self, 'object') and self.object is not None:
				# If this view is operating on a single object, use
				# the class of that object
				model = self.object.__class__
			else:
				# Try to get a queryset and extract the model class
				# from that
				model = self.get_queryset().model

			if self.fields is None:
				raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )

			return model_forms.modelform_factory(model, fields = self.fields)
	
	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instantiating the form.
		"""
		kwargs = super(ProductivEnvModelFormView, self).get_form_kwargs()
		if hasattr(self, 'object'):
			kwargs.update({'instance': self.object})
		return kwargs

	def get_content_type(self):
		if not self.content_type:
			self.content_type = ContentType.objects.get_for_model(self, self.model)
		return self.content_type

	def __validate_configuration(self):
		messages = []
		if not self.model:
			messages.append("model is not defined")
		if not self.view_id:
			messages.append("view id is not defined")
		if not self.pattern:
			messages.append("pattern is not defined")
		if messages:
			raise ImproperlyConfigured("ProductivEnvModelFormView is not properly configured because of: %s" % (", ".join(messages)))

	def get_user(self):
		return self.request.user

	def get_object(self, *args, **kwargs):
		self.__validate_configuration()
		if self.is_update is None:
			if not self.model:
				raise ImproperlyConfigured(_("The model atribute is required."))
			pk = kwargs.get("pk")
			if pk:
				self.is_update = True
				self.object = self.model.objects.get(**kwargs)
			else:
				self.is_update = False
				self.object = None
		return self.object

	def get_context_data(self, **kwargs):
		kwargs[self.context_object_name] = self.object
		kwargs["view_id"] = self.view_id
		if self.view_name:
			kwargs["view_name"] = self.view_name
		return super(ProductivEnvModelFormView, self).get_context_data(**kwargs)

	def get(self, request, *args, **kwargs):
		self.__validate_configuration()
		self.object = self.get_object(*args, **kwargs)
		return super(ProductivEnvModelFormView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.__validate_configuration()
		self.object = self.get_object(*args, **kwargs)
		return super(ProductivEnvModelFormView, self).post(request, *args, **kwargs)

	def form_commit(self):
		self.model.save(self.object)

	def form_valid(self, form):
		self.__validate_configuration()
		self.object = form.save(commit = False)
		self.form_commit()
		return super(ProductivEnvModelFormView, self).form_valid(form)

class ProductivEnvLogEntryMixin:

	def form_commit(self):
		user = self.get_user()
		if user:
			super(ProductivEnvLogEntryMixin, self).form_commit()
			content_type = ContentType.objects.get_for_model(model = self.model)
			action_flag = log_models.ADDITION
			change_message = "created"
			if self.is_update:
				action_flag = log_models.CHANGE
				change_message = "updated"
			log_models.LogEntry.objects.log_action(
					user_id = user.id,
					content_type_id = content_type.pk,
					object_id = self.object.id,
					object_repr = self.object.__str__(),
					action_flag = action_flag,
					change_message = change_message)
		else:
			raise ImproperlyConfigured("ProductivEnvLogEntryMixin must identify an user to log the action.")

class ProductivEnvHistoryEntryMixin:

	history_message_template = None

	def get_message_template(self):
		return self.history_message_template

	def get_message_parameters(self):
		return {"user_first_name": self.get_user().first_name}

	def form_commit(self):
		super(ProductivEnvHistoryEntryMixin, self).form_commit()
		HistoryEntry.objects.register_history_entry(
			user = self.get_user(),
			model_object = self.object,
			message = self.get_message_template(),
			parameters = self.get_message_parameters()
		)

class PermissionDeniedInfoMessageMixin(AccessMixin):
	message_template = _lazy("access denied, please provide the credentials of a user who has permission to %(message)s.")
	def handle_no_permission(self):
		message = self.get_permission_denied_message()
		if message:
			messages.info(self.request, self.message_template % { "message": message })
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

class UpdateFormMixin:
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
		return super(BaseFormView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(*args, **kwargs)
		return super(BaseFormView, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(BaseFormView, self).get_context_data(**kwargs)
		context["object"] = self.object
		return context

class BaseFormView(generic.FormView):
	object = None
	model = None

	def before_save(self, instance):
		self.object = instance

	def after_save(self, instance):
		pass

	def form_valid(self, form):
		instance = form.save(commit = False)
		self.before_save(instance)
		self.model.save(instance)
		self.after_save(instance)
		return super(BaseFormView, self).form_valid(form)
