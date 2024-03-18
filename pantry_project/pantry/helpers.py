from django.http import HttpResponse
from pantry.models import *

# HELPER FUNCTIONS


def is_own_profile(user, other_user):
    if user.is_authenticated and user.id == other_user.id:
        own_profile = True
    else:
        own_profile = False

    return own_profile


def get_page_name(user, other_user, page_string):

    own_profile = is_own_profile(user, other_user)

    if own_profile:
        page_name = "My " + page_string + "s"
    else:
        page_name = other_user.username + "'s " + page_string + "s"

    return page_name, own_profile


def get_user_data_context_dict(request, user_id, page_string, model):

    user = request.user
    other_user = User.objects.get(id=user_id)

    page_name, own_profile = get_page_name(user, other_user, page_string)

    user_data = model.objects.filter(user=other_user)

    context_dict = {
        "page_name": page_name,
        "user_data": user_data,
        # needed for knowing if we are visiting our OWN profile or another users
        "own_profile": own_profile,
    }

    if model == Review:
        context_dict["is_reviews_page"] = True
    elif model == SavedRecipes:
        context_dict["is_saved_recipes_page"] = True

    return context_dict


def has_reviewed_helper(user, recipe):

    if not user.is_authenticated:
        return False

    user_review = Review.objects.filter(user=user, recipe=recipe)

    if user_review:
        return True

    return False

def delete_user_data(request, model):
    data_id = request.POST.get('data[dataId]')
    print(request.POST.get("csrfmiddlewaretoken"))
    
    stored_data = model.objects.get(id=data_id)
    stored_data.delete()

    # check that we successfully deleted the object
    try:
        model.objects.get(id=data_id)
    except model.DoesNotExist:
        return HttpResponse("success")

    return HttpResponse("fail")
