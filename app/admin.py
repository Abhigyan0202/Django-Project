from django.contrib import admin
from .models import Post, Comment, UserProfile

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
