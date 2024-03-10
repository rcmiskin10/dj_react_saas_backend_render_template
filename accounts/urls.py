from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import DeleteProfile, LogoutView, RegisterView, RetrieveProfileInfo

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="accounts_register"),
    path("logout/", LogoutView.as_view(), name="accounts_logout"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path(
        "retrieve-profile-info/",
        RetrieveProfileInfo.as_view(),
        name="accounts_retrieve_profile_info",
    ),
    path(
        "delete-profile/",
        DeleteProfile.as_view(),
        name="accounts_delete_profile",
    ),
]
