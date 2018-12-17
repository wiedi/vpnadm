from django.conf.urls import url
from vpnadm import views

urlpatterns = [
	url(r'^$',                           views.ClientList.as_view(),   name='client_list'),
#	url(r'status/^$',                    views.status,                 name='status'),

	url(r'^client/add$',                        views.ClientCreate.as_view(),  name='client_add'),
	
	url(r'^client/(?P<pk>\d+)/config.ovpn$',    views.client_download_config,  name='client_download_config'),
	url(r'^client/(?P<pk>\d+)/reset_cert$',     views.client_reset_cert,       name='client_reset_cert'),
	url(r'^client/(?P<pk>\d+)/delete$',         views.ClientDelete.as_view(),  name='client_delete'),

	url(r'^settings/$',                 views.ServerSettingsUpdate.as_view(), name='serversettings_update'),

	url(r'^route4/$',                           views.Route4List.as_view(),    name='route4_list'),
	url(r'^route4/add$',                        views.Route4Create.as_view(),  name='route4_add'),
	url(r'^route4/(?P<pk>\d+)/delete$',         views.Route4Delete.as_view(),  name='route4_delete'),
	url(r'^route6/$',                           views.Route6List.as_view(),    name='route6_list'),
	url(r'^route6/add$',                        views.Route6Create.as_view(),  name='route6_add'),
	url(r'^route6/(?P<pk>\d+)/delete$',         views.Route6Delete.as_view(),  name='route6_delete'),

]