from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'content', 'image']
    list_filter = ['title']
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}
