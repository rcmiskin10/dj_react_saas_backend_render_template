from django.db import models


class Feature(models.Model):
    feature_title = models.CharField(max_length=256)
    feature_description = models.CharField(max_length=256)
    feature_mui_icon_name = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.feature_title


class HowItWorksStep(models.Model):
    step = models.CharField(max_length=256)
    step_description = models.CharField(max_length=256)
    step_mui_icon_name = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.step


class SocialMediaLink(models.Model):
    social_media_type = models.CharField(max_length=256)
    social_media_mui_icon_name = models.CharField(max_length=256)
    social_media_link = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.social_media_type


class LandingPage(models.Model):
    primary_hero_title = models.CharField(max_length=256)
    primary_hero_subtitle = models.CharField(max_length=256)
    primary_hero_image = models.ImageField(upload_to="landingpage_images/")
    features = models.ManyToManyField(to=Feature, related_name="landingpage_features")
    how_it_works_steps = models.ManyToManyField(
        to=HowItWorksStep, related_name="landingpage_how_it_works_steps"
    )
    secondary_hero_title = models.CharField(max_length=256)
    secondary_hero_subtitle = models.CharField(max_length=256)
    secondary_hero_image = models.ImageField(upload_to="landingpage_images/")
    social_media_links = models.ManyToManyField(
        to=SocialMediaLink, related_name="landingpage_social_media_links"
    )

    def __str__(self):
        return self.primary_hero_title


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
