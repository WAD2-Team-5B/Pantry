from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Review, SavedRecipes


# Signal receiver function for pre_delete
@receiver(pre_delete, sender=Review)
def update_reviews_count_on_review_delete(sender, instance, **kwargs):
    recipe = instance.recipe
    recipe.reviews_count = Review.objects.filter(recipe=recipe).count() - 1
    recipe.save()


@receiver(pre_delete, sender=SavedRecipes)
def update_saves_on_unsave(sender, instance, **kwargs):
    recipe = instance.recipe
    recipe.saves = Review.objects.filter(recipe=recipe).count() - 1
    recipe.save()
