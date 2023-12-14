
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API paths
    path("api/change_followers", views.change_followers, name="change_followers"),
    path("api/like", views.like, name="like"),
    path("api/likes/<str:post_id>", views.like_number, name="like_number"),
    path("api/edit_post", views.edit_post, name="edit_post"),
    path("api/post/<str:post_id>", views.update_post, name="update_post")
]
