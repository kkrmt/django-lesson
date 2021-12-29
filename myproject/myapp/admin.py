from django.contrib import admin
from .models import Post, Like, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'author', 'title', 'created_at')
    list_display_links = ('title', 'category')
    ordering = ('-created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')
    list_display_links = ('id',)
    ordering = ('-id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_en', 'created_at')
    list_display_links = ('name',)
    ordering = ('-created_at',)
