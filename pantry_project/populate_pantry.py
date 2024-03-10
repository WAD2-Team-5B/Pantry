import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pantry_project.settings")

import django

django.setup()
from pantry.models import Cuisine


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

    for cuisine in cuisines:
        add_cuisine(cuisine["type"])


def add_cuisine(type):
    c = Cuisine.objects.get_or_create(type=type)[0]
    c.save()
    return c


if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()
