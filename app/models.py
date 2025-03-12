from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    heading = models.CharField(max_length=128)
    content = models.TextField(max_length=2048)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    likes = models.ManyToManyField(User,through='Like',related_name='liked_posts')
    def __str__(self):
        if len(self.content) <= 200:
            return self.content
        return f"{self.content[:200]}...."
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField(max_length=512)
    
    def __str__(self):
        return f'{self.post} {self.content[:20]}'
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="userprofile",unique=True)
    description = models.TextField(max_length=512)
    pfp = models.ImageField(upload_to="profile_pics/",default='profile_pics/default.jpg')
    
    def __str__(self):
        return f"{self.user.username} {self.description[:20]}"
    
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)