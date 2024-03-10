import blog.views as views
from django.urls import path

urlpatterns = [
    path("retrieve-posts/", views.RetrievePosts.as_view()),
    path("retrieve-post/", views.RetrievePost.as_view()),
]
