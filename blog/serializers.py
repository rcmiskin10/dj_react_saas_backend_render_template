from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    html_content_body = serializers.SerializerMethodField()
    created_on = serializers.DateTimeField(read_only=True, format="%b. %-d %Y")

    class Meta:
        model = Post
        fields = ["id", "title", "html_content_body", "created_on", "cover"]

    def get_html_content_body(self, instance):
        return str(instance.body.html)
