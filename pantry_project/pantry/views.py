from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

# TEMPLATE VIEWS


def index(request):
    return render(request, "pantry/index.html")


def about(request):
    return render(request, "pantry/about.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse("pantry:index"))
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "pantry/login.html")
        # return user_login_bypass(request)


## REMOVE
# username:testuser, password:12345
def user_login_bypass(request):
    user = authenticate(username="testuser", password="12345")
    login(request, user)
    return redirect(reverse("pantry:index"))


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("pantry:index"))
