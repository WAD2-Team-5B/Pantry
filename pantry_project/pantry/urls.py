from django.urls import path

from pantry import views

app_name = "pantry"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
