from django.urls import path

from . import auth_views
from . import profile_views
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("trending/", views.trending, name="trending"),

    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),

    path(
        "notifications/",
        views.notifications,
        name="notifications",
    ),

    path(
        "profile/edit/",
        profile_views.edit_profile,
        name="edit_profile",
    ),

    path(
        "profile/<str:username>/",
        profile_views.profile,
        name="profile",
    ),
    path("profile/<str:username>/follow/", profile_views.toggle_follow, name="toggle_follow"),
    path("profile/<str:username>/following/", profile_views.following, name="following"),
    path("profile/<str:username>/followers/", profile_views.followers, name="followers"),

    path("register/", auth_views.register, name="register"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
]


# Report a post
urlpatterns.append(
    path(
        "post/<int:post_id>/report/",
        views.report_post,
        name="report_post",
    )
)


# Report a post
urlpatterns.append(
    path(
        "post/<int:post_id>/report/",
        views.report_post,
        name="report_post",
    )
)
