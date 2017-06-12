from settings import * # Secret keys and so on

# Captcha and other stuff for registration
from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

from django.forms import CharField
from django.forms import URLField
from django.forms import ModelForm

from django.db.models import ForeignKey

from django.contrib.auth.models import User

from betterforms.changelist import SortForm
from betterforms.changelist import Header
from betterforms.forms import BetterModelForm
from betterforms.forms import BetterForm
from betterforms.changelist import SearchForm
from tinymce.widgets import TinyMCE

from models import ChipDesign
from suit.admin import SortableModelAdmin
from suit.admin import SortableChangeList
from suit.admin import SortableListForm

class RegistrationFormCaptcha(RegistrationForm):
	captcha = ReCaptchaField(public_key=GOOGLE_RECAPTCHA_SITE_KEY,private_key=GOOGLE_RECAPTCHA_SECRET_KEY)

class ChipDesignEditForm(BetterModelForm):
	description = CharField(
		required=False,
		widget=TinyMCE(attrs={'style':'width:100%'})
	)
	url = URLField()
	
	label = 'Design'
	class Meta:
		model = ChipDesign
		fields = ('name','url','private','locally','description')
		fieldsets = [('design', {
			'fields': ['name','url','private','locally','description'],
			'legend': '', 'classes': ['boxy-grey'],
		})]
