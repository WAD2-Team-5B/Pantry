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
        # get base filename
        filename = os.path.basename(filename)
        # return correct media folder using their user ID and recipe ID
        dir_name = "user-id-" + str(self.user.pk)
        recipe_id = "recipe-id-" + str(self.pk)
        return os.path.join(dir_name, "recipes", recipe_id, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=recipe_upload_path)
    desc = models.CharField(max_length=500)
    ingredients = models.CharField(max_length=2000)
    steps = models.CharField(max_length=10_000)
    prep = models.CharField(max_length=4)
    cook = models.CharField(max_length=4)
    difficulty = models.CharField(max_length=1)
    rating = models.FloatField(default=0)
    star_count = models.IntegerField(default=0)
    star_submissions = models.IntegerField(default=0)
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


class UserProfile(models.Model):

    # helper
    def userprofile_upload_path(self, filename):
        # get base filename
        filename = os.path.basename(filename)
        # return correct media folder using their user ID and recipe ID
        dir_name = "user-id-" + str(self.user.pk)
        return os.path.join(dir_name, "profile", filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=userprofile_upload_path, blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")

    review = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")


class SavedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saves")

    class Meta:
        unique_together = ("user", "recipe")


class LikedReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


class StarredRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="stars")
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        self.recipe.star_submissions += 1
        self.recipe.star_count += self.value

        self.recipe.save()
       
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        
        self.recipe.star_submissions -= 1
        self.recipe.star_count -= self.value

        self.recipe.save()

        

