from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm
from .models import Profile


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    posts = user.posts.filter(approved=True)

    likes_received = sum(
        post.likes.count()
        for post in posts
    )

    return render(
        request,
        "community/profile.html",
        {
            "profile_user": user,
            "posts": posts,
            "likes_received": likes_received,
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
        {"form": form},
    )


@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        if request.user.profile.following.filter(
            id=user_to_follow.id
        ).exists():
            request.user.profile.following.remove(
                user_to_follow
            )
        else:
            request.user.profile.following.add(
                user_to_follow
            )

    return redirect(
        "profile",
        username=username,
    )


@login_required
def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(
        request,
        "community/followers.html",
        {
            "profile_user": user,
            "followers": user.profile.followers.all(),
        },
    )


@login_required
def following(request, username):
    user = get_object_or_404(User, username=username)

    return render(
        request,
        "community/following.html",
        {
            "profile_user": user,
            "following": user.profile.following.all(),
        },
    )
