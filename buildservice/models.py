from django.contrib.auth.models import User

from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import Model
from django.db.models import PositiveIntegerField

from cms.utils.permissions import get_current_user

class ChipDesign(Model):
	user = ForeignKey(User, default=get_current_user)
	#user = ForeignKey(User)
	name = CharField(max_length=10, blank=True)
	url = CharField(max_length=100, blank=True)
	private = BooleanField()
	locally = BooleanField()
	description = CharField(max_length=500, blank=True)

	class Meta:
		managed = True
		db_table = 'buildservice_chipdesign'

