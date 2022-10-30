from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from feed.routers import urls as feed_url

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="FeedzE API",
        default_version="1.0.0",
        description="API documentation of Feed",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("user.urls")),
    path("api/v1/", include(feed_url)),
    path(
        "docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-schema"
    ),
]
