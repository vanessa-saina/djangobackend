from django.contrib import admin

from evaluation.models import Evaluation,Question
from users.models import User

admin.site.register(User)
admin.site.register(Evaluation)
admin.site.register(Question)