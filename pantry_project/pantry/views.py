from django.shortcuts import render
from pantry.models import Recipe

# TEMPLATE VIEWS


def index(request):

    # UNCOMMENT ONCE DATABASE IS SET UP
   #newest_recipes = Recipe.objects.order_by("-rating")[:10].values("name", "photo")
   # newest_recipes = Recipe.objects.order_by("-pub_date")[:10].values("name", "photo")

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
    highest_rated_recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 10
    newest_recipes = [{"name": "Spag Bol", "link": "", "image": ""}] * 10

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


def login(request):
    context_dict = {"success": True}
    return render(request, "pantry/login.html", context=context_dict)


def signup(request):
    return render(request, "pantry/signup.html")


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
            "user": "GreatCook123",
            "likes": 17,
            "date_pub": "2023-10-21",
            "review": "#" * 150,
        }
    ] * 5

    # TESTING PURPOSES UNTIL DATABASE IS SET UP
    context_dict = {
        # header
        "user": "John12345",
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
