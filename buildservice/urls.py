from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

import buildservice.settings
import buildservice.views
import django.contrib.auth.views
import registration.backends.hmac.views

urlpatterns = [
	# admin interface
	url(r'^admin/', admin.site.urls, name='admin'),

	# default page
	url(r'^$', buildservice.views.ChipDesignView.as_view(), name='home'),

	# user administration
	url(r'^accounts/profile', buildservice.views.ChipDesignView.as_view(), name='profile'),
	url(r'^register/$', buildservice.views.RegistrationViewCaptcha.as_view(), name='registration_register'),
	url(r'^accounts/register/$', buildservice.views.RegistrationViewCaptcha.as_view(), name='registration_register'),
	url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete'),
	# The activation key can make use of any character from the
	# URL-safe base64 alphabet, plus the colon as a separator.
	url(r'^activate/(?P<activation_key>[-:\w]+)/$', registration.backends.hmac.views.ActivationView.as_view(), name='registration_activate'),
	url(r'^register/$', registration.backends.hmac.views.RegistrationView.as_view(), name='registration_register'),
	url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
	url(r'^register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'),name='registration_disallowed'),
	url(r'', include('registration.auth_urls')),

	# managing chip designs
	url(r'^design/add', buildservice.views.ChipDesignAdd.as_view(), name='add_design'),
	url(r'^design/add', buildservice.views.ChipDesignAdd.as_view(), name='add_design_process'),
	url(r'^design/modify', buildservice.views.ChipDesignModify.as_view(), name='modify_design'),
	url(r'^design/modify', buildservice.views.ChipDesignModify.as_view(), name='modify_design_process'),

] + static(buildservice.settings.STATIC_URL, document_root=buildservice.settings.STATIC_ROOT)
