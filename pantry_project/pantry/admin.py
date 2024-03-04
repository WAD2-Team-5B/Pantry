from django.contrib import admin
from pantry.models import Recipe, Review, SavedRecipes, Cuisine, Category, UserProfile

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(SavedRecipes)
admin.site.register(UserProfile)
admin.site.register(Cuisine)
admin.site.register(Category)
