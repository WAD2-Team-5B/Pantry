from django.shortcuts import render

# TEMPLATE VIEWS


def index(request):
    return render(request, "pantry/index.html")


def about(request):
    return render(request, "pantry/about.html")


def recipes(request):
    # TESTING PURPOSE
    recipes = [
        {
            "name": "Spaghetti Bolegnaise",
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
    context_dict = {"recipes": recipes}
    return render(request, "pantry/recipes.html", context=context_dict)
