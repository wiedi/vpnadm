from django.conf.urls import url
from staffpanel.views import *

urlpatterns = [
	url(r'^users/$',                             UserList.as_view(),   name='staffpanel_user_list'),
	url(r'^users/add$',                          user_create,          name='staffpanel_user_add'),
	url(r'^users/(?P<pk>\d+)/reset$',            user_reset_password,  name='staffpanel_user_reset_password'),
	url(r'^users/(?P<pk>\d+)/delete$',           UserDelete.as_view(), name='staffpanel_user_delete'),

	url(r'^users/(?P<pk>\d+)/disable$',          user_disable,         name='staffpanel_user_disable'),
	url(r'^users/(?P<pk>\d+)/enable$',           user_enable,          name='staffpanel_user_enable'),

	url(r'^users/(?P<pk>\d+)/user_set_staff$',   user_set_staff,       name='staffpanel_user_set_staff'),
	url(r'^users/(?P<pk>\d+)/user_unset_staff$', user_unset_staff,     name='staffpanel_user_unset_staff'),

]
