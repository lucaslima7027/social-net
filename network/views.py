from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, UserNumber


def index(request):
    # Render all posts views 
    all_posts = getPosts(request)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 3)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        "page_obj": page_obj 
    })


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

            # Attempt to create user numbers
            user_numbers = UserNumber(user=user)
            user_numbers.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def returnHtml(request, file_name):
    return render(request, f'network/{file_name}.html')

def following(request):
    username = request.user.username
    print("USERNAME = " + username)

    uri = request.get_full_path()

    all_posts = getPosts(request, uri)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 3)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        "page_obj": page_obj 
    })

def getPosts(request, page=""):
    if (page == "/following"):
        following_ids = UserNumber.objects.values_list('following',flat= True).filter(user__username = request.user.username)
        all_posts = Post.objects.filter(creator_id__in = set(following_ids)).order_by('-date')
        return all_posts
    else:
        return  Post.objects.exclude(creator__username = request.user.username).order_by('-date')