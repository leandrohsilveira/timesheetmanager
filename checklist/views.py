from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _lazy
from django.views import generic

from base.forms import ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin, \
	ProductivEnvModelFormView, ProductivEnvDetailView
from checklist.models import Company


# Create your views here.
def get_or_none(model, *args, **kwargs):
	try:
		return model.objects.get(*args, **kwargs)
	except model.DoesNotExist:
		return None

@login_required
def index(request):
	company = get_or_none(Company, creator__id = request.user.id)
	if company:
		return redirect("checklist:company_detail")
	else:
		return redirect("checklist:company_create")

class CompanyDetailView(LoginRequiredMixin, ProductivEnvDetailView):
	model = Company
	view_id = "company_detail"
	view_name = "My Company"
	pattern = r'^$'

	def get_object(self, queryset = None):
		return get_or_none(Company, creator__id = self.request.user.id)


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, ProductivEnvLogEntryMixin, ProductivEnvHistoryEntryMixin, ProductivEnvModelFormView):
	model = Company
	view_id = "company_create"
	view_name = "New Company Form"
	pattern = r'^new$'
	fields = ("name",)
	success_url = reverse_lazy("checklist:index")
	success_message = _lazy("Company successfully created!")
	history_message_template = "%(user_first_name)s has created his own Company named %(company_name)s."

	def form_commit(self):
		self.object.creator = self.get_user()
		super(CompanyCreateView, self).form_commit()

	def get_message_parameters(self):
		return {
			"user_first_name": self.get_user().first_name,
			"company_name": self.get_current_object().name,
		}
