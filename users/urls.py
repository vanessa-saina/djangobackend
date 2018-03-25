from django.conf.urls import url, patterns

from .views import *

urlpatterns = [
	url(r'^login/$', login),
	url(r'^create_user/$', create_user),
	url(r'^approve_users/$', approve_users),
	url(r'^view_users/$', view_users),
	url(r'^search_users/(?P<name>[A-Za-z]+)/$', search_users),
	url(r'^delete_user/(?P<user_id>[0-9a-z-]+)/$', delete_user),
	url(r'^check_activation_key/(?P<key>[A-Za-z0-9]+)/$',check_activation_key),
	url(r'^update_account/$', update_account)
]

