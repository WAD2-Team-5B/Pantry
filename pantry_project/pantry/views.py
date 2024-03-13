from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q, Count
from pantry_project.settings import MEDIA_DIR
from django.utils.decorators import method_decorator
from django.views import View

from pantry.models import *
from pantry.forms import *
from pantry.helpers import *

SPACER = "<SPACER>"

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

    # TODO - if redirect then user is coming from the index page and we need to display search query results

    # user is searching and not page refresh
    if request.GET.get("request", False):

        search_query = request.GET.get("search_query")
        difficulties = request.GET.get("selected_difficulty").split(SPACER)
        cuisines = request.GET.get("selected_cuisines").split(SPACER)
        categories = request.GET.get("selected_categories").split(SPACER)
        sort = request.GET.get("selected_sort").split(SPACER)[0]

        search_query_query = Q()

        # check the user started searching
        if search_query:
            search_query_query = Q(title__startswith=search_query)

        difficulty_query = Q()

        for difficulty in difficulties:
            if difficulty:
                difficulty_query |= Q(difficulty=difficulty)

        cuisine_query = Q()

        for cuisine in cuisines:
            if cuisine:
                cuisine_query |= Q(cuisine=Cuisine.objects.get(type=cuisine))

        category_query = Q()

        for category in categories:
            if category:
                category_query |= Q(categories=Category.objects.get(type=category))

        recipes = Recipe.objects.filter(
            search_query_query & difficulty_query & cuisine_query & category_query
        )

        if sort == "rating":
            recipes = recipes.order_by("-rating")
        elif sort == "reviews":
            recipes = recipes.order_by("-reviews")
        elif sort == "saves":
            # Count() will count number of review objects
            # we create our own pseudo field for number of review objects and order by this field
            recipes = recipes.annotate(num_reviews=Count("reviews")).order_by(
                "-num_reviews"
            )
        else:
            recipes = recipes.order_by("-pub_date")

        context_dict = {
            "recipes": recipes,
        }

        return render(request, "pantry/recipe-response.html", context=context_dict)

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict = {
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
    reviews = Review.objects.filter(recipe=recipe)

    print(recipe.rating)

    # additional
    ingredients = recipe.ingredients.split(SPACER)

    context_dict = {
        "recipe": recipe,
        "reviews": reviews,
        "ingredients": ingredients,
        "steps": recipe.steps.split(SPACER),
    }

    return render(request, "pantry/recipe.html", context=context_dict)


@login_required
def create_a_recipe(request):

    # user is submitting the form
    if request.method == "POST":

        # get our cuisine instance
        user_cuisine = Cuisine.objects.get(type=request.POST.get("cuisine"))

        # get our categories strings
        category_strings = request.POST.get("categories").split(SPACER)
        print(category_strings)

        recipe = Recipe.objects.create(
            user=request.user,
            cuisine=user_cuisine,
            title=request.POST.get("name"),
            desc=request.POST.get("description"),
            ingredients=request.POST.get("ingredients"),
            steps=request.POST.get("steps"),
            prep=request.POST.get("prep"),
            cook=request.POST.get("cook"),
            difficulty=request.POST.get("difficulty"),
        )

        # add our category instances
        recipe.categories.set(Category.objects.filter(type__in=category_strings))

        # save first so generate a recipe id
        recipe.save()

        recipe.image = request.FILES.get("image")
        recipe.save()

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict = {"cuisines": cuisines, "categories": categories}

    return render(request, "pantry/create-a-recipe.html", context=context_dict)


def user_profile(request, user_id):

    user = request.user
    other_user = User.objects.get(id=user_id)
    own_profile = is_own_profile(user, other_user)
    other_user_profile = UserProfile.objects.get(user=other_user)

    context_dict = {
        "profileuser": other_user,
        "profileuser_profile": other_user_profile,
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
def edit_profile(request):

    userprofile = UserProfile.objects.get(user=request.user)

    # user submitting request
    if request.method == "POST":
        changed_username = request.POST.get("changed_username")
        changed_password = request.POST.get("changed_password")
        changed_image = request.FILES.get("changed_image", False)
        changed_bio = request.POST.get("changed_bio")

        # check if username is actually changed
        if request.user.username != changed_username:
            request.user.username = changed_username
            request.user.save()
            print(f"changed username to {request.user.username}")

        # check if password is actually changed
        if changed_password != "":
            request.user.set_password(changed_password)
            request.user.save()
            print("changed password")

        # check if image was changed
        if changed_image:
            userprofile.image = changed_image
            userprofile.save()
            print("changed image")

        # check if bio was changed
        if userprofile.bio != changed_bio:
            userprofile.bio = changed_bio
            userprofile.save()
            print("changed bio")

    context_dict = {"userprofile": userprofile}

    return render(request, "pantry/edit-profile.html", context=context_dict)


class SaveRecipeView(View):
    @method_decorator(login_required)
    def get(self, request):
        recipe_id = request.GET["recipe_id"]

        try:
            recipe = Recipe.objects.get(id=int(recipe_id))
        except Recipe.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        recipe.saves = recipe.save + 1
        recipe.save()

        return HttpResponse(recipe.saves)


class LikeReviewView(View):
    @method_decorator(login_required)
    def get(self, request):
        reveiw_id = request.GET["review_id"]

        try:
            review = Review.objects.get(id=int(reveiw_id))
        except Review.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        review.likes = review.likes + 1
        review.save()

        return HttpResponse(review.likes)
