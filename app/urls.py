from django.urls import path
from . import views
app_name = 'app'

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('addpost',views.addpost,name='addpost'),
    path('posts/<int:id>',views.posts,name="posts"),
    path('userp',views.userp,name="userp"),
    path('addcomment',views.add_comment,name="add_comment"),
    path('updateprofile',views.updateprofile,name="updateprofile")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)