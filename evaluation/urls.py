from django.conf.urls import url, patterns

from .views import *

urlpatterns = [
	url(r'^create_evaluation/$', create_evaluation),
	url(r'^create_question/$', create_question),
	url(r'^view_questions/$', view_questions),
	url(r'^view_evaluations/$', view_evaluations)
]
