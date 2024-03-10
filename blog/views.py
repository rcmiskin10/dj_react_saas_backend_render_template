import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RetrievePosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            posts = Post.objects.all()
            posts_serializer = PostSerializer(posts, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "posts": posts_serializer.data,
                    "success": True,
                },
            )
        except Exception as e:
            logger.error("Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str("Error occurred while retrieving posts."),
                    "success": False,
                },
            )


class RetrievePost(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            data = request.query_params
            post_id = data["post_id"]
            post = Post.objects.get(id=post_id)
            post_serializer = PostSerializer(post, many=False)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "post": post_serializer.data,
                    "success": True,
                },
            )
        except Exception as e:
            logger.error("Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str("Unknown issue occured retrieving post."),
                    "success": False,
                },
            )
