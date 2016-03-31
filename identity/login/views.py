'''
Created on 21 de mar de 2016

@author: Leandro
'''
from django.contrib.auth import login
from django.contrib.auth.views import logout_then_login
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.views.generic.edit import FormView

from identity.login import forms as login_forms
from timesheetmanager import settings


class LoginView(FormView):
	form_class = login_forms.LoginForm
	template_name = "identity/login.html"
	
	def get_initial(self):
		initials = super(LoginView, self).get_initial()
		initials["next"] = self.request.GET.get("next", settings.LOGIN_REDIRECT_URL)
		return initials

	def form_valid(self, form):
		form.clean()
		login(self.request, form.get_user())
		redirect_to = self.request.POST.get("next")
		if not is_safe_url(url=redirect_to, host=self.request.get_host()):
			redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
			
		self.success_url = redirect_to
		return FormView.form_valid(self, form)

def fazer_logout(request):
	return logout_then_login(request);
