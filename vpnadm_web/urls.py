from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

admin.autodiscover()


urlpatterns = [
	url(r'',         include('vpnadm.urls')),
	url(r'^staff/',  include('staffpanel.urls')),
	url(r'^admin/',  include(admin.site.urls)),

	url(r'',         include('django.contrib.auth.urls')),

	url(r'^accounts/login/$',  login,             name='login'),
	url(r'^accounts/logout/$', logout_then_login, name='logout_then_login'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
