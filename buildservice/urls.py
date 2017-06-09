from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

import buildservice.views
import django.contrib.auth.views

urlpatterns = [
	url(r'^admin/', admin.site.urls, name='admin'),
	url(r'^$', buildservice.views.index.as_view(), name='home'),
	url(r'^accounts/profile', buildservice.views.index.as_view(), name='profile'),
	#including with and without namespace: workaround for buggy name reverse resolution
	url(r'^accounts/', include('registration.backends.hmac.urls', namespace='accounts')),
	url(r'^accounts/', include('registration.backends.hmac.urls')),
	url(r'^register/$', buildservice.views.RegistrationViewCaptcha.as_view(), name='registration_register'),
	url(r'^accounts/register/$', buildservice.views.RegistrationViewCaptcha.as_view(), name='registration_register'),
]
