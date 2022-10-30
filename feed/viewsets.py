from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from feed.models import Feed
from feed.serializers import FeedSerializer


class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    model = Feed
    queryset = model.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]
