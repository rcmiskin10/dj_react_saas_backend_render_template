from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/landingpage/", include("landingpage.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/blog/", include("blog.urls")),
    path("api/landingpage/", include("landingpage.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        )
    ]
