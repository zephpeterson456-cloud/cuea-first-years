from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    bio = models.TextField(
        max_length=300,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.user.username


class Post(models.Model):
    POST_TYPES = [
        ("MEME", "Meme"),
        ("MOTIVATION", "Motivation"),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES,
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True,
    )

    approved = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.get_post_type_display()} - "
            f"{self.title or self.content[:40]}"
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField(
        max_length=500,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.author.username}: "
            f"{self.content[:40]}"
        )


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("LIKE", "Like"),
        ("COMMENT", "Comment"),
        ("FOLLOW", "Follow"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notifications",
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Report(models.Model):
    REPORT_REASONS = [
        ("SPAM", "Spam"),
        ("HARASSMENT", "Harassment or bullying"),
        ("INAPPROPRIATE", "Inappropriate content"),
        ("MISINFORMATION", "Misinformation"),
        ("OTHER", "Other"),
    ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reports",
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_made",
    )

    reason = models.CharField(
        max_length=30,
        choices=REPORT_REASONS,
    )

    details = models.TextField(
        max_length=500,
        blank=True,
    )

    resolved = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.reporter.username} reported "
            f"Post #{self.post.id}"
        )

class PushSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="push_subscriptions",
    )
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Push subscription for {self.user.username}"
