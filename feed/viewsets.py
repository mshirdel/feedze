from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from feed.models import Feed, FeedItem
from feed.serializers import FeedSerializer, FeedItemSerializer
from feed.tasks import import_feed_task


class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    model = Feed
    queryset = model.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False, url_path="import-feed")
    def import_feed(self, request, *args, **kwargs):
        url = request.data.get("url")
        import_feed_task.delay(url)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    model = FeedItem
    queryset = model.objects.all()
    serializer_class = FeedItemSerializer
    permission_classes = [IsAuthenticated]
