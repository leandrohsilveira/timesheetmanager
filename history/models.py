from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy as _lazy

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
	class Meta:
		verbose_name = _lazy("history entry")
		verbose_name_plural = _lazy("history entries")
	event_time = models.DateTimeField(
        _lazy('event time'),
        default = timezone.now,
        editable = False,
    )
	user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name = _lazy('user'),
    	null = True,
    	blank = True,
    	default = None
    )
	content_type = models.ForeignKey(
		ContentType,
		models.SET_NULL,
		verbose_name = _lazy('content type'),
		blank = True,
		null = True,
	)
	object_id = models.IntegerField(_lazy('object id'), blank = True, null = True)
	parameters = models.TextField(_lazy('parameters'), blank = True, null = True, max_length = 255)
	message_template = models.TextField(_lazy('message'), blank = True, null = True, max_length = 255)

	objects = HistoryEntryManager()

	def __str__(self):
		return _("HistoryEntry< id: %(pk)d, message_template: %(message_template)s, parameters: %(parameters)s, content_type: %(content_type)s. >") % {
					"pk": self.id,
					"message_template": self.message_template,
					"parameters": self.parameters,
					"content_type": self.content_type
				}

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
