from django.shortcuts import render
from django.views.generic.base import TemplateView

class DefaultView(TemplateView):
	template_name = 'base.html'
