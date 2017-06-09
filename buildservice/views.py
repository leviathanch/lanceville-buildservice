import textwrap

from django.conf import settings
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.generic.base import View
from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

from settings import *

class index(TemplateView):
	#template_name = 'base.html'
	template_name = 'base.html'
	body_content = "miau"

	def dispatch(self, request, *args, **kwargs):
		response = super(index, self).dispatch(request, *args, **kwargs)
		response.render()
		return response

class RegistrationFormCaptcha(RegistrationForm):
	captcha = ReCaptchaField(public_key=GOOGLE_RECAPTCHA_SITE_KEY,private_key=GOOGLE_RECAPTCHA_SECRET_KEY)

class RegistrationViewCaptcha(RegistrationView):
	form_class = RegistrationFormCaptcha
	def register(self, form):
		super(RegistrationViewCaptcha,self).register(form)
