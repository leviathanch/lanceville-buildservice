from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db.models import CharField

class ChipDesign(models.Model):
	user = ForeignKey(User)
	name = CharField(max_length=10, blank=True)

	class Meta:
		managed = True
		db_table = 'buildservice_chipdesign'
