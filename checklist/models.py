from django.contrib.auth.models import User
from django.core import signing
from django.db import models
from django.utils import timezone


# Create your models here.
class Company(models.Model):
	name = models.CharField(max_length = 255)
	creator = models.OneToOneField(User)

	def __str__(self):
		return self.name

class Teammate(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	accepted = models.BooleanField(default = False)

	def __str__(self):
		if self.user.get_full_name():
			return self.user.get_full_name()
		else:
			return self.user.get_username()

class Team(models.Model):
	name = models.CharField(max_length = 255)
	manager = models.ForeignKey(User, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name = "teams")

	def get_accepted_teammates(self):
		return Teammate.objects.filter(invite__team__id = self.id, invite__invitation_type = "teammate", invite__status = "accepted", accepted = True)

	def get_pending_teammates(self):
		return Teammate.objects.filter(invite__team__id = self.id, invite__invitation_type = "teammate", invite__status = "accepted", accepted = False)

	def get_invites(self, status = "pending", invitation_type = "teammate"):
		return Invite.objects.filter(team__id = self.id, invitation_type = invitation_type, status = "pending")

	def get_invite(self, user):
		return Invite.objects.get(team__id = self.id, teammate__user__id = user.id)

	def is_invited(self, user):
		return self.get_invite(user) != None

	def get_teammate(self, user):
		return Teammate.objects.get(invite__team__id = self.id, user__id = user.id, invite__invitation_type = "teammate", invite__status = "accepted", accepted = True)

	def is_teammate(self, user):
		return self.get_teammate(user) != None

	def promote(self, teammate):
		invite = self.get_invite(teammate.user)
		invite.status = "promoted"
		self.manager = teammate.user

	def __str__(self):
		return self.name

class Invite(models.Model):
	sender = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 255)
	email = models.EmailField(blank = False)
	teammate = models.OneToOneField(Teammate, on_delete = models.CASCADE, blank = True, null = True, related_name = "invite")
	team = models.ForeignKey(Team, related_name = "invites")
	invitation_time = models.DateTimeField(default = timezone.now)
	invitation_type = models.CharField(
						max_length=10,
						default = "teammate",
						choices=(
							("teammate", "To be teammate"),
							("manager", "To be the new manager"),
						))
	status = models.CharField(
						max_length = 10,
						default = "pending",
						choices = (
							("pending", "Pending"),
							("rejected", "Rejected"),
							("accepted", "Accepted"),
							("cancelled", "Cancelled"),
							("promoted", "Promoted"),
						))

	def __str__(self):
		return "%s - %s - %s - %s" % (self.name, self.email, self.team, self.status)

	def get_access_invite_key(self, user):
		return signing.dumps({"id": self.id, "invitation_time": self.invitation_time, "valid_until": None, "username": user.get_username()})

	def get_invite_key(self):
		return signing.dumps({"id": self.id, "invitation_time": self.invitation_time})

	def __respond_invite(self, status, user = None):
		if user:
			teammate = Teammate.objects.create(user = user)
			Teammate.save(teammate)
			self.teammate = teammate
		self.status = status
		Invite.save(self)

	def accept(self, user):
		self.__respond_invite("accepted", user)
	
	def reject(self, user):
		self.__respond_invite("rejected", user)

	def accept_teammate(self):
		if self.teammate:
			self.teammate.accepted = True
			Teammate.save(self.teammate)

	def cancel(self):
		self.__respond_invite("cancelled")

	def review_invite(self, name, email, invitation_type):
		self.cancel()
		invite = Invite.objects.create(name = name, email = email, invitation_type = self.invitation_type, team = self.team)
		Invite.save(invite)
		return invite
