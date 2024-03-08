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
    # TESTING PURPOSES
    # TODO - CHANGE TO INCLUDE USER ID AND RECIPE ID
    path("recipe/", views.recipe, name="recipe"),
    path("create-a-recipe/", views.create_a_recipe, name="create-a-recipe"),
    # TESTING PURPOSE
    # TODO - CHANGE TO USER ID
    path("user-profile/<int:user_id>", views.user_profile, name="user-profile"),
    # TESTING PURPOSE
    # TODO - CHANGE TO USER ID
    path("user-profile/user-recipes/", views.user_recipes, name="user-recipes"),
    # TESTING PURPOSE
    # TODO - CHANGE TO USER ID
    path("user-profile/saved-recipes/", views.saved_recipes, name="saved-recipes"),
    # TESTING PURPOSE
    # TODO - CHANGE TO USER ID
    path("user-profile/user-reviews/", views.user_reviews, name="user-reviews"),
]
