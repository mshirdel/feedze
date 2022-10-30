from django.contrib import admin
from django.urls import path, include

from feed.routers import urls as feed_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("user.urls")),
    path("api/v1/", include(feed_url)),
]
