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
    link = models.URLField()
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to='recipe_images')
    desc = models.CharField(max_length = 500)
    ingredients = models.CharField(max_length = 2000)
    steps = models.CharField(max_length = 10_000)
    prep_time = models.CharField(max_length=4)
    cook_time = models.CharField(max_length=4)
    difficulty = models.CharField(max_length=1)
    rating = models.FloatField(default=0)
    star_count = models.IntegerField(default=0)
    star_submissions = models.IntegerField(default=0)
    no_of_saves = models.IntegerField()
    date_pub = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # every time an instance of the model is saved to the DB we recalculate the avg star rating
        self.rating = round(self.star_count/self.star_submissions, 2)
        super(Recipe, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date_pub = models.DateTimeField('date published')

    class Meta:
        unique_together = ('user', 'recipe')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
    
class SavedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')
