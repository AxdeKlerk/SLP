from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
]