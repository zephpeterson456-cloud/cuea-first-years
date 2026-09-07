from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    posts = user.posts.filter(
        approved=True
    )

    likes_received = sum(
        post.likes.count()
        for post in posts
    )

    followers_count = user.followers.count()
    following_count = user.following.count()

    is_following = False

    if request.user != user:
        is_following = user.followers.filter(
            follower=request.user
        ).exists()

    return render(
        request,
        "community/profile.html",
        {
            "profile_user": user,
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
    from .models import Follow

    target_user = get_object_or_404(
        User,
        username=username,
    )

    if target_user == request.user:
        return redirect(
            "profile",
            username=username,
        )

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user,
    ).first()

    if follow:
        follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user,
        )

    return redirect(
        "profile",
        username=username,
    )


@login_required
def followers(request, username):
    from .models import Follow

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    follower_users = User.objects.filter(
        following__following=profile_user
    ).select_related(
        "profile"
    )

    return render(
        request,
        "community/followers.html",
        {
            "profile_user": profile_user,
            "users": follower_users,
        },
    )


@login_required
def following(request, username):
    from .models import Follow

    profile_user = get_object_or_404(
        User,
        username=username,
    )

    following_users = User.objects.filter(
        followers__follower=profile_user
    ).select_related(
        "profile"
    )

    return render(
        request,
        "community/following.html",
        {
            "profile_user": profile_user,
            "users": following_users,
        },
    )
