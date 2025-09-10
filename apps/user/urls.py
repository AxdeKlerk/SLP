from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("login-success/", views.login_success_view, name="login_success"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile_view, name="profile"),
]