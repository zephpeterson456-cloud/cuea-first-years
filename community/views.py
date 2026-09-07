from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post, Notification


def home(request):
    posts = Post.objects.filter(
        approved=True
    ).select_related("author")

    return render(
        request,
        "community/home.html",
        {
            "posts": posts,
        },
    )


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.approved = False
            post.save()

            return redirect("home")

    else:
        form = PostForm()

    return render(
        request,
        "community/create_post.html",
        {
            "form": form,
        },
    )


@login_required
def toggle_like(request, post_id):

    post = Post.objects.get(
        id=post_id,
        approved=True,
    )

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type="LIKE",
                post=post,
            )

    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def add_comment(request, post_id):

    if request.method != "POST":
        return redirect("home")

    post = Post.objects.get(
        id=post_id,
        approved=True,
    )

    content = request.POST.get(
        "content",
        "",
    ).strip()

    if content:
        from .models import Comment

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
        )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type="COMMENT",
                post=post,
                comment=comment,
            )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home",
        )
    )


@login_required
def delete_comment(request, comment_id):

    from .models import Comment

    comment = Comment.objects.get(
        id=comment_id,
    )

    if comment.author == request.user:
        comment.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home",
        )
    )


@login_required
def notifications(request):
    from .models import Notification

    items = Notification.objects.filter(
        recipient=request.user
    ).select_related(
        "sender",
        "post",
        "comment",
    )

    items.filter(is_read=False).update(is_read=True)

    return render(
        request,
        "community/notifications.html",
        {
            "notifications": items,
        },
    )


def search(request):
    from django.db.models import Q
    from django.contrib.auth.models import User

    query = request.GET.get("q", "").strip()
    post_type = request.GET.get("type", "").strip().upper()

    posts = Post.objects.filter(
        approved=True
    ).select_related("author")

    users = User.objects.none()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

        users = User.objects.filter(
            username__icontains=query
        ).order_by("username")

    if post_type in ["MEME", "MOTIVATION"]:
        posts = posts.filter(post_type=post_type)

    return render(
        request,
        "community/search.html",
        {
            "posts": posts,
            "users": users,
            "query": query,
            "post_type": post_type,
        },
    )


def trending(request):
    from django.db.models import Count

    posts = Post.objects.filter(
        approved=True
    ).select_related(
        "author"
    ).annotate(
        like_count=Count("likes", distinct=True),
        comment_count=Count("comments", distinct=True),
    ).order_by(
        "-like_count",
        "-comment_count",
        "-created_at",
    )

    return render(
        request,
        "community/trending.html",
        {
            "posts": posts,
        },
    )


@login_required
def edit_post(request, post_id):
    from django.shortcuts import get_object_or_404

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
    )

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            post = form.save(commit=False)

            # Edited posts go back for moderation.
            post.approved = False
            post.save()

            return redirect(
                "profile",
                username=request.user.username,
            )

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "community/edit_post.html",
        {
            "form": form,
            "post": post,
        },
    )


@login_required
def delete_post(request, post_id):
    from django.shortcuts import get_object_or_404

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
    )

    if request.method == "POST":
        post.delete()

    return redirect(
        "profile",
        username=request.user.username,
    )


@login_required
def edit_post(request, post_id):
    from django.shortcuts import get_object_or_404

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
    )

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            post = form.save(commit=False)

            # Edited posts go back for moderation.
            post.approved = False
            post.save()

            return redirect(
                "profile",
                username=request.user.username,
            )

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "community/edit_post.html",
        {
            "form": form,
            "post": post,
        },
    )


@login_required
def delete_post(request, post_id):
    from django.shortcuts import get_object_or_404

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user,
    )

    if request.method == "POST":
        post.delete()

    return redirect(
        "profile",
        username=request.user.username,
    )


@login_required
def report_post(request, post_id):
    from django.shortcuts import get_object_or_404
    from .forms import ReportForm

    post = get_object_or_404(
        Post,
        id=post_id,
        approved=True,
    )

    # Don't allow users to report their own posts.
    if post.author == request.user:
        return redirect("home")

    # Prevent duplicate unresolved reports.
    existing_report = post.reports.filter(
        reporter=request.user,
        resolved=False,
    ).first()

    if existing_report:
        return redirect("home")

    if request.method == "POST":
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.reporter = request.user
            report.save()

            return redirect("home")

    else:
        form = ReportForm()

    return render(
        request,
        "community/report_post.html",
        {
            "form": form,
            "post": post,
        },
    )
