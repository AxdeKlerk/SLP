from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

class EmailOnlyPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Filter users by email only
        active_users = User._default_manager.filter(
            email__iexact=email, is_active=True
        )
        return (u for u in active_users if u.has_usable_password())

class ForgotUsernameForm(forms.Form): 
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(attrs={"class": "form-control"}))
