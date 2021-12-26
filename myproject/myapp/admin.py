from django.contrib import admin
from .models import Post, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'title', 'created_at')
  list_display_links = ('title',)
  ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ('id', 'post', 'user')
  list_display_links = ('id',)
  ordering = ('-id',)
