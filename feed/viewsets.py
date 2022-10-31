from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from feed.feed_manager import FeedFetcher
from feed.models import Feed
from feed.serializers import FeedSerializer


class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    model = Feed
    queryset = model.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def fetch_feed(self, request, *args, **kwargs):
        url = request.data.get("url")
        FeedFetcher(url)
        return Response(status=status.HTTP_204_NO_CONTENT)
