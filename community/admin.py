from django.contrib import admin

from .models import Comment, Post, Profile
try:
    from .push import send_push_notification
except ModuleNotFoundError:
    def send_push_notification(*args, **kwargs):
        return None



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bio",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "bio",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post_type",
        "title",
        "author",
        "approved",
        "created_at",
    )

    list_filter = (
        "post_type",
        "approved",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )

    list_editable = (
        "approved",
    )

    def save_model(self, request, obj, form, change):
        was_approved = False

        if change:
            was_approved = (
                Post.objects
                .filter(pk=obj.pk)
                .values_list("approved", flat=True)
                .first()
            )

        super().save_model(request, obj, form, change)

        if change and not was_approved and obj.approved:
            send_push_notification(
                obj.author,
                "📢 Your Post Was Approved",
                f"Your post \"{obj.title}\" is now live.",
                f"/post/{obj.id}/",
            )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "author",
        "content",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "content",
        "author__username",
    )

from .models import Report

admin.site.register(Report)
