from django import forms 
from .models import *

class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login__input'
    }))
    
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['heading','content','file']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description', 'pfp']
    
