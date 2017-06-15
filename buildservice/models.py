from django.contrib.auth.models import User

from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import Model
from django.db.models import PositiveIntegerField

from cms.utils.permissions import get_current_user

class ChipDesign(Model):
	user = ForeignKey(User, default=get_current_user)
	name = CharField(max_length=10, blank=True)
	url = CharField(max_length=100, blank=True)
	description = CharField(max_length=1000, blank=True)

	class Meta:
		managed = True
		db_table = 'buildservice_chipdesign'
		unique_together = ('user', 'name')

class SSHPublicKey(Model):
	user = ForeignKey(User, default=get_current_user)
	key = CharField(max_length=1000, blank=False)

	class Meta:
		managed = True
		db_table = 'buildservice_sshpublickeys'
		unique_together = ('user', 'key')
