import os
from datetime import datetime

import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pantry_project.settings")
django.setup()

from django.contrib.auth.models import User
from django.core.files.images import ImageFile

from pantry.models import *
from pantry.views import SPACER

from django.contrib.auth.models import User
from pantry.models import Cuisine, Category, Recipe, UserProfile

# HELPERS


def add_cuisine(type):
    c = Cuisine.objects.get_or_create(type=type)[0]
    c.save()
    return c


def add_category(type):
    c = Category.objects.get_or_create(type=type)[0]
    c.save()
    return c


def add_user(username, password):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(password)
    user.save()
    return user


def add_userprofile(user, image, bio):
    userprofile = UserProfile.objects.get_or_create(user=user, bio=bio)[0]
    userprofile.save()
    userprofile.image = image
    userprofile.save()
    return userprofile


def add_recipe(recipe_data):
    recipe = Recipe.objects.create(
        user=recipe_data["user"],
        cuisine=recipe_data["cuisine"],
        title=recipe_data["title"],
        desc=recipe_data["desc"],
        ingredients=recipe_data["ingredients"],
        steps=recipe_data["steps"],
        prep=recipe_data["prep"],
        cook=recipe_data["cook"],
        difficulty=recipe_data["difficulty"],
    )
    recipe.categories.set(recipe_data["categories"])
    # save first so generate a recipe id
    recipe.save()
    recipe.image = recipe_data["image"]
    recipe.save()
    return recipe


def add_review(review_data):
    recipes = Recipe.objects.all()
    for recipe in recipes:
        # user cant review his own recipe
        if recipe.user == review_data["user"]:
            continue

        review = Review.objects.create(
            user=review_data["user"],
            recipe=recipe,
            review=review_data["review"],
            likes=review_data["likes"],
        )
        review.save()


# CREATE FUNCTIONS


def create_users_and_profiles():
    users_data = [
        {
            "username": "andrewS",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person1.jpeg", "rb")),
            "bio": "My favourite cuisine is Italian.",
        },
        {
            "username": "andrewM",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person2.jpeg", "rb")),
            "bio": "My favourite cuisine is Indian.",
        },
        {
            "username": "andrewH",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person3.jpeg", "rb")),
            "bio": "My favourite cuisine is Chinese.",
        },
        {
            "username": "nicole",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person4.jpeg", "rb")),
            "bio": "My favourite cuisine is Mexican.",
        },
        {
            "username": "jeval",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person5.jpeg", "rb")),
            "bio": "My favourite cuisine is Japanese.",
        },
        {
            "username": "layla",
            "password": "123456",
            "image": ImageFile(open("./populate_data/person6.jpeg", "rb")),
            "bio": "My favourite cuisine is Thai.",
        },
    ]

    for user_data in users_data:
        user_object = add_user(user_data["username"], user_data["password"])
        userprofile_object = add_userprofile(
            user_object, user_data["image"], user_data["bio"]
        )
        print(f"Created User: {user_object.username}\tCreated UserProfile")


def create_cuisines_and_categories():
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


