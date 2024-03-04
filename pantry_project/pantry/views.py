from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from pantry.models import UserProfile

# TEMPLATE VIEWS


def index(request):

    # TESTING PURPOSES
    # would use real data from database
    recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 10

    num_highest_rated = len(recipes)
    num_newest = len(recipes)

    context_dict = {
        "highest_rated_recipes": recipes,
        "newest_recipes": recipes,
        "num_highest_rated": num_highest_rated,
        "num_newest": num_newest,
    }
    return render(request, "pantry/index.html", context=context_dict)


def about(request):
    return render(request, "pantry/about.html")


def recipes(request):

    # TESTING PURPOSES
    # would use real data from database
    recipes = [
        {
            "name": "Spag Bol",
            "link": "",
            "image": "",
            "rating": 4.67,
            "saves": 34,
            "difficulty": "beginner",
            "cuisine": "Italian",
            "prep": "1:30",
            "cook": "0:30",
        }
    ] * 20

    # TESTING PURPOSES
    # would use real data from database
    cuisines = [
        "Italian",
        "Mexican",
        "Indian",
        "Chinese",
        "Japanese",
        "Thai",
        "French",
        "Greek",
        "Spanish",
        "American",
    ]

    # TESTING PURPOSES
    # would use real data from database
    categories = [
        "Vegan",
        "Vegetarian",
        "Pescatarian",
        "Gluten-Free",
        "Dairy-Free",
        "Nut-Free",
        "Soy-Free",
        "Egg-Free",
    ]

    context_dict = {
        "recipes": recipes,
        "cuisines": cuisines,
        "categories": categories,
    }
    return render(request, "pantry/recipes.html", context=context_dict)


def signup(request):
    PASSWORD_MIN_LENGTH = 6
    USERNAME_MIN_LENGTH = 1

    context_dict = {"success": True, "error": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if len(username) < USERNAME_MIN_LENGTH:
            context_dict["success"] = False
            context_dict["error"] = (
                f"Username must be at least {USERNAME_MIN_LENGTH} characters long!"
            )
            return render(request, "pantry/signup.html", context_dict)

        if len(password) < PASSWORD_MIN_LENGTH:
            context_dict["success"] = False
            context_dict["error"] = (
                f"Password must be at least {PASSWORD_MIN_LENGTH} characters long!"
            )
            return render(request, "pantry/signup.html", context_dict)

        try:
            user = User.objects.create_user(username=username, password=password)

        except IntegrityError:  # the username already exists
            context_dict["success"] = False
            context_dict["error"] = f"Username '{username}' already exists"
            return render(request, "pantry/signup.html", context_dict)

        if user:

            # if django user object created, a UserProfile can be created with additional fields required by pantry
            userProfile = UserProfile.objects.create(user=user)

            if userProfile:
                auth.login(request, user)
                return redirect(reverse("pantry:index"))

        # either the User or UserProfile have failed to be created
        context_dict["success"] = False
        context_dict["error"] = "Unknown error"
        return render(request, "pantry/signup.html", context_dict)

    else:
        return render(request, "pantry/signup.html", context_dict)


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
