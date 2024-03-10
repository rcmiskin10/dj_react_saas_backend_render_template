from django.db import models
from django_quill.fields import QuillField


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = QuillField()
    created_on = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="blog_post_images/")

    def __str__(self):
        return self.title
