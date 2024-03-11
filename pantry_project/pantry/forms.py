from django import forms
from django.contrib.auth.models import User
from pantry.models import UserProfile, Recipe, Review, Cuisine


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "confirm-password"})
    )

    class Meta:
        model = User
        fields = ("username", "password")


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    image = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"id": "image"})
    )
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"id": "bio"}))

    class Meta:
        model = UserProfile
        fields = ("image", "bio")


# class CreateARecipeForm(forms.ModelForm):

#     title = forms.CharField(
#         widget=forms.TextInput(
#             attrs={"id": "recipe-name", "placeholder": "recipe title"}
#         )
#     )
#     prep = forms.CharField(
#         widget=forms.TextInput(attrs={"id": "recipe-prep", "placeholder": "prep"})
#     )
#     cook = forms.CharField(
#         widget=forms.TextInput(attrs={"id": "recipe-cook", "placeholder": "cook"})
#     )
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(attrs={"id": "recipe-image"})
#     )
#     desc = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 "id": "recipe-description",
#                 "placeholder": "description",
#                 # override the default rows and cols for the css
#                 "rows": "",
#                 "cols": "",
#             }
#         )
#     )
#     ingredients = forms.CharField(widget=forms.HiddenInput(attrs={"id": "ingredients"}))
#     difficulty = forms.CharField(widget=forms.HiddenInput(attrs={"id": "difficulty"}))
#     steps = forms.CharField(widget=forms.HiddenInput(attrs={"id": "steps"}))
#     categories = forms.CharField(widget=forms.HiddenInput(attrs={"id": "categories"}))
#     cuisine = forms.ModelChoiceField(queryset=Cuisine.objects.all())

#     class Meta:
#         model = Recipe
#         fields = (
#             "title",
#             "prep",
#             "cook",
#             "image",
#             "desc",
#             "ingredients",
#             "difficulty",
#             "steps",
#             "categories",
#             "cuisine",
#         )
