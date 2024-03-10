from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("id", "title", "body", "created_on", "cover")


admin.site.register(Post, PostAdmin)
