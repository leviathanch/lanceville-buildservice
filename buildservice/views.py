import textwrap

from django.conf import settings
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.generic.base import View

class index(TemplateView):
	#template_name = 'base.html'
	template_name = 'base.html'
	body_content = "miau"

	def dispatch(self, request, *args, **kwargs):
		response = super(index, self).dispatch(request, *args, **kwargs)
		response.render()
		return response
