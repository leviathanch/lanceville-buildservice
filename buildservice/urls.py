from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

import buildservice.views
import django.contrib.auth.views

urlpatterns = [
	url(r'^admin/', admin.site.urls, name='admin'),
	url(r'^$', buildservice.views.index.as_view(), name='home'),
	url(r'^accounts/profile', buildservice.views.index.as_view(), name='home'),
	url(r'^accounts/', include('registration.urls', namespace='accounts')),
]
