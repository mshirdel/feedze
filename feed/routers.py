from rest_framework.routers import DefaultRouter

from feed.viewsets import FeedViewSet

router = DefaultRouter()

router.register("feeds", FeedViewSet, basename="feed-viewset")

urls = router.urls
