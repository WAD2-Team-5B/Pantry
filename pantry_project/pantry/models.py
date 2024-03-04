from django.db import models

# Create your models here.

def Recipe(models.Model):
    title = models.CharField(max_length = 200)
    photo_url = models.URLField(max_length = 500)
    desc = models.CharField(max_length = 500)
    ingredients = models.CharField(max_length = 2000)
    steps = models.CharField(max_length = 10_000)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    difficulty = modelsIntegerField()
    star_rating = models.IntegerField()
    no_of_saves = models.IntegerField()
    date_pub = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title
    

    
def User(models.Model):
    likes = models.IntegerField()
    date_pub = models.DateField()
    
