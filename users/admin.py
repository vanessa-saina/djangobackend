from django.contrib import admin

from evaluation.models import Evaluation, Question
from users.models import User, Unit


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'role', 'is_staff')
    list_filter = ('date_joined', 'role')
    search_fields = ('first_name', 'last_name', 'email')


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lecturer_id', 'date_added', 'date_modified')


admin.site.register(User, UserAdmin)
admin.site.register(Unit)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Question)