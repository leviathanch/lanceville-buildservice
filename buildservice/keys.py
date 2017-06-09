from django.conf import settings # import the settings file

def google_site_key(request):
	# return the value you want as a dictionnary. you may add multiple values in there.
	return {'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY}
