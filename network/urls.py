
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("compose", views.compose_post, name="compose"),
    path("posts", views.all_posts, name="posts"),
    path("like/<int:post_id>", views.like_post, name="like"),
]
