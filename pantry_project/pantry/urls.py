from django.urls import path

from pantry import views

app_name = "pantry"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("recipes/", views.recipes, name="recipes"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
]
