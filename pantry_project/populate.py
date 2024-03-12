import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pantry_project.settings')
django.setup()

from django.contrib.auth.models import User
from pantry.models import Cuisine, Category, Recipe, UserProfile

def create_users():
    users_data = [
        {"username": "andrewS", "bio": "My favourite cuisine is Italian."},
        {"username": "andrewM", "bio": "My favourite cuisine is Indian."},
        {"username": "andrewH", "bio": "My favourite cuisine is Chinese."},
        {"username": "nicole", "bio": "My favourite cuisine is Mexican."},
        {"username": "jeval", "bio": "My favourite cuisine is Japanese."},
        {"username": "layla", "bio": "My favourite cuisine is Thai."},
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(username=user_data['username'])
        if created:
            try:
                UserProfile.objects.create(user=user, bio=user_data['bio'])
            except Exception as e:
                print("Error creating user profile")

def create_recipes():
    cuisines = ["Italian", "Indian", "Chinese", "Mexican", "Japanese", "Thai"]
    for cuisine_name in cuisines:
        Cuisine.objects.get_or_create(type=cuisine_name)


    categories = ["Vegan", "Vegetarian ", "Gluten-Free", "Dairy-Free"]
    for category_name in categories:
        Category.objects.get_or_create(type=category_name)

    
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
            "prep_time": 20,
            "cook_time": 20,
            "difficulty": 2,
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
            "prep_time": 30,
            "cook_time": 30,
            "difficulty": 3,
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
            "prep_time": 25,
            "cook_time": 20,
            "difficulty": 3,
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
            "prep_time": 15,
            "cook_time": 10,
            "difficulty": 2,
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
            "prep_time": 40,
            "cook_time": 0,
            "difficulty": 4,
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
            "prep_time": 30,
            "cook_time": 20,
            "difficulty": 3,
            "no_of_saves": 20,
            "date_pub": datetime(2022, 3, 10, 12, 0, 0),
        },
    ]


    for recipe_data in recipes_data:
        user = User.objects.get(username=recipe_data["username"])
        cuisine = Cuisine.objects.get(type=recipe_data["cuisine"])
        recipe = Recipe.objects.create(
            user=user,
            cuisine=cuisine,
            title=recipe_data["title"],
            link=recipe_data["link"],
            image=recipe_data["image"],
            desc=recipe_data["desc"],
            ingredients=recipe_data["ingredients"],
            steps=recipe_data["steps"],
            prep=recipe_data["prep_time"],
            cook=recipe_data["cook_time"],
            difficulty=recipe_data["difficulty"],
            saves=recipe_data["no_of_saves"],
            pub_date=recipe_data["date_pub"]
        )


        for category_name in recipe_data["categories"]:
            try:
                category = Category.objects.get(type=category_name)
            except Category.DoesNotExist:
                category = Category.objects.create(type=category_name)
            recipe.categories.add(category)
        recipe.save()

def populate():
    create_users()
    create_recipes()

if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Population completed.")
