from django.shortcuts import render

# TEMPLATE VIEWS


def index(request):
    return render(request, "pantry/index.html")
