import textwrap

from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from registration.backends.hmac.views import RegistrationView

from django.forms.models import model_to_dict
from django.forms.models import modelform_factory

from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from django.views.generic import ListView
from django.views.generic import RedirectView

from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from django.views.generic.base import TemplateView
from django.views.generic.base import View

from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_protect

from django.db.models import ForeignKey
from django.contrib.auth.models import User

from bootstrap3.templatetags.bootstrap3 import bootstrap_button
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from betterforms.views import BrowseView
from django_tables2 import SingleTableView

from tables import ChipDesignTable
from models import ChipDesign

from forms import RegistrationFormCaptcha
from forms import ChipDesignEditForm

from django_tables2.utils import A  # alias for Accessor

class ChipDesignDelete(DeleteView, SingleObjectMixin):
	template_name = 'chipdesign_confirm_delete.html'
	success_url = reverse_lazy('home')
	model = ChipDesign

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(ChipDesignDelete, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		design = self.get_object()
		design_id = design.id

		if 'open_designs' in request.session:
			saved_list = request.session['open_designs']
		else:
			saved_list = []

		new_list = []
		for saved in saved_list:
			if saved['id'] != design_id:
				new_list.append(saved)

		request.session['open_designs'] = new_list

		return super(ChipDesignDelete, self).post(request, *args, **kwargs)

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

class WorkBenchOpenView(RedirectView, SingleObjectMixin):
	model = ChipDesign

	def __init__(self, *args, **kwargs):
		self.url = reverse_lazy('home')
		super(WorkBenchOpenView, self).__init__(*args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		design = self.get_object()
		if 'open_designs' in request.session:
			saved_list = request.session['open_designs']
		else:
			saved_list = []

		for saved in saved_list:
			if saved['id'] == design.id:
				return super(WorkBenchOpenView, self).get(request, *args, **kwargs) # already in list

		saved_list.append(model_to_dict(design))

		request.session['open_designs'] = saved_list

		return super(WorkBenchOpenView, self).get(request, *args, **kwargs)

class WorkBenchCloseView(RedirectView, SingleObjectMixin):
	model = ChipDesign

	def __init__(self, *args, **kwargs):
		self.url = reverse_lazy('home')
		super(WorkBenchCloseView, self).__init__(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		design = self.get_object()
		if 'open_designs' in request.session:
			saved_list = request.session['open_designs']
		else:
			saved_list = []

		new_list = []
		for saved in saved_list:
			if saved['id'] != design.id:
				new_list.append(saved)

		request.session['open_designs'] = new_list

		return super(WorkBenchCloseView, self).get(request, *args, **kwargs)

class WorkBenchView(DetailView):
	template_name = 'workbench_default.html'
	model = ChipDesign

class UpdateProfileView(UpdateView):
	model = User
