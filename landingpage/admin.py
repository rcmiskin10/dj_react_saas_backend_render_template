from django.contrib import admin

from .models import (
    Feature,
    HowItWorksStep,
    LandingPage,
    NewsletterSignup,
    SocialMediaLink,
)


class LandingPageAdmin(admin.ModelAdmin):
    model = LandingPage
    list_display = (
        "primary_hero_title",
        "primary_hero_subtitle",
        "primary_hero_image",
        "secondary_hero_title",
        "secondary_hero_subtitle",
        "secondary_hero_image",
    )


admin.site.register(LandingPage, LandingPageAdmin)


class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    list_display = (
        "feature_title",
        "feature_description",
        "feature_mui_icon_name",
        "order",
    )


admin.site.register(Feature, FeatureAdmin)


class HowItWorksStepAdmin(admin.ModelAdmin):
    model = HowItWorksStep
    list_display = (
        "step",
        "step_description",
        "step_mui_icon_name",
        "order",
    )


admin.site.register(HowItWorksStep, HowItWorksStepAdmin)


class SocialMediaLinkAdmin(admin.ModelAdmin):
    model = SocialMediaLink
    list_display = (
        "social_media_type",
        "social_media_mui_icon_name",
        "social_media_link",
        "order",
    )


admin.site.register(SocialMediaLink, SocialMediaLinkAdmin)


class NewsletterSignupAdmin(admin.ModelAdmin):
    model = NewsletterSignup
    list_display = ("id", "email")


admin.site.register(NewsletterSignup, NewsletterSignupAdmin)
