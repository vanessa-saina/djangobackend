from django.conf.urls import url, patterns

from .views import *

urlpatterns = [
    url(r'^get_dict/$', get_dict),
]