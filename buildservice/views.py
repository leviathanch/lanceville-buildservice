import textwrap

from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

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
from django.http.request import HttpRequest

from bootstrap3.templatetags.bootstrap3 import bootstrap_button
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from cms.utils.permissions import get_current_user
from django.contrib.sites.shortcuts import get_current_site

from betterforms.views import BrowseView
from django_tables2 import SingleTableView

from tables import ChipDesignTable
from tables import SSHKeyTable

from models import SSHPublicKey
from models import ChipDesign

from forms import RegistrationFormCaptcha
from forms import ChipDesignEditForm
from forms import UserForm

from django_tables2.utils import A  # alias for Accessor

from sshpubkeys import SSHKey

from pyolite import Pyolite

def class_view_decorator(function_decorator):
	"""Convert a function based decorator into a class based decorator usable
	on class based Views.
	Can't subclass the `View` as it breaks inheritance (super in particular),
	so we monkey-patch instead.
	"""

	def simple_decorator(View):
		View.dispatch = method_decorator(function_decorator)(View.dispatch)
		return View

	return simple_decorator

@class_view_decorator(login_required)
class ChipDesignDelete(DeleteView, SingleObjectMixin):
	template_name = 'chipdesign_confirm_delete.html'
	success_url = reverse_lazy('home')
	model = ChipDesign

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

@class_view_decorator(login_required)
class ChipDesignAdd(CreateView):
	template_name = 'chipdesign_form.html'
	form_class = ChipDesignEditForm
	model = ChipDesign
	success_url = reverse_lazy('home')
	user = None

	def __init__(self, *args, **kwargs):
		site_url = get_current_site(self)
		self.user = get_current_user()
		self.new_project_url = str(site_url) + '/' + str(self.user) + '/' 
		super(ChipDesignAdd, self).__init__(*args, **kwargs)

	def form_valid(self, form):
		print form.save()
		return super(ChipDesignAdd, self).form_valid(form)

	@csrf_protect
	def view(request, *args, **kwargs):
		super(ChipDesignAdd, self).view(request, *args, **kwargs)

@class_view_decorator(login_required)
class ChipDesignModify(UpdateView):
	template_name = 'chipdesign_form.html'
	form_class = ChipDesignEditForm
	model = ChipDesign
	success_url = reverse_lazy('home')

	@csrf_protect
	def view(request, *args, **kwargs):
		super(ChipDesignModify, self).view(request, *args, **kwargs)

@class_view_decorator(login_required)
class ChipDesignSelectionView(SingleTableView):
	model = ChipDesign
	table_class = ChipDesignTable
	template_name = 'chipdesign_list.html'

@class_view_decorator(login_required)
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

@class_view_decorator(login_required)
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

@class_view_decorator(login_required)
class WorkBenchView(DetailView):
	template_name = 'workbench_default.html'
	model = ChipDesign

@class_view_decorator(login_required)
class SSHKeyDelete(DeleteView, SingleObjectMixin):
	template_name = 'key_confirm_delete.html'
	success_url = reverse_lazy('profile')
	model = SSHPublicKey

	def __init__(self, *args, **kwargs):
		user = get_current_user()
		self.success_url = reverse_lazy('profile', args=[user.id])
		super(SSHKeyDelete, self).__init__(*args, **kwargs)

@class_view_decorator(login_required)
class UpdateProfileView(TemplateView):
	template_name = 'profile_form.html'
	key_status = None

	def get_context_data(self, **kwargs):
		context = super(UpdateProfileView, self).get_context_data(**kwargs)
		context['key_table'] = SSHKeyTable(SSHPublicKey.objects.all(), prefix="1-")
		context['key_status'] = self.key_status
		return context

	def get(self, request, *args, **kwargs):
		context = super(UpdateProfileView, self).get_context_data(**kwargs) # get context data

		# Add new record
		new_key=request.GET.get('new_key')
		if(new_key!=None):
			if(len(new_key)>0):
				try:
					ssh = SSHKey(new_key)
					ssh.parse() # make sure the key is ok
					key=SSHPublicKey(user=get_current_user(), comment=ssh.comment, key=new_key)
					key.save()
					self.key_status='Added new key with ID: '+ssh.comment
				except:
					self.key_status='Could not add key'

		# Updating existing record
		key_id=request.GET.get('key_id')
		update_key=request.GET.get('update_key')
		if((update_key!=None) and (key_id!=None)):
			try:
				ssh = SSHKey(update_key)
				ssh.parse() # make sure the key is ok
				key=SSHPublicKey.objects.get(id=key_id)
				key.key = update_key
				key.comment = ssh.comment
				key.save()
				self.key_status='Updated key with ID: '+ssh.comment
			except:
				self.key_status='Could not update key'

		return super(UpdateProfileView, self).get(request, *args, **kwargs)

