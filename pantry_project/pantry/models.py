from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Cuisine(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type

class Category(models.Model):
    type = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.type


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    title = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to='recipe_images')
    desc = models.CharField(max_length = 500)
    ingredients = models.CharField(max_length = 2000)
    steps = models.CharField(max_length = 10_000)
    prep_time = models.CharField(max_length=4)
    cook_time = models.CharField(max_length=4)
    difficulty = models.CharField(max_length=1)
    star_count = models.IntegerField()
    star_submissions = models.IntegerField()
    no_of_saves = models.IntegerField()
    date_pub = models.DateField()
    
    
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)

    likes = models.IntegerField(default=0)
    date_pub = models.DateField('date published')

    class Meta:
        unique_together = ('user', 'recipe')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
    
class SavedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')
