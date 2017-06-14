import textwrap

from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_protect

from django.views.generic.base import View
from registration.backends.hmac.views import RegistrationView
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from forms import RegistrationFormCaptcha
from forms import ChipDesignEditForm
from django.forms.models import modelform_factory

from models import ChipDesign
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from django.db.models import ForeignKey
from django.contrib.auth.models import User

from bootstrap3.templatetags.bootstrap3 import bootstrap_button
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from betterforms.views import BrowseView
from django_tables2 import SingleTableView

from tables import ChipDesignTable

from django_tables2.utils import A  # alias for Accessor

class ChipDesignDelete(DeleteView):
	template_name = 'chipdesign_confirm_delete.html'
	success_url = reverse_lazy('home')
	model = ChipDesign

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ChipDesignDelete, self).dispatch(request, *args, **kwargs)

class ChipDesignAdd(CreateView):
	template_name = 'chipdesign_form.html'
	form_class = ChipDesignEditForm
	model = ChipDesign
	success_url = reverse_lazy('home')

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ChipDesignAdd, self).dispatch(request, *args, **kwargs)

	@csrf_protect
	def view(request, *args, **kwargs):
		print("\n\nviewing\n\n")
		super(ChipDesignAdd, self).view(request, *args, **kwargs)

	@csrf_protect
	def save(self, force_insert, force_update):
		print("\n\nviewing\n\n")
		super(ChipDesignAdd, self).save(self, force_insert, force_update)

class ChipDesignModify(UpdateView):
	template_name = 'chipdesign_form.html'
	form_class = ChipDesignEditForm
	model = ChipDesign
	success_url = reverse_lazy('home')

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ChipDesignModify, self).dispatch(request, *args, **kwargs)

	@csrf_protect
	def view(request, *args, **kwargs):
		print("\n\nviewing\n\n")
		super(ChipDesignModify, self).view(request, *args, **kwargs)

class ChipDesignSelectionView(SingleTableView):
	model = ChipDesign
	table_class = ChipDesignTable
	template_name = 'chipdesign_list.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ChipDesignSelectionView, self).dispatch(request, *args, **kwargs)

	def view(request, *args, **kwargs):
		super(ChipDesignSelectionView, self).view(request, *args, **kwargs)

class WorkBenchView(TemplateView):
	template_name = 'base.html'
