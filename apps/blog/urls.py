from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # Post URLs
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("posts/create/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/my/", views.my_posts_view, name="my-posts"),
    path("posts/featured/", views.featured_posts_view, name="featured-posts"),
    path("posts/popular/", views.popular_posts_view, name="popular-posts"),
    path("posts/recent/", views.recent_posts_view, name="recent-posts"),
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post-update"),
    path("posts/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    # Comment URLs
    path("posts/<slug:post_slug>/comments/", views.CommentCreateView.as_view(), name="comment-create"),
    # Category and Tag URLs
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("tags/", views.TagListView.as_view(), name="tag-list"),
    # Analytics URLs
    path("stats/", views.blog_stats_view, name="blog-stats"),
]
