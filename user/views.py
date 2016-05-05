'''
Created on 8 de abr de 2016

@author: Leandro
'''

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.views import generic

from base.forms import PermissionDeniedInfoMessageMixin, BaseFormView, \
	UpdateFormMixin, ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin, \
	ProductivEnvModelFormView
from history.forms import HistoryEntryMixin
from user.forms import UserCreateForm, UserUpdateForm


def index(request):
	return redirect("user:current_user_detail")

class UserHistoryEntryMixin(ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin):

	def get_message_parameters(self):
		instance = self.get_current_object()
		return {
			"user_first_name": self.get_user().first_name if self.get_user().first_name else self.get_user().get_username(),
			'changed_user_first_name': instance.first_name if instance.first_name else instance.get_username()
		}

class CurrentUserHistoryEntryMixin(ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin):

	def get_message_parameters(self):
		return { "user_first_name": self.get_user().first_name if self.get_user().first_name else self.get_user().get_username() }


class UserSignUpView(SuccessMessageMixin, ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	view_id = "user_signup"
	view_name = _lazy("New user form")
	pattern = r'^signup$'
	form_class = UserCreateForm
	success_url = reverse_lazy('user:current_user_detail')
	# Translators: user data successful create message
	success_message = _lazy("user successfully created!")
	history_message_template = "%(user_first_name)s has signed up."

	def get_user(self):
		instance = self.get_current_object()
		if instance:
			return instance
		else:
			return super(UserSignUpView, self).get_user()

	def get_message_parameters(self):
		return { "user_first_name": self.get_user().first_name if self.get_user().first_name else self.get_user().get_username() }

class UserCreateView(PermissionDeniedInfoMessageMixin, SuccessMessageMixin, PermissionRequiredMixin, UserHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	view_id = "user_create"
	view_name = _lazy("New user form")
	pattern = r'^new$'
	form_class = UserCreateForm
	success_url = reverse_lazy('user:current_user_detail')
	# Translators: user data successful create message
	success_message = _lazy("user successfully created!")
	permission_required = "auth.add_user"
	permission_denied_message = _lazy("create new users")
	history_message_template = "%(user_first_name)s has created a new user named \"%(changed_user_first_name)s\"."

class UserUpdateView(PermissionDeniedInfoMessageMixin, SuccessMessageMixin, PermissionRequiredMixin, UserHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	view_id = "user_update"
	view_name = _lazy("%(first_name)s's user data")
	pattern = r'^(?P<pk>\d+)/edit$'
	form_class = UserUpdateForm
	permission_required = "auth.change_user"
	# Translators: user data successful update message
	success_message = _lazy("user data successfully updated!")
	# Translators: permission description to access the user update view appeared on permission denied message
	permission_denied_message = _lazy("change other users data")
	history_message_template = "%(user_first_name)s has updated \"%(changed_user_first_name)s\" user's data."

	def has_permission(self):
		if self.get_current_object().is_superuser:
			return False
		return super(UserUpdateView, self).has_permission()

	def get_success_url(self):
		return reverse_lazy('user:user_detail', kwargs = {"pk": self.object.id })

class UserDetailView(PermissionDeniedInfoMessageMixin, PermissionRequiredMixin, generic.DetailView):
	model = User
	permission_required = "auth.add_user"
	context_object_name = "user_detail"
	# Translators: permission description to access the user detail view appeared on permission denied message
	permission_denied_message = _lazy("see other users data")
	def has_permission(self):
		if self.get_object().is_superuser:
			raise PermissionDenied(self.get_permission_denied_message())
		return super(UserDetailView, self).has_permission()


class UserPasswordUpdateView(PermissionDeniedInfoMessageMixin, SuccessMessageMixin, PermissionRequiredMixin, UserHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	view_id = "user_password_update"
	view_name = _lazy("change password of %(first_name)s")
	pattern = r'^(?P<pk>\d+)/password$'
	form_class = AdminPasswordChangeForm
	permission_required = "auth.change_user"
	template_name = "auth/password_change_form.html"
	# Translators: user password successful update message
	success_message = _lazy("user password successfully updated!")
	# Translators: permission description to access the user password update view appeared on permission denied message
	permission_denied_message = _lazy("change other users password")
	history_message_template = "%(user_first_name)s has updated \"%(changed_user_first_name)s\" user password."

	def get_success_url(self):
		return reverse_lazy('user:user_detail', kwargs = {"pk": self.object.id })

	def get_form_kwargs(self):
		kwargs = super(UserPasswordUpdateView, self).get_form_kwargs()
		kwargs["user"] = kwargs["instance"]
		del kwargs["instance"]
		return kwargs

class CurrentUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, CurrentUserHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	view_id = "current_user_update"
	view_name = _lazy("my user")
	pattern = r'^edit$'
	form_class = UserUpdateForm
	success_url = reverse_lazy('user:current_user_detail')
	# Translators: current user data successful update message
	success_message = _lazy("your user data were successfully updated!")
	context_object_name = "current_user_update"
	history_message_template = "%(user_first_name)s has updated own user's data."

	def get_object(self):
		self.is_update = True
		return self.request.user

class CurrentUserDetailView(LoginRequiredMixin, generic.DetailView):
	model = User
	context_object_name = "current_user_detail"

	def get_object(self):
		return self.request.user

class CurrentUserPasswordUpdateView(SuccessMessageMixin, LoginRequiredMixin, CurrentUserHistoryEntryMixin, ProductivEnvModelFormView):
	model = User
	form_class = PasswordChangeForm
	template_name = "auth/password_change_form.html"
	view_id = "current_user_password_update"
	view_name = _lazy("change password")
	pattern = r'^password$'
	success_url = reverse_lazy("user:current_user_detail")
	# Translators: current user password successful update message
	success_message = _lazy("your password were successfully updated!")
	history_message_template = "%(user_first_name)s has updated own user's password."

	def get_object(self, *args, **kwargs):
		self.is_update = True
		return self.request.user

	def get_form_kwargs(self):
		kwargs = super(CurrentUserPasswordUpdateView, self).get_form_kwargs()
		kwargs["user"] = self.get_user()
		del kwargs["instance"]
		return kwargs

	def form_valid(self, form):
		response = super(CurrentUserPasswordUpdateView, self).form_valid(form)
		update_session_auth_hash(self.request, form.user)
		return response

class UsersListView(PermissionRequiredMixin, PermissionDeniedInfoMessageMixin, generic.ListView):
	model = User
	permission_required = "auth.add_user"
	# Translators: permission description to access the all users list view appeared on permission denied message
	permission_denied_message = _lazy("see all system users")

	paginate_by = 10

	def get_queryset(self):
		username = self.request.user.get_username()
		return User.objects.filter(is_superuser = False).exclude(username = username).order_by('-date_joined')


