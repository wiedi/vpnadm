from django.conf.urls import url
from vpnadm import views

urlpatterns = [
	url(r'^$',                           views.ClientList.as_view(),   name='client_list'),
#	url(r'status/^$',                    views.status,                 name='status'),

	url(r'^client/add$',                        views.ClientCreate.as_view(),  name='client_add'),
	
	url(r'^client/(?P<pk>\d+)/config.ovpn$',    views.client_download_config,  name='client_download_config'),
	url(r'^client/(?P<pk>\d+)/reset_password$', views.client_reset_password,   name='client_reset_password'),
	url(r'^client/(?P<pk>\d+)/delete$',         views.ClientDelete.as_view(),  name='client_delete'),

	url(r'^settings/$',                 views.ServerSettingsUpdate.as_view(), name='serversettings_update'),

]