from django.db import models

# Create your models here.

def Recipe(models.Model):
    title = models.CharField(max_length = 200)
    photo_url = models.CharField(max_length = 500)
    desc = models.CharField(max_length = 500)
    ingredients = models.CharField(max_length = 2000)
    steps = models.Char
    
    
    def __str__(self):
        return self.title