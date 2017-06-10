from settings import * # Secret keys and so on

# Captcha and other stuff for registration
from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

from django.forms import CharField as FormCharField
from django.forms import ModelForm

from django.db.models import ForeignKey
from django.db.models import CharField

from django.contrib.auth.models import User

from models import ChipDesign

class RegistrationFormCaptcha(RegistrationForm):
	captcha = ReCaptchaField(public_key=GOOGLE_RECAPTCHA_SITE_KEY,private_key=GOOGLE_RECAPTCHA_SECRET_KEY)

class ChipDesignAddForm(ModelForm):
	class Meta:
		model = ChipDesign
		fields = ('name','user')
		#field_classes = {'name': CharField}

class ChipDesignSelectionForm(ModelForm):
	class Meta:
		model = ChipDesign
		fields = ('name','user')
		#field_classes = {'name': CharField}
