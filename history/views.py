from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.views import generic

from base.forms import PermissionDeniedInfoMessageMixin
from history.models import HistoryEntry


# Create your views here.
def index(request):
	return redirect("history:historyentry_list", page = 1)

class HistoryEntryListView(PermissionRequiredMixin, PermissionDeniedInfoMessageMixin, generic.ListView):
	model = HistoryEntry
	permission_required = "auth.change_user"
	# Translators: permission description to access the all users list view appeared on permission denied message
	permission_denied_message = "see all system history entries"

	paginate_by = 10

	def get_queryset(self):
		return self.model.objects.order_by('-event_time')

@permission_required(perm = "auth.change_user")
def delete_historyentry(request, pk):
	historyentry = get_object_or_404(HistoryEntry, pk = pk)
	HistoryEntry.delete(historyentry)
	messages.success(request, _("the history entry was successfully deleted!"))
	return redirect("history:index")
