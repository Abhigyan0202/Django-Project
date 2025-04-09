from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('addpost',views.addpost,name='addpost'),
    path('posts/<int:id>',views.posts,name="posts"),
    path('userprofile/<str:username>',views.userp,name="userp"),
    path('addcomment',views.add_comment,name="add_comment"),
    path('updateprofile',views.updateprofile,name="updateprofile"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="users/password_reset.html",email_template_name='users/email.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name='password_reset_complete' ),
    path('like/<int:id>/',views.like,name='like'),
    path('getFile/<int:id>',views.getFile,name='getFile'),
    path('search',views.search,name='search'),
    path('fetchPosts/<int:index>',views.fetchPosts,name='fetchPosts'),
    path('saveuser',views.saveUser,name="saveuser"),
    path('resetOTP/<str:email>',views.resetOTP,name="resetOTP"),
    path('events',views.events,name="events"),
    path('events/<int:id>',views.showevent,name='showevent'),
    path("registerUserForEvent/<int:id>",views.registerUserForEvent,name='regsiterUserForEvent'),
    path('createevent',views.createevent,name='createevent'),
    path('myposts',views.myPosts,name='myposts'),
    path('myevents',views.myEvents,name='myevents'),
    path('deletePost/<int:id>',views.deletePost,name='deletePost'),
    path('deleteEvent/<int:id>',views.deleteEvent,name='deleteEvent'),
    path('checkparticipants/<int:id>',views.checkparticipants,name='checkparticipants'),
    path('deleteUser/<str:username>',views.deleteUser,name='deleteUser'),
    path('emailParticipants/<int:eventid>',views.emailParticipants,name='emailParticipants')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)