from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

class HistoryEntryManager(models.Manager):

	def register_history_entry(self, user = None, model_object = None, message = None, parameters = None):
		user_id = None
		content_type_id = None
		object_id = None
		parameters_str = None

		if user:
			user_id = user.id

		if model_object:
			object_id = model_object.id
			content_type_id = ContentType.objects.get_for_model(model_object).id

		if parameters:
			parameters_str = parameters.__str__()

		self.model.objects.create(
            user_id = user_id,
            content_type_id = content_type_id,
            object_id = object_id,
            message_template = message,
            parameters = parameters_str,
        )

# Create your models here.
class HistoryEntry(models.Model):
	event_time = models.DateTimeField(
        _('event time'),
        default = timezone.now,
        editable = False,
    )
	user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name = _('user'),
    	null = True,
    	blank = True,
    	default = None
    )
	content_type = models.ForeignKey(
		ContentType,
		models.SET_NULL,
		verbose_name = _('content type'),
		blank = True,
		null = True,
	)
	object_id = models.IntegerField(_('object id'), blank = True, null = True)
	parameters = models.TextField(_('parameters'), blank = True, null = True, max_length = 255)
	message_template = models.TextField(_('message'), blank = True, null = True, max_length = 255)

	objects = HistoryEntryManager()

	def __str__(self):
		return self.get_event_message(default = _("no message recorded."))

	def get_event_message(self, default = None):
		if self.message_template:
			return _(self.message_template) % self.get_parameters_dict()
		else:
			return default

	def get_parameters_dict(self, default = {}):
		if self.parameters:
			return eval(self.parameters)
		else:
			return default

	def set_parameters(self, **kwargs):
		if kwargs:
			self.parameters = kwargs.__str__()
