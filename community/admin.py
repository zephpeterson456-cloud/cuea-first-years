from django.contrib import admin

from .models import Comment, Post, Profile


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
