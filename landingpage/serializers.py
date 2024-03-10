from rest_framework import serializers

from .models import Feature, HowItWorksStep, LandingPage, SocialMediaLink


class HowItWorksStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorksStep
        fields = ["step", "step_description", "step_mui_icon_name", "order"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            "feature_title",
            "feature_description",
            "feature_mui_icon_name",
            "order",
        ]


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = [
            "social_media_type",
            "social_media_link",
            "social_media_mui_icon_name",
            "order",
        ]


class LandingPageSerializer(serializers.ModelSerializer):
    how_it_works_steps = HowItWorksStepSerializer(many=True)
    features = FeatureSerializer(many=True)
    social_media_links = SocialMediaLinkSerializer(many=True)

    class Meta:
        model = LandingPage
        fields = "__all__"
