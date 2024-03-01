from django.shortcuts import render

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

    context_dict = {"recipes": recipes}
    return render(request, "pantry/recipes.html", context=context_dict)
