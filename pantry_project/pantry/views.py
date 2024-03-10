from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q
from pantry_project.settings import MEDIA_DIR

from pantry.models import Review, UserProfile, Recipe, SavedRecipes, Cuisine, Category
from pantry.forms import UserForm, UserProfileForm

from pantry.helpers import *

import os

# TEMPLATE VIEWS


def index(request):

    # TODO - if request = post, then they are have searched so need the redirect to the recipes page
    # need to somehow send in the search_query with the redirect

    # UNCOMMENT ONCE DATABASE IS SET UP
    highest_rated_recipes = Recipe.objects.order_by("-rating", "-pub_date")[:10]
    newest_recipes = Recipe.objects.order_by("-pub_date")[:10]

    context_dict = {
        "highest_rated_recipes": highest_rated_recipes,
        "newest_recipes": newest_recipes,
        "num_highest_rated": len(highest_rated_recipes),
        "num_newest": len(newest_recipes),
    }
    return render(request, "pantry/index.html", context=context_dict)


def about(request):
    return render(request, "pantry/about.html")


def recipes(request):

    # assume that request method = post? - what of they have jumped to find recipes page
    # TODO - if redirect then user is coming from the index page and we need to display search query results

    recipes = [{}]

    if request.method == "POST":

        difficulties = request.POST.get("selected_difficulty")
        cuisines = request.POST.get("selected_cuisines")
        categories = request.POST.get("selected_categories")
        sort = request.POST.get("selected_sort")

        difficulty_query = Q()
        # reviews is the only different one
        for difficulty in difficulties:
            difficulty_query |= Q(difficulty=difficulty)

        cuisine_query = Q()

        for cuisine in cuisines:
            cuisine_query |= Q(cuisine=cuisine)

        category_query = Q()

        for category in categories:
            categories |= Q(category=category)

        recipes = Recipe.objects.filter(difficulty_query, cuisine_query, category_query)
        if sort != "":
            recipes = recipes.order_by("-" + sort)
        else:
            recipes = recipes.order_by("-pub_date")

        recipes = recipes.values(
            "title",
            "link",
            "image",
            "rating",
            "saves",
            "difficulty",
            "cuisine",
            "prep",
            "cook",
        )

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict = {
        "recipes": recipes,
        "cuisines": cuisines,
        "categories": categories,
    }
    return render(request, "pantry/recipes.html", context=context_dict)


def signup(request):

    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # TODO - i dont think we are sending images in the signup form?

            if "image" in request.FILES:
                profile.image = request.FILES["image"]

            profile.save()
            auth.login(request, user)

            # # create their media folder using their id
            # dir_name = "user-id-" + str(user.pk)
            # os.mkdir(os.path.join(MEDIA_DIR, dir_name))
            # os.mkdir(os.path.join(MEDIA_DIR, dir_name, "profile"))
            # os.mkdir(os.path.join(MEDIA_DIR, dir_name, "recipes"))

            return redirect(reverse("pantry:index"))

        else:
            return render(
                request,
                "pantry/signup.html",
                {"user_form": user_form, "profile_form": profile_form},
            )

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "pantry/signup.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def login(request):

    context_dict = {"success": True}

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect(reverse("pantry:index"))
        else:
            context_dict["success"] = False
            return render(request, "pantry/login.html", context=context_dict)

    else:
        return render(request, "pantry/login.html", context=context_dict)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("pantry:index"))


def recipe(request, user_id, recipe_id):

    recipe = Recipe.objects.get(id=recipe_id)
    user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(recipe=recipe)

    context_dict = {
        "user": user,
        "recipe": recipe,
        "reviews": reviews,
    }

    return render(request, "pantry/recipe.html", context=context_dict)


@login_required
def create_a_recipe(request):

    if request.method == "POST":

        # get our cuisine instance
        cuisine = Cuisine.objects.get(type=request.POST.get("cuisine"))

        # create the recipe instance
        instance = Recipe.objects.create(user=request.user, cuisine=cuisine)

        # upload the image
        image = request.FILES.get("image")
        instance.image = image
        instance.save()

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict = {
        "cuisines": cuisines,
        "categories": categories,
    }

    return render(request, "pantry/create-a-recipe.html", context=context_dict)


def user_profile(request, user_id):

    user = request.user
    other_user = User.objects.get(id=user_id)
    own_profile = is_own_profile(user, other_user)
    other_user_profile = UserProfile.objects.get(user=other_user)

    context_dict = {
        "user": other_user,
        "user_profile": other_user_profile,
        "own_profile": own_profile,
    }

    return render(request, "pantry/user-profile.html", context=context_dict)


def user_recipes(request, user_id):

    return render(
        request,
        "pantry/user-data.html",
        context=get_user_data_context_dict(request, user_id, "Recipe", Recipe),
    )


def saved_recipes(request, user_id):

    return render(
        request,
        "pantry/user-data.html",
        context=get_user_data_context_dict(
            request, user_id, "Saved Recipe", SavedRecipes
        ),
    )


def user_reviews(request, user_id):

    return render(
        request,
        "pantry/user-data.html",
        context=get_user_data_context_dict(request, user_id, "Reviewed Recipe", Review),
    )


@login_required
def edit_profile(request, user_id):

    return render(request, "pantry/edit-profile.html")
