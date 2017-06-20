from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import StackedInline
from django.contrib.admin import site

from django.views.decorators.csrf import csrf_protect

from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import Model
from django.db.models import PositiveIntegerField

from cms.utils.permissions import get_current_user

class UserProfile(Model):
	user = ForeignKey(User, default=get_current_user)

	class Meta:
		managed = True
		db_table = 'buildservice_userprofiles'

class TechnologyNode(Model):
	name = CharField(max_length=20, blank=False)

	def __unicode__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'buildservice_technologies'

class EnabledTechnologyNode(Model):
	user = ForeignKey(User, default=get_current_user)
	technology = ForeignKey(TechnologyNode, default=1)

	class Meta:
		managed = True
		db_table = 'buildservice_enabled_technologies'

class ChipDesign(Model):
	user = ForeignKey(User, default=get_current_user)
	name = CharField(max_length=10, blank=True)
	url = CharField(max_length=100, blank=True)
	description = CharField(max_length=1000, blank=True)
	technology = ForeignKey(TechnologyNode, default=1)

	def __unicode__(self):
		return 'Policy: ' + self.name

	class Meta:
		managed = True
		db_table = 'buildservice_chipdesign'
		unique_together = ('user', 'name')

class SSHPublicKey(Model):
	user = ForeignKey(User, default=get_current_user)
	comment = CharField(max_length=20, blank=False)
	key = CharField(max_length=1000, blank=False)

	class Meta:
		managed = True
		db_table = 'buildservice_sshpublickeys'
		unique_together = ('user', 'key')

class InlineUserProfile(StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'user'

class InlineEnabledTechnologyNode(StackedInline):
	model = EnabledTechnologyNode

class CustomUserAdmin(UserAdmin):
	inlines = (InlineUserProfile, InlineEnabledTechnologyNode)

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

#site.unregister(User)
#site.register(User, CustomUserAdmin)
site.register(TechnologyNode)
