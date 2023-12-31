from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from .models import User, UserNumber, Post


def index(request):
    # Create a new post
    if request.method == "POST":
        content, message = createNewPost(request)
    
    else:
        content, message = "", ""
            
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
        "page_obj": page_obj,
        "message": message,
        "content": content
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
    if request.method == "POST":
        content, message = createNewPost(request)

    else:
        content, message = "",""

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
        "page_obj": page_obj,
        "content": content,
        "message": message
        })

def profile(request, username):
    actual_user = request.user
    user_numbers = UserNumber.objects.get(user__username=username)

    followers = user_numbers.followers.all() 
    following_count = user_numbers.following.all().count()
    followers_count = user_numbers.followers.all().count()
    
    if actual_user in followers:
        is_follower = True
    else:
        is_follower = False

    all_posts = getPosts(request, "/profile", user_numbers.user.username)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts, 3)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "user_numbers": user_numbers,
        "following_count": following_count,
        "followers_count": followers_count,
        "profile": True,
        "is_follower": is_follower
    })

# Checks if action is follow or unfollow and update DB
def change_followers(request):
    visitor_username = request.POST["visitor"]
    visited_username = request.POST["visited"]
    action = request.POST["action"]
    visitor = UserNumber.objects.get(user__username = visitor_username)
    visited = UserNumber.objects.get(user__username = visited_username)
    
    if action == "unfollow":
        visitor.following.remove(visited.user)
        visitor.save()
        
        visited.followers.remove(visitor.user)
        visited.save()
    else:
        visitor.following.add(visited.user)
        visitor.save()
        
        visited.followers.add(visitor.user)
        visited.save()

    return HttpResponseRedirect(reverse("profile", kwargs={"username":visited_username}))

def like(request):
    
    if request.method == "PUT":
        body = json.loads(request.body)
        post_id = body["id"]

        like_post = Post.objects.get(id = post_id)
        
        likes_ids = Post.objects.values_list('likes',flat= True).filter(id = post_id)

        user_liked = Post.objects.filter(creator_id__in = set(likes_ids))

        if user_liked:
            like_post.likes.remove(request.user)
            
        else:
            like_post.likes.add(request.user)
        
        like_post.save()
        return HttpResponse(200)
            

def like_number(request, post_id):
    post = Post.objects.get(id = post_id)
    post_likes = post.likes.count()
    
    return HttpResponse(json.dumps(post_likes), content_type='application/json')


def edit_post(request):
    data = json.loads(request.body)
    post_id = data["id"]
    new_content = data["content"]
    
    post = Post.objects.get(id=post_id)
    creator = post.creator.username

    if request.user.username == creator:
        post.content = new_content
        post.save()
    return HttpResponse(200)

def update_post(request, post_id):
    post = Post.objects.get(id = post_id)
    new_post = {
        "post_content": post.content,
        "post_date": post.date
    }
    print(new_post)

    return HttpResponse(json.dumps(new_post, indent=4, sort_keys=True, default=str), content_type='application/json')


def getPosts(request, page="", username=""):
    if (page == "/following"):
        following_ids = UserNumber.objects.values_list('following',flat= True).filter(user__username = request.user.username)
        all_posts = Post.objects.filter(creator_id__in = set(following_ids)).order_by('-date')
        return all_posts
    if (page == "/profile"):
        return  Post.objects.filter(creator__username = username).order_by('-date')
    else:
        return  Post.objects.exclude(creator__username = request.user.username).order_by('-date')
    
def createNewPost(request):
    user = request.user
    content = request.POST["content"]

    if len(content) <= 500:
        newPost = Post(creator=user, content=content)
        newPost.save()
        return "",""
    else:
        message = "The Post contains more than 500 characters."
        return content, message
        