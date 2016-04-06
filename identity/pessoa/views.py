from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin, \
	LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from identity.pessoa.forms import UserCreateForm, UserUpdateForm


def add_permission_denied_message(request, permission_label):
	msg = "Seu usuário não tem permissão para acessar esta página. Informe abaixo as credenciais de um usuário que possui permissão para %s." % permission_label
	messages.info(request, msg)

class UserCreateView(generic.CreateView):
	model = User
	form_class = UserCreateForm
	success_url = reverse_lazy('identity:current_user_detail')

class CurrentUserUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = User
	form_class = UserUpdateForm
	success_url = reverse_lazy('identity:current_user_detail')
	def get_object(self):
		return self.request.user

class CurrentUserDetailView(LoginRequiredMixin, generic.DetailView):
	model = User
	def get_object(self):
		return self.request.user

class CurrentUserPasswordUpdateView(LoginRequiredMixin, generic.FormView):
	template_name = "auth/password_change_form.html"
	form_class = PasswordChangeForm
	success_url = reverse_lazy("identity:current_user_detail")

	def get_form(self):
		return self.form_class(user = self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self.request, form.user)
		messages.success(self.request, "Senha alterada com sucesso!")
		return super(CurrentUserPasswordUpdateView, self).form_valid(form)

class UsersListView(PermissionRequiredMixin, generic.ListView):
	model = User
	permission_required = "identity.can_see_pessoas_list"  # TODO:
	def handle_no_permission(self):
		add_permission_denied_message(self.request, "visualizar todos os usuários do sistema")
		return super(UsersListView, self).handle_no_permission()

	paginate_by = 10
	def get_queryset(self):
		username = self.request.user.get_username()
		return User.objects.exclude(is_superuser = False, username = username).order_by('-date_joined')
