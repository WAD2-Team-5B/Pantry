from django.db import models
from django.contrib.auth.models import User

import os


class Cuisine(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type


class Category(models.Model):
    type = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.type


class Recipe(models.Model):

    # helper
    def recipe_upload_path(self, filename):
        # return correct media folder using their user ID and recipe ID
        dir_name = "user-id-" + str(self.user.pk)
        recipe_id = "recipe-id-" + str(self.pk)
        return os.path.join(dir_name, "recipes", recipe_id, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    link = models.URLField()
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=recipe_upload_path)
    desc = models.CharField(max_length=500)
    ingredients = models.CharField(max_length=2000)
    steps = models.CharField(max_length=10_000)
    prep = models.CharField(max_length=4)
    cook = models.CharField(max_length=4)
    difficulty = models.CharField(max_length=1)
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)
    star_count = models.IntegerField(default=0)
    star_submissions = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # every time an instance of the model is saved to the DB we recalculate the avg star rating
        if self.star_submissions != 0:
            # Calculate average star rating
            self.rating = round(self.star_count / self.star_submissions, 2)
        else:
            self.rating = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date_pub = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=500)

    def save(self, *args, **kwargs):

        # call save as usual
        super().save(*args, **kwargs)

        # Increment reviews_count in the associated Recipe
        self.recipe.reviews_count = Review.objects.filter(recipe=self.recipe).count()
        self.recipe.save()

    class Meta:
        unique_together = ("user", "recipe")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images", blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class SavedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        # call save as usual
        super().save(*args, **kwargs)

        # Increment saves in the associated Recipe
        self.recipe.saves = SavedRecipes.objects.filter(recipe=self.recipe).count()
        self.recipe.save()

    class Meta:
        unique_together = ("user", "recipe")
