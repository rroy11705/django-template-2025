from typing import List, Optional

from django.db import models
from django.db.models import Count, F, Q, Sum
from django.utils import timezone

from .models import Category, Comment, Post, Tag


class BlogPostService:
    @staticmethod
    def get_published_posts():
        return (
            Post.objects.filter(status="published", published_at__lte=timezone.now())
            .select_related("author", "category")
            .prefetch_related("tags")
        )

    @staticmethod
    def get_featured_posts(limit: int = 5):
        return BlogPostService.get_published_posts().filter(is_featured=True)[:limit]

    @staticmethod
    def search_posts(query: str):
        return BlogPostService.get_published_posts().filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query)
        )

    @staticmethod
    def get_posts_by_category(category_slug: str):
        return BlogPostService.get_published_posts().filter(category__slug=category_slug)

    @staticmethod
    def get_posts_by_tag(tag_slug: str):
        return BlogPostService.get_published_posts().filter(tags__slug=tag_slug)

    @staticmethod
    def get_posts_by_author(author_id: int):
        return BlogPostService.get_published_posts().filter(author_id=author_id)

    @staticmethod
    def publish_post(post: Post):
        post.status = "published"
        post.published_at = timezone.now()
        post.save()
        return post

    @staticmethod
    def increment_post_views(post: Post):
        Post.objects.filter(id=post.id).update(views_count=F("views_count") + 1)


class BlogAnalyticsService:
    @staticmethod
    def get_popular_posts(limit: int = 10):
        return BlogPostService.get_published_posts().order_by("-views_count")[:limit]

    @staticmethod
    def get_recent_posts(limit: int = 10):
        return BlogPostService.get_published_posts().order_by("-published_at")[:limit]

    @staticmethod
    def get_blog_stats():
        published_posts = BlogPostService.get_published_posts()

        return {
            "total_posts": published_posts.count(),
            "total_categories": Category.objects.filter(posts__status="published").distinct().count(),
            "total_tags": Tag.objects.filter(posts__status="published").distinct().count(),
            "total_views": published_posts.aggregate(total=Sum("views_count"))["total"] or 0,
            "total_comments": Comment.objects.filter(post__status="published", is_approved=True).count(),
        }

    @staticmethod
    def get_category_stats():
        return (
            Category.objects.annotate(
                posts_count=Count("posts", filter=Q(posts__status="published")),
                total_views=Sum("posts__views_count", filter=Q(posts__status="published")),
            )
            .filter(posts_count__gt=0)
            .order_by("-posts_count")
        )


class BlogCommentService:
    @staticmethod
    def create_comment(post: Post, author, content: str):
        return Comment.objects.create(post=post, author=author, content=content)

    @staticmethod
    def approve_comment(comment: Comment):
        comment.is_approved = True
        comment.save()
        return comment

    @staticmethod
    def get_recent_comments(limit: int = 10):
        return (
            Comment.objects.filter(is_approved=True, post__status="published")
            .select_related("author", "post")
            .order_by("-created_at")[:limit]
        )


class BlogRecommendationService:
    @staticmethod
    def get_related_posts(post: Post, limit: int = 5):
        related_posts = BlogPostService.get_published_posts().exclude(id=post.id)

        # Priority 1: Same category
        if post.category:
            category_posts = related_posts.filter(category=post.category)[:limit]
            if category_posts.count() >= limit:
                return category_posts

        # Priority 2: Same tags
        if post.tags.exists():
            tag_posts = related_posts.filter(tags__in=post.tags.all()).distinct()[:limit]
            if tag_posts.count() >= limit:
                return tag_posts

        # Priority 3: Same author
        author_posts = related_posts.filter(author=post.author)[:limit]
        if author_posts.count() >= limit:
            return author_posts

        # Fallback: Recent posts
        return BlogAnalyticsService.get_recent_posts(limit)
