from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q, Count, Avg
from pantry.models import *
from pantry.forms import *
from pantry.helpers import *

SPACER = "<SPACER>"

def index(request):

    # user is using search bar
    if request.method == "POST":
        search_query = request.POST.get("search_query")
        # send in url parameters with get request
        return redirect(reverse("pantry:recipes") + "?search_query=" + search_query)
    rated_recipes = Recipe.objects.annotate(rating=Avg("ratings__value"))
    highest_rated_recipes = rated_recipes.order_by("-rating", "-pub_date")[:10]
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

    context_dict = {}

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

        # queries
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

        # apply filters
        recipes = Recipe.objects.filter(
            search_query_query & difficulty_query & cuisine_query & category_query
        ).annotate(num_saves=Count("saves", distinct=True))

        recipes = recipes.annotate(rating=Avg("ratings__value"))
        
        # apply sort
        if sort == "rating":
            recipes = recipes.order_by("-rating")
        elif sort == "reviews":
            recipes = recipes.annotate(num_reviews=Count("reviews", distinct=True))
            recipes = recipes.order_by("-num_reviews")
        elif sort == "saves":
            recipes = recipes.order_by("-num_saves")
        else:
            recipes = recipes.order_by("-pub_date")

        context_dict["recipes"] = recipes

        return render(request, "pantry/recipe-response.html", context=context_dict)

    # user was redirected from index page
    elif request.GET.get("search_query", False):

        search_query = request.GET.get("search_query")

        # only display results if user has given a search query
        if not search_query:
            return render(request, "pantry/recipe-response.html")

        search_query_query = Q(title__startswith=search_query)
        recipes = Recipe.objects.filter(search_query_query).annotate(
            num_saves=Count("saves", distinct=True)
        )
        recipes = recipes.annotate(rating=Avg("ratings__value"))
        context_dict["recipes"] = recipes
        context_dict["search_query"] = search_query

    cuisines = Cuisine.objects.all().values_list("type", flat=True)
    categories = Category.objects.all().values_list("type", flat=True)

    context_dict["cuisines"] = cuisines
    context_dict["categories"] = categories

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
            profile.bio = "Hey there, I'm a new user!"
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

    context_dict = {}
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == "POST":

        # user is bookmarking
        if "data[bookmarked]" in request.POST:

            bookmarked = request.POST.get("data[bookmarked]")
            if bookmarked == "true":
                SavedRecipes.objects.get(user=request.user, recipe=recipe).delete()
                return return_ajax_success(
                    request.user, recipe, SavedRecipes, "success", "fail"
                )
            elif bookmarked == "false":
                SavedRecipes.objects.create(user=request.user, recipe=recipe).save()
                return return_ajax_success(
                    request.user, recipe, SavedRecipes, "fail", "success"
                )

        # user is rating
        elif "data[rating]" in request.POST:
            new_rating = request.POST.get("data[rating]")

            if int(new_rating) > 5:
                return HttpResponse("Invalid rating")


            prev_rating = StarredRecipes.objects.filter(
                user=request.user, recipe=recipe
            )
            # delete if previously rated
            if prev_rating.exists():
                prev_rating.delete()
            
            # add new rating
            StarredRecipes.objects.create(
                user=request.user, recipe=recipe, value=new_rating
            )
            return return_ajax_success(
                request.user, recipe, StarredRecipes, "fail", "success"
            )

        # user is posting a review
        elif request.POST.get("reason") == "review":

            request_review = request.POST.get("review")
            Review.objects.create(
                user=request.user, recipe=recipe, review=request_review
            ).save()

    # logged in user data
    if request.user.is_authenticated:
        # bookmark
        bookmark_exists = SavedRecipes.objects.filter(user=request.user, recipe=recipe)
        context_dict["bookmarked"] = True if bookmark_exists else False

        # liking reviews
        liked_reviews = LikedReviews.objects.filter(
            user=request.user, review__recipe=recipe
        )
        liked_review_ids = list(liked_reviews.values_list("review__id", flat=True))
        context_dict["liked_reviews"] = liked_review_ids

        # star rating
        try:
            user_rating = StarredRecipes.objects.get(user=request.user, recipe=recipe)
            context_dict["user_rating"] = user_rating.value
        except StarredRecipes.DoesNotExist:
            context_dict["user_rating"] = 0
        # make sure not to double count by excluding users rating
        context_dict["all_ratings"] = list(
            recipe.ratings.all()
            .exclude(user=request.user)
            .values_list("value", flat=True)
        )

    # general page data
    other_user = User.objects.get(id=user_id)
    has_reviewed = has_reviewed_helper(request.user, recipe)
    if not "all_ratings" in context_dict:
        context_dict["all_ratings"] = list(
            recipe.ratings.all().values_list("value", flat=True)
        )

    context_dict["recipe"] = recipe
    context_dict["reviews"] = Review.objects.filter(recipe=recipe)
    context_dict["ingredients"] = recipe.ingredients.split(SPACER)
    context_dict["steps"] = recipe.steps.split(SPACER)
    context_dict["my_profile"] = is_own_profile(request.user, other_user)
    context_dict["has_reviewed"] = has_reviewed
    context_dict["saves"] = SavedRecipes.objects.filter(recipe=recipe).count()

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
        # return top 10
        users = User.objects.filter(username__startswith=search_query)[:10]
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
    if request.method == "POST":
        return delete_user_data(request, Recipe)
    else:
        return render(
            request,
            "pantry/user-data.html",
            context=get_user_data_context_dict(request, user_id, "Recipe", Recipe),
        )


def saved_recipes(request, user_id):

    # user deleting their bookmarked recipe
    if request.method == "POST":
        return delete_user_data(request, SavedRecipes)
    else:
        return render(
            request,
            "pantry/user-data.html",
            context=get_user_data_context_dict(
                request, user_id, "Saved Recipe", SavedRecipes
            ),
        )


def user_reviews(request, user_id):

    # user is deleting their review
    if request.method == "POST":
        return delete_user_data(request, Review)
    else:
        return render(
            request,
            "pantry/user-data.html",
            context=get_user_data_context_dict(
                request, user_id, "Reviewed Recipe", Review
            ),
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

        # check if username was changed
        if user.username != changed_username:

            # check if username is avaliable
            exists = User.objects.filter(username=changed_username)
            if exists:
                context_dict = {
                    "userprofile": userprofile,
                    "error": "Username already exists!",
                }
                return render(request, "pantry/edit-profile.html", context=context_dict)

            user.username = changed_username
            user.save()
            print(f"changed username to {user.username}")

        auth.logout(request)

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


@login_required
def like_review(request):

    review_id = request.POST.get("data[reviewId]")
    user = request.user
    review = Review.objects.get(id=review_id)
    like = request.POST.get("data[like]")

    if like == "true":
        if not LikedReviews.objects.filter(review=review, user=user).exists(): # make sure user has not already liked review
            LikedReviews.objects.create(user=user, review=review)
            print("created")
            review.likes += 1
    else:
        liked_review = LikedReviews.objects.get(review=review, user=user)
        liked_review.delete()
        print("deleted")
        review.likes -= 1

    review.save()

    return HttpResponse("success")
