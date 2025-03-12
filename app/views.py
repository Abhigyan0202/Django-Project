from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings


# Create your views here.
def index(request):
    return render(request,'app/index.html')

#Need to implement protections against attacks
#Need to implement forgot password feature
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            usernameWarning = User.objects.filter(username=username).exists()
            emailWarning = User.objects.filter(email=email).exists()
            if usernameWarning or emailWarning:
                return render(request,'app/signup.html', {
                    "username": username,
                    "email": email,
                    "usernameWarning": usernameWarning,
                    "emailWarning": emailWarning,
                    'password': password
                })
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username,email,password)
            userp = UserProfile.objects.create(user=user,description="")
            user.save()
            userp.save()
            return redirect('login_user')
    return render(request,'app/signup.html',{
        "usernameWarning": False,
        "emailWarning": False
    })

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                return render(request, 'app/login.html', {
                    "form": forms.LoginForm(),
                    "alert": True
                })
        
    return render(request, 'app/login.html', {
        "form": forms.LoginForm()
    })
    
def home(request):
    posts = Post.objects.prefetch_related('likes').all()
    context = {
        "posts": posts,
        "user": request.user,
        "flag": request.user.is_authenticated
    }
    return render(request,'app/home.html', context)



@login_required    
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def addpost(request):
    if request.method == 'POST':
        #Need to implement a feature that if length of post is too long then alert the user
        form1 = forms.PostForm(request.POST)
        if form1.is_valid():
            post = form1.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    return render(request, "app/addpost.html", {
        "form": forms.PostForm()
    })


def posts(request,id):
    post = Post.objects.get(pk=id)
    comments = Comment.objects.filter(post=post)
    return render(request,'app/posts.html',{
        "post": post,
        "comments": comments,
        "commentForm": forms.CommentForm()
    })

@login_required    
def userp(request):
    userprofile = UserProfile.objects.get(user=request.user)
    return render(request, "app/userprofile.html", {
        "user": request.user,
        "form": forms.UserProfileForm()
    })
    
def add_comment(request):
    if request.method=="POST":
        form1 = forms.CommentForm(request.POST)
        if form1.is_valid():
            comment1 = form1.save(commit=False)
            comment1.user = request.user
            id = request.POST['id']
            comment1.post = Post.objects.get(pk=id)
            comment1.save()
            return JsonResponse({
                "username": comment1.user.username,
                "content": comment1.content,
                "pfp": comment1.user.userprofile.pfp.url
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)
            
@login_required            
def updateprofile(request):
    obj = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = forms.UserProfileForm(request.POST,request.FILES,instance=obj)
        #Need to delete the previous profile picture from the database
        if form1.is_valid():
            form1.save()
            return redirect("userp")
    
        
def forgot(request):
    if request.method == 'POST':
        pass
    return render(request, "app/forgot.html")


def like(request,id):
    user = request.user
    post = Post.objects.get(pk=id)
    l = len(Like.objects.filter(post=post))
    if Like.objects.filter(user=user,post=post).exists():
        Like.objects.filter(user=user,post=post).delete()
        return JsonResponse({
            "likes": f"{l-1}",
            "flag": "remove"
        })
    Like.objects.create(user=user,post=post)
    return JsonResponse({
        "likes": f"{l+1}",
        "flag": "add"
    })
            


        
    
