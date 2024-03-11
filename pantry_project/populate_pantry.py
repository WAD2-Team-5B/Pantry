import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pantry_project.settings")

import django

django.setup()
from pantry.models import Cuisine, Category


def populate():

    cuisines = [
        {"type": "Japanese"},
        {"type": "Italian"},
        {"type": "Mexican"},
        {"type": "Chinese"},
        {"type": "Indian"},
        {"type": "Thai"},
        {"type": "Mediterranean"},
        {"type": "French"},
        {"type": "American"},
        {"type": "Korean"},
        {"type": "Vietnamese"},
        {"type": "Middle Eastern"},
        {"type": "African"},
        {"type": "Caribbean"},
        {"type": "South American"},
        {"type": "Eastern European"},
        {"type": "Scandinavian"},
        {"type": "British"},
        {"type": "Australian"},
    ]

    categories = [
        {"type": "Vegan"},
        {"type": "Vegetarian"},
        {"type": "Gluten Free"},
        {"type": "Dairy Free"},
        {"type": "Low Carb"},
        {"type": "Low Fat"},
        {"type": "Low Calorie"},
        {"type": "High Protein"},
        {"type": "High Fiber"},
        {"type": "Low Sodium"},
        {"type": "Sugar Free"},
        {"type": "Raw"},
        {"type": "Organic"},
        {"type": "Nut Free"},
        {"type": "Soy Free"},
        {"type": "Egg Free"},
        {"type": "Seafood Free"},
        {"type": "Peanut Free"},
        {"type": "Red Meat Free"},
        {"type": "White Meat Free"},
        {"type": "Alcohol Free"},
        {"type": "Oil Free"},
    ]

    for cuisine in cuisines:
        add_cuisine(cuisine["type"])

    for category in categories:
        add_category(category["type"])


def add_cuisine(type):
    c = Cuisine.objects.get_or_create(type=type)[0]
    c.save()
    return c


def add_category(type):
    c = Category.objects.get_or_create(type=type)[0]
    c.save()
    return c


if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()
