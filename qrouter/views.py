from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from buildservice.models import ChipDesign

class DefaultView(DetailView):
	template_name = 'base.html'
	model = ChipDesign
