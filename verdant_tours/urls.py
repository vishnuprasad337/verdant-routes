from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


handler404 = "verdant_tours_app.views.custom_404"

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("verdant_tours_app.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )