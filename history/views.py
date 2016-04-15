from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, \
	LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _, gettext_lazy as _lazy
from django.views import generic

from base.forms import PermissionDeniedInfoMessageMixin, ViewIdMixin
from history.models import HistoryEntry


# Create your views here.
def index(request):
	return redirect("history:current_user_historyentry_list", page = 1)

class HistoryEntryListView(PermissionRequiredMixin, PermissionDeniedInfoMessageMixin, ViewIdMixin, generic.ListView):
	model = HistoryEntry
	view_id = "historyentry_list"
	view_verbose_name = _lazy("all history entries")
	permission_required = "auth.change_user"
	# Translators: permission description to access the all users list view appeared on permission denied message
	permission_denied_message = "see all system history entries"

	paginate_by = 10

	def get_queryset(self):
		return self.model.objects.order_by('-event_time')

class CurrentUserHistoryEntryListView(LoginRequiredMixin, ViewIdMixin, generic.ListView):
	model = HistoryEntry
	paginate_by = 20
	view_verbose_name = _lazy("my history entries")
	view_id = "current_user_historyentry_list"

	def get_queryset(self):
		return self.model.objects.filter(user__id = self.request.user.id).order_by('-event_time')

@permission_required(perm = "history.delete_historyentry")
def delete_historyentry(request, pk):
	historyentry = get_object_or_404(HistoryEntry, pk = pk)
	HistoryEntry.delete(historyentry)
	messages.success(request, _("the history entry was successfully deleted!"))
	return redirect("history:index")
