import landingpage.views as views
from django.urls import path

urlpatterns = [
    path(
        "get-landingpage-data/",
        views.GetLandingPageData.as_view(),
        name="api_landingpage_get",
    ),
    path(
        "newsletter-signup/",
        views.CreateNewsletterSignup.as_view(),
        name="api_newsletter_signup",
    ),
]
