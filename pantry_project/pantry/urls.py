from django.urls import path

from pantry import views

app_name = "pantry"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),

    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),

    path("recipes/", views.recipes, name="recipes"),
    path("recipes/<int:user_id>/<int:recipe_id>", views.recipe, name="recipe"),

    path("create-a-recipe/", views.create_a_recipe, name="create-a-recipe"),

    path("<int:user_id>", views.user_profile, name="user-profile"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),

    path("<int:user_id>/user-recipes/", views.user_recipes, name="user-recipes"),
    path("<int:user_id>/saved-recipes/", views.saved_recipes, name="saved-recipes"),
    path("<int:user_id>/user-reviews/", views.user_reviews, name="user-reviews"),

    path("like_review/", views.like_review, name="like-review"),
]
