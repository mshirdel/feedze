from django.db import models
from django.db.models import F


class UserFollowFeed(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="followed_feeds"
    )
    feed = models.ForeignKey(
        "feed.Feed", on_delete=models.CASCADE, related_name="users_follow"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "feed")


class Feed(models.Model):
    feed_url = models.URLField(
        unique=True, db_index=True, help_text="Url for fetching feeds"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    published = models.DateTimeField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    update_interval = models.IntegerField(
        default=60, help_text="Update interval time in minutes"
    )
    image = models.URLField(null=True, blank=True)
    followers = models.ManyToManyField(
        "user.User", related_name="feeds", through="feed.UserFollowFeed"
    )

    def __str__(self):
        return f"{self.title}"

    def followed_by_user(self, user_id: int):
        self.followers.add(user_id)

    def unfollow_by_user(self, user_id: int):
        self.followers.remove(user_id)


class FeedItemQuerySet(models.QuerySet):
    def unread_items_by_user_id(self, user_id):
        return self.exclude(users_read__user_id=user_id).filter(
            feed__users_follow__user_id=user_id,
            feed__users_follow__created_at__lt=F("created_at"),
        )

    def favorites_items_by_user_id(self, user_id):
        return self.exclude(users_favorite__user_id=user_id).filter(
            feed__users_follow__user_id=user_id,
            feed__users_follow__created_at__lt=F("created_at"),
        )

    def bookmarked_items_by_user_id(self, user_id):
        return self.exclude(users_bookmark__user_id=user_id).filter(
            feed__users_follow__user_id=user_id,
            feed__users_follow__created_at__lt=F("created_at"),
        )


class FeedItem(models.Model):
    feed = models.ForeignKey(
        "feed.Feed", on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField(unique=True, db_index=True)
    author = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    read_by = models.ManyToManyField(
        "user.User", related_name="reads", through="feed.UserRead"
    )
    favorite_by = models.ManyToManyField(
        "user.User", related_name="favorites", through="feed.UserFavorite"
    )

    bookmarked_by = models.ManyToManyField(
        "user.User", related_name="bookmarks", through="feed.UserBookmark"
    )

    objects = FeedItemQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} - {self.feed.title}"

    def read_by_user_id(self, user_id: int) -> None:
        self.read_by.add(user_id)

    def bookmark_by_user_id(self, user_id: int) -> None:
        self.bookmarked_by.add(user_id)

    def remove_bookmark_by_user_id(self, user_id: int) -> None:
        self.bookmarked_by.remove(user_id)

    def favorite_by_user_id(self, user_id: int) -> None:
        self.favorite_by.add(user_id)

    def remove_favorite_by_user_id(self, user_id: int) -> None:
        self.favorite_by.remove(user_id)


class UserRead(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="read_items"
    )
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="users_read"
    )

    class Meta:
        unique_together = ("user", "feed_item")


class UserFavorite(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="favorites_items"
    )
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="users_favorite"
    )

    class Meta:
        unique_together = ("user", "feed_item")


class UserBookmark(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="bookmarked_items"
    )
    feed_item = models.ForeignKey(
        FeedItem, on_delete=models.CASCADE, related_name="users_bookmark"
    )

    class Meta:
        unique_together = ("user", "feed_item")
