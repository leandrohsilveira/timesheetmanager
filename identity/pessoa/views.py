from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, \
	AdminPasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin, \
	LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views import generic

from identity.base import PermissionDeniedInfoMessageMixin, FormUpdateView
from identity.pessoa.forms import UserCreateForm, UserUpdateForm


class UserCreateView(SuccessMessageMixin, generic.CreateView):
	model = User
	form_class = UserCreateForm
	success_url = reverse_lazy('identity:current_user_detail')
	# Translators: user data successful create message
	success_message = _("user successfully created!")

class UserUpdateView(PermissionDeniedInfoMessageMixin, SuccessMessageMixin, PermissionRequiredMixin, generic.UpdateView):
	model = User
	form_class = UserUpdateForm
	permission_required = "auth.change_user"
	# Translators: user data successful update message
	success_message = _("the user data successfully updated!")
	context_object_name = "user_update"
	# Translators: permission description to access the user update view appeared on permission denied message
	permission_denied_message = _("change other users data")

	def has_permission(self):
		if self.get_object().is_superuser:
			return False
		return super(UserUpdateView, self).has_permission()

	def get_success_url(self):
		return reverse_lazy('identity:user_detail', kwargs = {"pk": self.object.id })


class UserDetailView(PermissionDeniedInfoMessageMixin, PermissionRequiredMixin, generic.DetailView):
	model = User
	permission_required = "auth.change_user"
	context_object_name = "user_detail"
	# Translators: permission description to access the user detail view appeared on permission denied message
	permission_denied_message = _("see other users data")
	def has_permission(self):
		if self.get_object().is_superuser:
			raise PermissionDenied(self.get_permission_denied_message())
		return super(UserDetailView, self).has_permission()


class UserPasswordUpdateView(SuccessMessageMixin, PermissionDeniedInfoMessageMixin, PermissionRequiredMixin, FormUpdateView):
	model = User
	form_class = AdminPasswordChangeForm
	permission_required = "auth.change_user"
	template_name = "auth/password_change_form.html"
	# Translators: user password successful update message
	success_message = _("the user password successfully updated!")
	# Translators: permission description to access the user password update view appeared on permission denied message
	permission_denied_message = _("change other users password")

	def get_success_url(self):
		return reverse_lazy('identity:user_detail', kwargs = {"pk": self.object.id })

	def get_form(self):
		return self.form_class(user = self.object, **self.get_form_kwargs())

	def form_valid(self, form):
		response = super(UserPasswordUpdateView, self).form_valid(form)
		update_session_auth_hash(self.request, form.user)
		return response


class CurrentUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
	model = User
	form_class = UserUpdateForm
	success_url = reverse_lazy('identity:current_user_detail')
	# Translators: current user data successful update message
	success_message = _("your user data were successfully updated!")
	context_object_name = "current_user_update"

	def get_object(self):
		return self.request.user

class CurrentUserDetailView(LoginRequiredMixin, generic.DetailView):
	model = User
	context_object_name = "current_user_detail"
	def get_object(self):
		return self.request.user

class CurrentUserPasswordUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
	template_name = "auth/password_change_form.html"
	form_class = PasswordChangeForm
	success_url = reverse_lazy("identity:current_user_detail")
	# Translators: current user password successful update message
	success_message = _("your password were successfully updated!")

	def get_form(self):
		return self.form_class(user = self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self.request, form.user)
		return super(CurrentUserPasswordUpdateView, self).form_valid(form)

class UsersListView(PermissionRequiredMixin, PermissionDeniedInfoMessageMixin, generic.ListView):
	model = User
	permission_required = "auth.change_user"
	# Translators: permission description to access the all users list view appeared on permission denied message
	permission_denied_message = "see all system users"

	paginate_by = 10
	def get_queryset(self):
		username = self.request.user.get_username()
		return User.objects.filter(is_superuser = False).exclude(username = username).order_by('-date_joined')
