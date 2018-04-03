from django.conf.urls import url, patterns

from .views import *

urlpatterns = [
	url(r'^create_evaluation/$', create_evaluation),
	url(r'^create_question/$', create_question),
	url(r'^create_unit/$', create_unit),
	url(r'^create_questions_many/$', create_questions_many),
	url(r'^view_questions/$', view_questions),
	url(r'^view_evaluations/$', view_evaluations),
	url(r'^view_units/$', view_units),
	url(r'^view_evaluation_by_lec/(?P<lec>[0-9a-z-]+)/$', view_evaluation_by_lec)
]

