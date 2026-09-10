from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile, Follow


@login_required
def profile(request, username):
    profile_user = get_object_or_404(
        User,
        username=username,
    )

    posts = profile_user.posts.filter(
        approved=True
    )

    likes_received = sum(
        post.likes.count()
        for post in posts
    )

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user,
    ).exists()

    return render(
        request,
        "community/profile.html",
        {
            "profile_user": profile_user,
            "posts": posts,
            "likes_received": likes_received,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        },
    )


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "profile",
                username=request.user.username,
            )

    else:
        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "community/edit_profile.html",
        {
            "form": form,
        },
    )


@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(
        User,
        username=username,
    )

    # Users cannot follow themselves.
    if request.user != user_to_follow:

        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow,
        ).first()

        if follow:
            follow.delete()
        else:
            Follow.objects.create(
                follower=request.user,
                following=user_to_follow,
            )

            from .models import Notification
            from .push import send_push_notification

            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type="FOLLOW",
            )

            send_push_notification(
                user_to_follow,
                "👥 New Follower",
                f"{request.user.username} started following you.",
                f"/profile/{request.user.username}/",
            )

    return redirect(
        "profile",
        username=username,
    )


@login_required
def followers(request, username):
    profile_user = get_object_or_404(
        User,
        username=username,
    )

    follow_records = Follow.objects.filter(
        following=profile_user
    ).select_related(
        "follower"
    )

    followers = [
        follow.follower
        for follow in follow_records
    ]

    return render(
        request,
        "community/followers.html",
        {
            "profile_user": profile_user,
            "followers": followers,
        },
    )


@login_required
def following(request, username):
    profile_user = get_object_or_404(
        User,
        username=username,
    )

    follow_records = Follow.objects.filter(
        follower=profile_user
    ).select_related(
        "following"
    )

    following = [
        follow.following
        for follow in follow_records
    ]

    return render(
        request,
        "community/following.html",
        {
            "profile_user": profile_user,
            "following": following,
        },
    )
