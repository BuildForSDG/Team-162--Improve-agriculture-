"""
The forms for core module
"""
from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from core.models import User


class CustomUserCreationForm(forms.ModelForm):
    """
    We do some custom stuff to ensure that the creation form is valid in this context.
    """

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label = _("Password"),
        strip = False,
        widget = forms.PasswordInput(attrs = {'autocomplete': 'new-password'}),
        help_text = password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label = _("Password confirmation"),
        widget = forms.PasswordInput(attrs = {'autocomplete': 'new-password'}),
        strip = False,
        help_text = _("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username', 'account_type', 'status')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        """
        Initialize the form's state (overriding).
        @param args:
        @param kwargs:
        """
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code = 'password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
