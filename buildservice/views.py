import textwrap

from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from django.views.generic.base import View
from registration.backends.hmac.views import RegistrationView
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from forms import RegistrationFormCaptcha
from forms import ChipDesignSelectionForm

from models import ChipDesign

from django.db.models import ForeignKey
from django.contrib.auth.models import User

from bootstrap3.templatetags.bootstrap3 import bootstrap_button
from django.contrib.auth.decorators import login_required

class ChipDesignAdd(TemplateView):
	template_name = 'chipdesign_form.html'

	def get_context_data(self, **kwargs):
		context = super(ChipDesignAdd, self).get_context_data(**kwargs)
		context['AddButton'] = bootstrap_button( "Save", button_type="submit", button_class="btn-primary", href=reverse('add_design_process'))
		return context

class ChipDesignModify(TemplateView):
	template_name = 'chipdesign_form.html'

	def get_context_data(self, **kwargs):
		context = super(ChipDesignModify, self).get_context_data(**kwargs)
		context['AddButton'] = bootstrap_button( "Save", button_type="submit", button_class="btn-primary", href=reverse('modify_design_process'))
		return context

#@login_required(login_url='/accounts/login/')
class ChipDesignView(ListView):
	template_name = 'chipdesign_list.html'
	model = ChipDesign
	context_object_name = 'design_list'

	def get_queryset(self):
		recent_user=self.request.user
		if recent_user.is_authenticated():
			return ChipDesign.objects.filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super(ChipDesignView, self).get_context_data(**kwargs)
		context['AddButton'] = bootstrap_button( "Add chip design", button_type="submit", button_class="btn-primary", href=reverse('add_design'))
		return context

class RegistrationViewCaptcha(RegistrationView):
	form_class = RegistrationFormCaptcha
