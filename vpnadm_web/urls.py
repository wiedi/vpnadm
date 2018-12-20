from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout_then_login

admin.autodiscover()


urlpatterns = [
	url(r'',         include('vpnadm.urls')),
	url(r'^staff/',  include('staffpanel.urls')),
	url(r'^admin/',  admin.site.urls),

	url(r'',         include('django.contrib.auth.urls')),

	url(r'^accounts/login/$',  LoginView.as_view(template_name='registration/login.html'), name='login'),
	url(r'^accounts/logout/$', logout_then_login,                                          name='logout_then_login'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
