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

    @action(methods=["post"], detail=True)
    def follow(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.followed_by_user(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @follow.mapping.delete
    def unfollow(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.unfollow_by_user(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="following")
    def user_following(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(followers=request.user)
        return self.list(request, *args, **kwargs)


class FeedItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    model = FeedItem
    queryset = model.objects.all()
    serializer_class = FeedItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            self.queryset = self.queryset.filter(
                feed__users_follow__user_id=self.request.user.id
            )
        return super().get_queryset()

    @action(methods=["post"], detail=True)
    def favorite(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.favorite_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove_favorite_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="my-favorites")
    def my_favorites(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            users_favorite__user_id=request.user.id
        ).prefetch_related("users_favorite")
        return self.list(request, *args, **kwargs)
