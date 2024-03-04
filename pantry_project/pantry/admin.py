from django.contrib import admin
from pantry.models import Recipe, Review, SavedRecipes, User, Cuisine, Category

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(SavedRecipes)
admin.site.register(User)
admin.site.register(Cuisine)
admin.site.register(Category)
