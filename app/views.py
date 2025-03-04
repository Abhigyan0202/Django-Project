from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings
from django.template import Template, Context
# Create your views here.
def index(request):
    return render(request,'app/index.html')

#Need to implement a better way to authenticate user, take care of privacy, attacks
#Need to implement forgot password feature
def signup(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                return render(request,'app/signup.html', {
                    "form": forms.SignUpForm(),
                    "usernameWarning": True
                })
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                return render(request,'app/signup.html', {
                    "form": forms.SignUpForm(),
                    "emailWarning": True
                })
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username,email,password)
            userp = UserProfile.objects.create(user=user,description="")
            user.save()
            userp.save()
            return redirect('app:login_user')
    return render(request,'app/signup.html',{
        "form": forms.SignUpForm()
    })

def login_user(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('app:home'))
            else :
                return render(request, 'app/login.html', {
                    "form": forms.LoginForm(),
                    "alert": True
                })
        
    return render(request, 'app/login.html', {
        "form": forms.LoginForm()
    })
    
def home(request):
    context = {
        "posts": Post.objects.all(),
        "user": request.user
    }
    return render(request,'app/home.html', context)



@login_required    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:home'))

@login_required
def addpost(request):
    if request.method == 'POST':
        #Need to implement a feature that if length of post is too long then alert the user
        form1 = forms.PostForm(request.POST)
        if form1.is_valid():
            post = form1.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('app:home'))
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
                "content": comment1.content
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
            return redirect("app:userp")
    
        
            


        
    
