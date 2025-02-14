from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User
from network.models import Post


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
def compose_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        user = request.user
        if content:
            post = Post.objects.create(user=user, content=content)
            post.save()
            return JsonResponse({"status": "success", "message": "Post created successfully"})
        else:
            return JsonResponse({"status": "error", "message": "Content cannot be empty"})

def all_posts(request):
    posts = Post.objects.all()
    posts = [post.serialize() for post in posts]
    posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)
    return JsonResponse(posts, safe=False)

def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        post.save()
        return JsonResponse({"status": "success", "message": "Post unliked successfully"})
    else:
        post.likes.add(user)
        post.save()
        return JsonResponse({"status": "success", "message": "Post liked successfully"})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
