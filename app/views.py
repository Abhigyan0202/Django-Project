import random
import string
from django.http import FileResponse, HttpResponse,  JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings
import pathlib
from django.db.models import Count


# Create your views here.
def index(request):
    return render(request,'app/index.html')

#Need to implement protections against attacks
#Need to implement forgot password feature
def generateUsername(email):
    t = ""
    for i in range(5):
        if email[i]=='@':
            break
        t += email[i]
    r = ''.join(random.choices(string.digits+string.ascii_letters,k=10-len(t)))
    t += r
    return t

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            #generate unique username
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = ""
            while True:
                username = generateUsername(email)
                if User.objects.filter(username=username).exists():
                    continue
                else :
                    break
            emailWarning = User.objects.filter(email=email).exists()
            if emailWarning:
                return render(request,'app/signup.html', {
                    "email": email,
                    "emailWarning": emailWarning,
                    'password': password
                })
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            if not User.objects.filter(email=email).exists():
                return render(request, 'app/login.html', {
                    "email": email,
                    "noaccount": True
                })
            user = User.objects.get(email=email)
            user = authenticate(request,username=user.username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                return render(request, 'app/login.html', {
                    "email": email,
                    "alert": True
                })
        
    return render(request, 'app/login.html')
    
def home(request):
    posts = Post.objects.prefetch_related('likes').all()
    top_posts = posts.annotate(number_of_likes=Count('likes'))
    top_posts = top_posts.order_by("-number_of_likes")[:5]
    context = {
        "posts": posts,
        "user": request.user,
        "flag": request.user.is_authenticated,
        "top_posts": top_posts
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
        form1 = forms.PostForm(request.POST,request.FILES)
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
        "flag": post.file
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
        oldusername = request.user.username
        user = User.objects.get(username=oldusername)
        newusername = request.POST['username']
        user.username = newusername
        user.save()
        if form1.data.get('pfp') is None:
            old_pfp = request.user.userprofile.pfp.url
            if old_pfp!='/media/profile_pics/default.jpg':
                p = f"D:\All study\Semester 6\Software Engineering\django prac\project5{old_pfp}"
                pathlib.Path(p).unlink()
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

def getFile(request,id):    
    post = Post.objects.get(pk=id)
    if post.file:
        return FileResponse(post.file,as_attachment=True)
    return None


def search(request):
    if request.method == 'GET':
        keyword = request.GET['s1']
        posts = Post.objects.filter(heading__icontains=keyword)
        return render(request,"app/searchresults.html",{
            "results": posts
        })


def fetchPosts(request,index):
    length = len(Post.objects.all())
    posts = Post.objects.all()[index:min(index+5,length)]
    return_response = {"size": len(posts)}
    for i in range(len(posts)):
        post = posts[i]
        temp = {}
        temp["id"] = post.id
        temp["heading"] = post.heading
        temp["content"] = post.__str__()
        temp["user"] = post.user.username
        temp["is_authenticated"] = request.user.is_authenticated
        temp["has_liked"] = request.user in post.likes.all() 
        temp["pfp_url"] = post.user.userprofile.pfp.url
        temp["like_count"] = post.likes.count()
        return_response[f"{i}"] = temp
    return JsonResponse(return_response)



        
    
