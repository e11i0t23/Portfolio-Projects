import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Comment, Profile
from math import ceil

def index(request):
    return render(request, "project_4_network/index.html")


# API route for recieving posts, here a user_id and page are taken as an input to get the approapriate set of posts
def posts(request, page, user_id):   
    if user_id == None:
        p = Post.objects.all().order_by('-timestamp')
    elif user_id=='following':
        users = [profile.user for profile in Profile.objects.get(user=request.user).following.all()]
        p = Post.objects.all().filter(user__in=users).order_by('-timestamp')
    else:
        p = Post.objects.all().filter(user=User.objects.get(pk=user_id)).order_by('-timestamp')
    pages = ceil(p.count()/10)
    posts = [post.serialize() for post in p[(page*10):(page*10)+10]]
    for post in posts:
        post['liked'] = True if request.user.id in post['likes'] else False
        post['likes'] = len(post['likes'])
    return JsonResponse({"pages":pages, "posts":posts}, safe=False)
        

def editpost(request, id):
    data = json.loads(request.body)
    # Out Put request requires a post id and allows for liking and editing a post
    if request.method=='PUT' and id != None:
        p = Post.objects.get(pk=id)
        if 'post' in data:
            # Ensure the person trying to update a post is the original author
            if p.user == request.user: 
                p.body=data['post']
                p.save()
            else: return JsonResponse({"error":"You must be the origian author to update a post"}, status=400)
        elif 'liked' in data:
            # Handle Liking and unliking a Post
            if request.user in p.likes.all():
                p.likes.remove(request.user)
            else:
                p.likes.add(request.user)
            p.save()
        # Finally on succes of these operations we return the updated post
        post = p.serialize()
        post['liked'] = True if request.user.id in post['likes'] else False
        post['likes'] = len(post['likes'])
        return JsonResponse(post, status=200)
    # If no post ID is provided and POST was used then we create a new post 
    elif id == None and request.method=="POST":
        body=data['post']
        if body.strip() == "": return JsonResponse({"error":"Post Content Blank"}, status=400)
        p = Post(body=body, user=request.user)
        p.save()
        return JsonResponse({"message":"Successfully posted"}, status=200)
    else:
        return JsonResponse({"error":"invalid operation"}, status=400)
    

def user(request, id):
    checkForProfile(request.user)
    following=False
    # Ensure a user exists otherwise return an error stating the fact
    try:
        user = User.objects.get(pk=id)
        checkForProfile(user)
        UserProfile = Profile.objects.get(user=user)
        profile = Profile.objects.get(user=request.user)
    except User.DoesNotExist:
        return JsonResponse({"error":"User does not exist"}, status=400)
    
    # Handle put requests which are used to follow and unfollow users
    if request.method == "PUT":
        following = json.loads(request.body)['following']
        if following:
            profile.following.add(UserProfile)
        else:
            profile.following.remove(UserProfile)
        request.user.save()
    
    
    if request.user.is_authenticated:
        following = True if UserProfile in profile.following.all() else False

    return JsonResponse({
        "following": following,
        "followerCount": profile.followers.all().count(),
        "followingCount": profile.following.all().count(),
        "username": user.username
    }, safe=False)

def checkForProfile(user):
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        print("test")
        Profile(user=user).save()
        
