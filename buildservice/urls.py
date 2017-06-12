from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.urls import reverse

import buildservice.settings
import buildservice.views
import django.contrib.auth.views
import registration.backends.hmac.views

admin.autodiscover()

urlpatterns = [
	# admin interface
	url(r'^admin/', admin.site.urls, name='admin'),

	# default page
	url(r'^$', buildservice.views.ChipDesignSelectionView.as_view(), name='home'),

	url(r'', include('allauth.urls')),

	# managing chip designs
	url(r'^design/add', buildservice.views.ChipDesignAdd.as_view(), name='add_design'),

	url(r'^design/add', buildservice.views.ChipDesignAdd.as_view(), name='add_design_process'),
	url(r'^design/add/success', buildservice.views.ChipDesignAdd.as_view(), name='add_design_sucess'),

	url(r'^design/modify/(?P<pk>\d+)/$', buildservice.views.ChipDesignModify.as_view(), name='modify_design'),
	url(r'^design/delete/(?P<pk>\d+)/$', buildservice.views.ChipDesignDelete.as_view(), name='delete_design'),

] + static(buildservice.settings.STATIC_URL, document_root=buildservice.settings.STATIC_ROOT)
