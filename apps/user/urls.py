from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from apps.user.forms import EmailOnlyPasswordResetForm

app_name = 'user'

urlpatterns = [
    path("login-success/", views.login_success_view, name="login_success"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile_view, name="profile_view"),
    path("password_reset/", auth_views.PasswordResetView.as_view
         (form_class=EmailOnlyPasswordResetForm, template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",), name="password_reset"),
    path("forgot-username/", views.forgot_username, name="forgot_username"),
]
