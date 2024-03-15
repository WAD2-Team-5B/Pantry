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

    # user is using search bar
    if request.method == "POST":
        search_query = request.POST.get("search_query")
        # send in url parameters with get request
        return redirect(reverse("pantry:recipes") + "?search_query=" + search_query)

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

    # user is searching and not page refresh
    if request.GET.get("request", False):

        search_query = request.GET.get("search_query")

        # only display results if user has given a search query
        if not search_query:
            return render(request, "pantry/recipe-response.html")

        difficulties = request.GET.get("selected_difficulty").split(SPACER)
        cuisines = request.GET.get("selected_cuisines").split(SPACER)
        categories = request.GET.get("selected_categories").split(SPACER)
        sort = request.GET.get("selected_sort").split(SPACER)[0]

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

    # user was redirected from index page using search bar
    search_query = request.GET.get("search_query", False)

    # only find results if a search was given
    # (user could of accidentally hit submit from index page)
    if search_query:

        search_query_query = Q(title__startswith=search_query)
        recipes = Recipe.objects.filter(search_query_query)
        context_dict["recipes"] = recipes
        context_dict["search_query"] = search_query

    return render(request, "pantry/recipes.html", context=context_dict)


def signup(request):

    # user is signing up
    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
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

    # user is logging in
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

    # user is posting a review
    if request.method == "POST":

        request_review = request.POST.get("review")

        review = Review.objects.create(
            user=request.user, recipe=recipe, review=request_review
        )

        review.save()

    reviews = Review.objects.filter(recipe=recipe)
    # ingredients stored as single string with 'SPACER' delimiter
    ingredients = recipe.ingredients.split(SPACER)

    user = request.user
    other_user = User.objects.get(id=user_id)

    has_reviewed = has_reviewed_helper(request.user, recipe)

    context_dict = {
        "recipe": recipe,
        "reviews": reviews,
        "ingredients": ingredients,
        # steps stored as single string with 'SPACER' delimiter
        "steps": recipe.steps.split(SPACER),
        "my_profile": is_own_profile(user, other_user),
        "has_reviewed": has_reviewed,
    }

    return render(request, "pantry/recipe.html", context=context_dict)


@login_required
def create_a_recipe(request):

    # user is creating a recipe
    if request.method == "POST":

        # get our cuisine instance
        user_cuisine = Cuisine.objects.get(type=request.POST.get("cuisine"))

        # get our categories strings
        category_strings = request.POST.get("categories").split(SPACER)

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
        if category_strings:
            recipe.categories.set(Category.objects.filter(type__in=category_strings))

        # save first to generate a recipe id
        # (this is needed for saving image into correct media dir using recipe id)
        recipe.save()

        recipe.image = request.FILES.get("image")
        recipe.save()

        return redirect(
            reverse(
                "pantry:recipe",
                kwargs={"user_id": request.user.id, "recipe_id": recipe.id},
            )
        )

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict = {"cuisines": cuisines, "categories": categories}

    return render(request, "pantry/create-a-recipe.html", context=context_dict)


def user_profile(request, user_id):

    # user is searching users
    if request.GET.get("request", False):

        search_query = request.GET.get("search_query")

        search_query_query = Q(username__startswith=search_query)

        users = User.objects.filter(search_query_query)

        context_dict = {
            "users": users,
        }

        return render(request, "pantry/user-response.html", context=context_dict)

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

    # user is deleting their recipe
    if request.GET.get("request", False):

        recipe_id = request.GET.get("dataId")
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.delete()

        # check that we successfully deleted the object
        try:
            Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return HttpResponse("success")

        return HttpResponse("fail")

    return render(
        request,
        "pantry/user-data.html",
        context=get_user_data_context_dict(request, user_id, "Recipe", Recipe),
    )


def saved_recipes(request, user_id):

    # user deleting their bookmarked recipe
    if request.GET.get("request", False):

        recipe_id = request.GET.get("dataId")
        recipe = Recipe.objects.get(id=recipe_id)
        saved_recipe = SavedRecipes.objects.get(user=request.user, recipe=recipe)
        saved_recipe.delete()

        # check that we successfully deleted the object
        try:
            SavedRecipes.objects.get(user=request.user, recipe=recipe)
        except SavedRecipes.DoesNotExist:
            return HttpResponse("success")

        return HttpResponse("fail")

    return render(
        request,
        "pantry/user-data.html",
        context=get_user_data_context_dict(
            request, user_id, "Saved Recipe", SavedRecipes
        ),
    )


def user_reviews(request, user_id):

    # user is deleting their review
    if request.GET.get("request", False):

        review_id = request.GET.get("dataId")
        review = Review.objects.get(id=review_id)
        review.delete()

        # check that we successfully deleted the object
        try:
            Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return HttpResponse("success")

        return HttpResponse("fail")

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

        # delete account request
        delete_request = request.POST.get("delete-request")
        if delete_request == "true":
            user = User.objects.get(id=request.user.id)
            auth.logout(request)
            user.delete()
            return redirect(reverse("pantry:index"))

        # current info
        user = request.user

        # edit profile request
        changed_username = request.POST.get("changed_username")
        changed_password = request.POST.get("changed_password")
        changed_image = request.FILES.get("changed_image", False)
        changed_bio = request.POST.get("changed_bio")

        auth.logout(request)

        # check if username was changed
        if user.username != changed_username:
            user.username = changed_username
            user.save()
            print(f"changed username to {user.username}")

        # check if password was changed
        if changed_password != "":
            user.set_password(changed_password)
            user.save()
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

        auth.login(request, user)

        return redirect(reverse("pantry:user-profile", kwargs={"user_id": user.id}))

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
