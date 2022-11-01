from rest_framework.routers import DefaultRouter

from feed.viewsets import FeedViewSet, FeedItemViewSet

router = DefaultRouter()

router.register("feeds", FeedViewSet, basename="feed-viewset")
router.register("stories", FeedItemViewSet, basename="stories-viewset")

urls = router.urls
