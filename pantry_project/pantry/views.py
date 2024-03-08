from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from pantry.models import UserProfile
from pantry.models import Recipe
from django.http import HttpResponseNotFound
from pantry.forms import UserForm, UserProfileForm

# TEMPLATE VIEWS


def index(request):

    # UNCOMMENT ONCE DATABASE IS SET UP
    highest_rated_recipes = Recipe.objects.order_by("-rating", "-date_pub")[:10].values(
        "title", "image", "link"
    )
    newest_recipes = Recipe.objects.order_by("-date_pub")[:10].values(
        "title", "image", "link"
    )

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
    # highest_rated_recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 10
    # newest_recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 10

    context_dict = {
        "highest_rated_recipes": list(highest_rated_recipes),
        "newest_recipes": list(newest_recipes),
        "num_highest_rated": len(highest_rated_recipes),
        "num_newest": len(newest_recipes),
    }
    return render(request, "pantry/index.html", context=context_dict)


def about(request):
    return render(request, "pantry/about.html")


def recipes(request):

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
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
    success = False

    if request.method=="POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "image" in request.FILES:
                profile.image = request.FILES["image"]

            profile.save()

            success = True

        else:
            render(request, "pantry/signup.html",{"success":success, "error":"", "user_form":user_form, "profile_form":profile_form})
    else:
        user_form = UserForm()
        profile_form=UserProfileForm()

    return render(request, "pantry/signup.html",{"success":True, "error":"", "user_form":user_form, "profile_form":profile_form})

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


def recipe(request):

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
    description = (("#" * 100) + "\n") * 10
    steps = [
        "#" * 150,
    ] * 10
    categories = ["Vegan", "Vegetarian", "Pescatarian"]
    ingredients = [
        "Milk",
        "Eggs",
        "Flour",
        "Sugar",
        "Butter",
        "Salt",
        "Pepper",
        "Tomatoes",
        "Beef",
        "Onions",
        "Garlic",
        "Pasta",
    ]
    reviews = [
        {
            "username": "GreatCook123",
            "likes": 17,
            "date_pub": "2023-10-21",
            "review": "#" * 150,
        }
    ] * 5

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
    context_dict = {
        # header
        "username": "John12345",
        "user_id": "",
        "name": "Spag Bol",
        "date_pub": "2021-09-21",
        # description
        "image": "",
        "description": description,
        # sub info
        "rating": 4.67,
        "saves": 34,
        "difficulty": "beginner",
        "cuisine": "Italian",
        "prep": "1:30",
        "cook": "0:30",
        # main info
        "steps": steps,
        "categories": categories,
        "ingredients": ingredients,
        # reviews
        "reviews": reviews,
    }

    return render(request, "pantry/recipe.html", context=context_dict)


@login_required
def create_a_recipe(request):

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
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
        "cuisines": cuisines,
        "categories": categories,
    }

    return render(request, "pantry/create-a-recipe.html", context=context_dict)


def user_profile(request, user_id):

    # TODO - CHECK IF OUR USER ID MATCHES THE USER ID OF USER'S PROFILE WE ARE VISITNG.
    # IF IT DOES, THEN IT'S OUR OWN PROFILE
    # username = "JOHN123"

    own_profile = False
    if request.user.is_authenticated:
        if user_id == request.user.id:
            own_profile = True

    profile_user = User.objects.get(id=user_id)

    if not profile_user:
        return HttpResponseNotFound("Profile does not exist.")

    username = profile_user.username
    user_profile = UserProfile.objects.get(user=profile_user)
    image = user_profile.image
    bio = user_profile.bio
    context_dict = {
        "username": username,
        "image": image,
        "user_bio": bio,
        "own_profile": own_profile,
    }

    return render(request, "pantry/user-profile.html", context=context_dict)


def user_recipes(request):

    # TODO - CHANGE TO EITHER 'My Recipes' OR 'JOHN123's Recipes'
    # BASED ON IF COMING FROM OUR OWN PROFILE OR ANOTHER USER'S
    page_name = "My Recipes"

    # TODO - CHANGE TO REAL DATA FROM DB
    recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 20

    context_dict = {
        "page_name": page_name,
        "user_data": recipes,
        # needed for knowing if we are visiting our OWN profile or another users
        "own_profile": True,
    }

    return render(request, "pantry/user-data.html", context=context_dict)


def saved_recipes(request):

    # TODO - CHANGE TO EITHER 'My Recipes' OR 'JOHN123's Recipes'
    # BASED ON IF COMING FROM OUR OWN PROFILE OR ANOTHER USER'S
    page_name = "My Saved Recipes"

    # TODO - CHANGE TO REAL DATA FROM DB
    recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 20

    context_dict = {
        "page_name": page_name,
        "user_data": recipes,
        # needed for knowing if we are visiting our OWN profile or another users
        "own_profile": True,
    }

    return render(request, "pantry/user-data.html", context=context_dict)


def user_reviews(request):

    # TODO - CHANGE TO EITHER 'My Recipes' OR 'JOHN123's Recipes'
    # BASED ON IF COMING FROM OUR OWN PROFILE OR ANOTHER USER'S
    page_name = "My Saved Recipes"

    # TODO - CHANGE TO REAL DATA FROM DB
    reviews = [{"name": "Spag Bol", "link": "", "review": "#" * 200}] * 20

    context_dict = {
        "page_name": page_name,
        "user_data": reviews,
        # needed for knowing if we are visiting our OWN profile or another users
        "own_profile": True,
        # needed since reusing templates
        "is_reviews_page": True,
    }

    return render(request, "pantry/user-data.html", context=context_dict)
