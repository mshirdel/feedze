from rest_framework import serializers

from feed.models import Feed, FeedItem


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = (
            "id",
            "title",
            "description",
            "link",
            "feed_url",
            "published",
        )
        read_only_fields = fields


class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = (
            "id",
            "feed",
            "title",
            "description",
            "link",
            "author",
            "published_at",
            "created_at",
        )
        read_only_fields = fields
