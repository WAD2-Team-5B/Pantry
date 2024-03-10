from django import forms
from django.contrib.auth.models import User
from pantry.models import UserProfile, Recipe, Review

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"id":"username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"confirm-password"}))

    class Meta:
        model = User
        fields = ("username", "password")


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={"id":"image"}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={"id":"bio"}))

    class Meta:
        model = UserProfile
        fields = ("image", "bio")
