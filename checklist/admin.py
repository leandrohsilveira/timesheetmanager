from django.contrib import admin
from checklist.models import Teammate, Team, Invite, Company

# Register your models here.
admin.site.register(Company)
admin.site.register(Teammate)
admin.site.register(Team)
admin.site.register(Invite)
