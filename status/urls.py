from django.conf.urls import url

from status.views import HomePageView

urlpatterns = [
	url(r'^status/', HomePageView.as_view(), name='home'),
]