def create_recipes():
    recipes_data = [
        {
            "user": User.objects.get(username="andrewS"),
            "cuisine": Cuisine.objects.get(type="Italian"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Spaghetti Carbonara",
            "image": ImageFile(open("./populate_data/spaghetti_carbonara.jpeg", "rb")),
            "desc": "Classic Italian pasta dish with eggs, cheese, bacon, and black pepper.",
            "ingredients": SPACER.join(["Pasta", "Eggs", "Parmesan Cheese", "Bacon"]),
            "steps": SPACER.join(
                [
                    "Boil pasta",
                    "Cook bacon",
                    "Mix eggs and cheese",
                    "Combine all with pasta",
                ]
            ),
            "prep": "0:20",
            "cook": "0:20",
            "difficulty": "intermediate",
        },
        {
            "user": User.objects.get(username="andrewM"),
            "cuisine": Cuisine.objects.get(type="Indian"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Butter Chicken",
            "image": ImageFile(open("./populate_data/butter_chicken.jpeg", "rb")),
            "desc": "Creamy Indian chicken dish made with butter, cream, and aromatic spices.",
            "ingredients": SPACER.join(["Chicken", "Butter", "Cream", "Spices"]),
            "steps": SPACER.join(
                [
                    "Marinate chicken",
                    "Cook in butter",
                    "Add cream and spices",
                    "Simmer until done",
                ]
            ),
            "prep": "0:30",
            "cook": "0:30",
            "difficulty": "expert",
        },
        {
            "user": User.objects.get(username="andrewH"),
            "cuisine": Cuisine.objects.get(type="Chinese"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Kung Pao Chicken",
            "image": ImageFile(open("./populate_data/kung_pao_chicken.jpeg", "rb")),
            "desc": "Spicy stir-fried Chinese dish made with chicken, peanuts, and vegetables.",
            "ingredients": SPACER.join(
                ["Chicken", "Peanuts", "Vegetables", "Soy Sauce"]
            ),
            "steps": SPACER.join(
                [
                    "Marinate chicken",
                    "Stir-fry with peanuts and vegetables",
                    "Add soy sauce",
                    "Serve hot",
                ]
            ),
            "prep": "0:25",
            "cook": "0:20",
            "difficulty": "expert",
        },
        {
            "user": User.objects.get(username="nicole"),
            "cuisine": Cuisine.objects.get(type="Mexican"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Vegetarian Tacos",
            "image": ImageFile(open("./populate_data/vegetarian_tacos.jpeg", "rb")),
            "desc": "Delicious vegetarian tacos loaded with beans, salsa, and avocado.",
            "ingredients": SPACER.join(["Tortillas", "Beans", "Salsa", "Avocado"]),
            "steps": SPACER.join(
                ["Warm tortillas", "Fill with beans, salsa, and avocado", "Enjoy!"]
            ),
            "prep": "0:15",
            "cook": "0:10",
            "difficulty": "intermediate",
        },
        {
            "user": User.objects.get(username="jeval"),
            "cuisine": Cuisine.objects.get(type="Japanese"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Sushi Rolls",
            "image": ImageFile(open("./populate_data/sushi_rolls.jpeg", "rb")),
            "desc": "Homemade sushi rolls with fresh fish, rice, and vegetables.",
            "ingredients": SPACER.join(["Sushi Rice", "Fish", "Nori", "Vegetables"]),
            "steps": SPACER.join(
                [
                    "Prepare sushi rice",
                    "Roll with fish and vegetables in nori sheets",
                    "Slice and serve",
                ]
            ),
            "prep": "0:40",
            "cook": "0:00",
            "difficulty": "expert",
        },
        {
            "user": User.objects.get(username="layla"),
            "cuisine": Cuisine.objects.get(type="Thai"),
            "categories": Category.objects.filter(
                type__in=["Low Fat", "Organic", "Vegetarian"]
            ),
            "title": "Pad Thai",
            "image": ImageFile(open("./populate_data/pad_thai.jpeg", "rb")),
            "desc": "Authentic Thai stir-fried noodles with shrimp, tofu, and peanuts.",
            "ingredients": SPACER.join(["Rice Noodles", "Shrimp", "Tofu", "Peanuts"]),
            "steps": SPACER.join(
                [
                    "Soak rice noodles",
                    "Stir-fry with shrimp, tofu, and peanuts",
                    "Serve hot",
                ]
            ),
            "prep": "0:30",
            "cook": "0:20",
            "difficulty": "expert",
        },
    ]

    for recipe_data in recipes_data:
        recipe = add_recipe(recipe_data)
        print(f"{recipe.title} has been created")


def create_reviews():
    reviews_data = [
        {
            "user": User.objects.get(username="layla"),
            "likes": 40,
            "review": "I loved this recipe!",
        },
        {
            "user": User.objects.get(username="nicole"),
            "likes": 25,
            "review": "The recipe was OK",
        },
        {
            "user": User.objects.get(username="jeval"),
            "likes": 19,
            "review": "This recipe proved to be a great addition to my kitchen!",
        },
        {
            "user": User.objects.get(username="andrewH"),
            "likes": 7,
            "review": "This was a great recipe!",
        },
        {
            "user": User.objects.get(username="andrewS"),
            "likes": 100,
            "review": "I really liked this one!",
        },
        {
            "user": User.objects.get(username="andrewM"),
            "likes": 22,
            "review": "It was not too bad...",
        },
    ]

    for review_data in reviews_data:
        add_review(review_data)
        username = review_data["user"]
        print(f"created reviews by user: {username}")


if __name__ == "__main__":
    print("Starting Rango population script...")
    create_users_and_profiles()
    create_cuisines_and_categories()
    create_recipes()
    create_reviews()
