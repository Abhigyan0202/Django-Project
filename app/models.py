import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField
# Create your models here.
class Post(models.Model):
    heading = models.CharField(max_length=128)
    content = models.TextField(max_length=2048)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    likes = models.ManyToManyField(User,through='Like',related_name='liked_posts')
    created = models.DateTimeField(auto_now=True)
    file = models.FileField(null=True,blank=True,upload_to='file_uploads/')
    def __str__(self):
        if len(self.content) <= 200:
            return self.content
        return f"{self.content[:200]}...."
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField(max_length=512)
    created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.post} {self.content[:20]}'
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="userprofile",unique=True)
    description = models.TextField(max_length=512,null=True)
    pfp = models.ImageField(upload_to="profile_pics/",default='profile_pics/default.jpg')
    education = models.TextField(max_length=256,default="")
    achievements = models.TextField(max_length=256,default="")
    
    def __str__(self):
        return f"{self.user.username} {self.description[:20]}"
    
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Otp(models.Model):
    email = models.TextField()
    otp = models.TextField()

class Event(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="events")
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(max_length=512)
    pfp = models.ImageField(upload_to="event_pics/",default='event_pics/default.jpg')
    users = models.ManyToManyField(User,through='EventUser',related_name='registered_users')
    
    def __str__(self):
        return f"{self.title} {self.start_time}"
    
class EventUser(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    