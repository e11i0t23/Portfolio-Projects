from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, "home/index.html")

def login_view(request, ref):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(f'/{ref if ref !="home" else ""}')
        else:
            return render(request, "home/login.html", {
                'ref': ref,
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "home/login.html", {
            'ref': ref
        })


def logout_view(request, ref):
    logout(request)
    return HttpResponseRedirect(f'/{ref if ref !="home" else ""}')


def register(request, ref):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "home/register.html", {
                'ref': ref,
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "home/register.html", {
                'ref': ref,
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(f'/{ref if ref !="home" else ""}')
    else:
        return render(request, "home/register.html", {
            'ref': ref
        })
