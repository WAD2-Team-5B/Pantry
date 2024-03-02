from django.shortcuts import render

# from .models import Recipe

# TEMPLATE VIEWS


def index(request):
    # highest_rated_recipes = Recipe.objects.order_by("-rating")[:10].values(
    #     "name", "link", "image"
    # )
    # newest_recipes = Recipe.objects.order_by("-created_at")[:10].values(
    #     "name", "link", "image"
    # )

    context_dict = {
        # "highest_rated_recipes": list(highest_rated_recipes),
        # "newest_recipes": list(newest_recipes),
        # "num_highest_rated": len(highest_rated_recipes),
        # "num_newest": len(newest_recipes),
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


def login(request):
    context_dict = {"success": True}
    return render(request, "pantry/login.html", context=context_dict)


def signup(request):
    return render(request, "pantry/signup.html")


def recipe(request):
    # TESTING PURPOSES
    # would use real data from database
    context_dict = {
        # header
        "user": "John12345",
        "user_id": "",
        "name": "Spag Bol",
        "date_pub": "2021-09-21",
        # description
        "image": "",
        "description": (("#" * 50) + "\n") * 10,
        # sub info
        "rating": 4.67,
        "saves": 34,
        "difficulty": "beginner",
        "cuisine": "Italian",
        "prep": "1:30",
        "cook": "0:30",
        # main info
        "steps": [
            "#" * 20,
        ]
        * 10,
        "categories": ["Vegan", "Vegetarian", "Pescatarian"],
        "ingredients": [
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
        ],
    }

    # TESTING
    return render(request, "pantry/recipe.html", context=context_dict)
