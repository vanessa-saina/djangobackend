from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from evaluation.models import Evaluation, Question
from users.models import User, Unit, Myunit



class UserCreationForm(forms.ModelForm):
    # A form for creating new users. Includes all the required
    # fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # A form for updating users. Includes all the fields on
    # the user, but replaces the password field with admin's
    # password hash display field.

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    #form = UserChangeForm
    #add_form = UserCreationForm
    #add_form = RegisterForm

    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'role', 'is_staff')
    list_filter = ('date_joined', 'role')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('id', 'first_name', 'last_name', 'email', 'role', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lecturer_id', 'date_added', 'date_modified')


admin.site.register(User, UserAdmin)
admin.site.register(Unit)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Question)
admin.site.register(Myunit)
