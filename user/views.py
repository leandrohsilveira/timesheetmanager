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
from django.utils.translation import ugettext as _
from django.views import generic

from base.forms import PermissionDeniedInfoMessageMixin, FormUpdateView
from history.forms import HistoryEntryMixin
from user.forms import UserCreateForm, UserUpdateForm


def index(request):
	return redirect("user:current_user_detail")

class UserHistoryEntryMixin(HistoryEntryMixin):
	def get_object_instance(self):
		form = self.get_form()
		if hasattr(form, "user"):
			return form.user
		elif hasattr(form, "instance"):
			return form.instance
		return None

	def get_history_parameters(self):
		form = self.get_form()
		user = None
		if hasattr(form, "user"):
			user = self.get_form().user
		elif hasattr(form, "instance"):
			user = self.get_form().instance

		return { "user_first_name": self.request.user.first_name, 'changed_user_first_name': user.first_name }

class CurrentUserHistoryEntryMixin(HistoryEntryMixin):
	def get_history_parameters(self):
		return { "user_first_name": self.request.user.first_name }

class UserSignUpView(SuccessMessageMixin, HistoryEntryMixin, generic.CreateView):
	model = User
	form_class = UserCreateForm
	success_url = reverse_lazy('user:current_user_detail')
	# Translators: user data successful create message
	success_message = _("user successfully created!")
	history_message_template = _("%(user_first_name)s has signed up.")

	def get_user(self):
		return self.get_form().instance

	def get_history_parameters(self):
		return { "user_first_name": self.get_form().instance.first_name }

class UserCreateView(PermissionDeniedInfoMessageMixin, UserHistoryEntryMixin, UserSignUpView):
	permission_required = "auth.add_user"
	permission_denied_message = _("create new users")
	history_message_template = _("%(user_first_name)s has created a new user named \"%(changed_user_first_name)s\".")

class UserUpdateView(PermissionDeniedInfoMessageMixin, SuccessMessageMixin, PermissionRequiredMixin, UserHistoryEntryMixin, generic.UpdateView):
	model = User
	form_class = UserUpdateForm
	permission_required = "auth.change_user"
	# Translators: user data successful update message
	success_message = _("the user data successfully updated!")
	context_object_name = "user_update"
	# Translators: permission description to access the user update view appeared on permission denied message
	permission_denied_message = _("change other users data")
	history_message_template = _("%(user_first_name)s has updated \"%(changed_user_first_name)s\" user's data.")

	def has_permission(self):
		if self.get_object().is_superuser:
			return False
		return super(UserUpdateView, self).has_permission()

	def get_success_url(self):
		return reverse_lazy('user:user_detail', kwargs = {"pk": self.object.id })


class UserDetailView(PermissionDeniedInfoMessageMixin, PermissionRequiredMixin, generic.DetailView):
	model = User
	permission_required = "auth.add_user"
	context_object_name = "user_detail"
	# Translators: permission description to access the user detail view appeared on permission denied message
	permission_denied_message = _("see other users data")
	def has_permission(self):
		if self.get_object().is_superuser:
			raise PermissionDenied(self.get_permission_denied_message())
		return super(UserDetailView, self).has_permission()


class UserPasswordUpdateView(SuccessMessageMixin, PermissionDeniedInfoMessageMixin, PermissionRequiredMixin, UserHistoryEntryMixin, FormUpdateView):
	model = User
	form_class = AdminPasswordChangeForm
	permission_required = "auth.change_user"
	template_name = "auth/password_change_form.html"
	# Translators: user password successful update message
	success_message = _("the user password successfully updated!")
	# Translators: permission description to access the user password update view appeared on permission denied message
	permission_denied_message = _("change other users password")
	history_message_template = _("%(user_first_name)s has updated \"%(changed_user_first_name)s\" user password.")

	def get_success_url(self):
		return reverse_lazy('user:user_detail', kwargs = {"pk": self.object.id })

	def get_form(self):
		return self.form_class(user = self.object, **self.get_form_kwargs())

	def form_valid(self, form):
		response = super(UserPasswordUpdateView, self).form_valid(form)
		update_session_auth_hash(self.request, form.user)
		return response

class CurrentUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, CurrentUserHistoryEntryMixin, generic.UpdateView):
	model = User
	form_class = UserUpdateForm
	success_url = reverse_lazy('user:current_user_detail')
	# Translators: current user data successful update message
	success_message = _("your user data were successfully updated!")
	context_object_name = "current_user_update"
	history_message_template = _("%(user_first_name)s has updated own user's data.")

	def get_object(self):
		return self.request.user

class CurrentUserDetailView(LoginRequiredMixin, generic.DetailView):
	model = User
	context_object_name = "current_user_detail"
	def get_object(self):
		return self.request.user

class CurrentUserPasswordUpdateView(SuccessMessageMixin, LoginRequiredMixin, CurrentUserHistoryEntryMixin, generic.FormView):
	template_name = "auth/password_change_form.html"
	form_class = PasswordChangeForm
	success_url = reverse_lazy("user:current_user_detail")
	# Translators: current user password successful update message
	success_message = _("your password were successfully updated!")
	history_message_template = _("%(user_first_name)s has updated own user's password.")

	def get_form(self):
		return self.form_class(user = self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self.request, form.user)
		return super(CurrentUserPasswordUpdateView, self).form_valid(form)

class UsersListView(PermissionRequiredMixin, PermissionDeniedInfoMessageMixin, generic.ListView):
	model = User
	permission_required = "auth.add_user"
	# Translators: permission description to access the all users list view appeared on permission denied message
	permission_denied_message = _("see all system users")

	paginate_by = 10

	def get_queryset(self):
		username = self.request.user.get_username()
		return User.objects.filter(is_superuser = False).exclude(username = username).order_by('-date_joined')


