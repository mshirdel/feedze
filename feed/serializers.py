from rest_framework import serializers

from feed.models import Feed


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
