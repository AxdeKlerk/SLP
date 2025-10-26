from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
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

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user