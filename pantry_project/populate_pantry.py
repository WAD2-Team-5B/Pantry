import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pantry_project.settings')
django.setup()

from django.contrib.auth.models import User
from pantry.models import Cuisine, Category, Recipe, UserProfile

def create_users_and_profiles():
    users_data = [
        {"username": "andrewS", "bio": "My favourite cuisine is Italian."},
        {"username": "andrewM", "bio": "My favourite cuisine is Indian."},
        {"username": "andrewH", "bio": "My favourite cuisine is Chinese."},
        {"username": "nicole", "bio": "My favourite cuisine is Mexican."},
        {"username": "jeval", "bio": "My favourite cuisine is Japanese."},
        {"username": "layla", "bio": "My favourite cuisine is Thai."},
    ]
    
    for user_data in users_data:
        user_object, created = User.objects.get_or_create(username=user_data['username'])
        profile, profile_created = UserProfile.objects.get_or_create(user=user_object, defaults={'bio': user_data['bio']})
        print(f"User: {user_object.username}, Profile created: {profile_created}")

def populate_cuisines_and_categories():
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
    c, created = Cuisine.objects.get_or_create(type=type)
    return c


def add_category(type):
    c, created = Category.objects.get_or_create(type=type)
    return c

def create_recipes():
    recipes_data = [
        {
            "username": "andrewS",
            "cuisine": "Italian",
            "categories": [" "],
            "title": "Spaghetti Carbonara",
            "link": "https://example.com/recipe1",
            "image": "path/to/image.jpg",
            "desc": "Classic Italian pasta dish with eggs, cheese, bacon, and black pepper.",
            "ingredients": "Pasta, Eggs, Parmesan Cheese, Bacon",
            "steps": "Boil pasta. Cook bacon. Mix eggs and cheese. Combine all with pasta.",
            "prep": 20,
            "cook": 20,
            "difficulty": 2,
            "rating": 3.0,
            "no_of_saves": 10,
            "date_pub": datetime(2024, 3, 5, 12, 0, 0),
        },
        {
            "username": "andrewM",
            "cuisine": "Indian",
            "categories": [" "],
            "title": "Butter Chicken",
            "link": "https://example.com/recipe2",
            "image": "path/to/image.jpg",
            "desc": "Creamy Indian chicken dish made with butter, cream, and aromatic spices.",
            "ingredients": "Chicken, Butter, Cream, Spices",
            "steps": "Marinate chicken. Cook in butter. Add cream and spices. Simmer until done.",
            "prep": 30,
            "cook": 30,
            "difficulty": 3,
            "rating": 4.0,
            "no_of_saves": 15,
            "date_pub": datetime(2023, 3, 6, 12, 0, 0),
        },
        
        {
            "username": "andrewH",
            "cuisine": "Chinese",
            "categories": [" "],
            "title": "Kung Pao Chicken",
            "link": "https://example.com/recipe3",
            "image": "path/to/image.jpg",
            "desc": "Spicy stir-fried Chinese dish made with chicken, peanuts, and vegetables.",
            "ingredients": "Chicken, Peanuts, Vegetables, Soy Sauce",
            "steps": "Marinate chicken. Stir-fry with peanuts and vegetables. Add soy sauce. Serve hot.",
            "prep": 25,
            "cook": 20,
            "difficulty": 3,
            "rating": 4.0,
            "no_of_saves": 12,
            "date_pub": datetime(2022, 3, 7, 12, 0, 0),
        },
        {
            "username": "nicole",
            "cuisine": "Mexican",
            "categories": [" "],
            "title": "Vegetarian Tacos",
            "link": "https://example.com/recipe4",
            "image": "path/to/image.jpg",
            "desc": "Delicious vegetarian tacos loaded with beans, salsa, and avocado.",
            "ingredients": "Tortillas, Beans, Salsa, Avocado",
            "steps": "Warm tortillas. Fill with beans, salsa, and avocado. Enjoy!",
            "prep": 15,
            "cook": 10,
            "difficulty": 2,
            "rating": 4.0,
            "no_of_saves": 18,
            "date_pub": datetime(2022, 3, 8, 12, 0, 0),
        },
        {
            "username": "jeval",
            "cuisine": "Japanese",
            "categories": [" "],
            "title": "Sushi Rolls",
            "link": "https://example.com/recipe5",
            "image": "path/to/image.jpg",
            "desc": "Homemade sushi rolls with fresh fish, rice, and vegetables.",
            "ingredients": "Sushi Rice, Fish, Nori, Vegetables",
            "steps": "Prepare sushi rice. Roll with fish and vegetables in nori sheets. Slice and serve.",
            "prep": 40,
            "cook": 0,
            "difficulty": 4,
            "rating": 4.0,
            "no_of_saves": 25,
            "date_pub": datetime(2022, 3, 9, 12, 0, 0),
        },
        {
            "username": "layla",
            "cuisine": "Thai",
            "categories": [" "],
            "title": "Pad Thai",
            "link": "https://example.com/recipe6",
            "image": "path/to/image.jpg",
            "desc": "Authentic Thai stir-fried noodles with shrimp, tofu, and peanuts.",
            "ingredients": "Rice Noodles, Shrimp, Tofu, Peanuts",
            "steps": "Soak rice noodles. Stir-fry with shrimp, tofu, and peanuts. Serve hot.",
            "prep": 30,
            "cook": 20,
            "difficulty": 3,
            "rating": 5.0,
            "no_of_saves": 20,
            "date_pub": datetime(2022, 3, 10, 12, 0, 0),
        },
    ]


    for recipe_data in recipes_data:
        user = User.objects.get(username=recipe_data["username"])
        cuisine = Cuisine.objects.get(type=recipe_data["cuisine"])
        prep_str = str(recipe_data["prep"])
        cook_str = str(recipe_data["cook"])
        difficulty_str = str(recipe_data["difficulty"])
        

        recipe = Recipe.objects.create(
            user=user,
            cuisine=cuisine,
            title=recipe_data["title"],
            link=recipe_data["link"],
            desc=recipe_data["desc"],
            ingredients=recipe_data["ingredients"],
            steps=recipe_data["steps"],
            prep=prep_str,
            cook=cook_str,
            difficulty=difficulty_str,
            rating=recipe_data.get("rating", 0),
            reviews=recipe_data.get("reviews", 0),
            star_count=recipe_data.get("star_count", 0),
            star_submissions=recipe_data.get("star_submissions", 0),
            saves=recipe_data.get("no_of_saves", 0),
            pub_date=recipe_data["date_pub"]
        )


        for category_name in recipe_data["categories"]:
            if category_name.strip():
                category = Category.objects.get_or_create(type=category_name.strip())
                recipe.categories.add(category)
    recipe.save()
    print(f"{recipe_data} has been created")


def populate():
    print("Starting population script ....")
    create_users_and_profiles()
    populate_cuisines_and_categories()
    create_recipes()

if __name__ == '__main__':
    populate()