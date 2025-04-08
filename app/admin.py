from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
admin.site.register(Like)
admin.site.register(Otp)
admin.site.register(Event, EventAdmin)
admin.site.register(EventUser)
