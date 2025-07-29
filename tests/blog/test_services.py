import pytest
from datetime import datetime
from django.utils import timezone
from apps.blog.models import Post, Category, Tag, Comment
from apps.blog.services import (
    BlogPostService, 
    BlogAnalyticsService, 
    BlogCommentService,
    BlogRecommendationService
)


@pytest.mark.django_db
class TestBlogPostService:
    def test_get_published_posts(self, post):
        posts = BlogPostService.get_published_posts()
        
        assert posts.count() == 1
        assert post in posts

    def test_get_published_posts_excludes_draft(self, user, category):
        draft_post = Post.objects.create(
            title='Draft Post',
            content='Draft content',
            author=user,
            category=category,
            status='draft'
        )
        
        posts = BlogPostService.get_published_posts()
        
        assert draft_post not in posts

    def test_get_featured_posts(self, user, category):
        from django.utils import timezone
        featured_post = Post.objects.create(
            title='Featured Post',
            content='Featured content',
            author=user,
            category=category,
            status='published',
            is_featured=True,
            published_at=timezone.now()
        )
        
        posts = BlogPostService.get_featured_posts()
        
        assert featured_post in posts

    def test_search_posts(self, post):
        posts = BlogPostService.search_posts('Test')
        
        assert post in posts

    def test_get_posts_by_category(self, post, category):
        posts = BlogPostService.get_posts_by_category(category.slug)
        
        assert post in posts

    def test_get_posts_by_tag(self, post, tag):
        post.tags.add(tag)
        
        posts = BlogPostService.get_posts_by_tag(tag.slug)
        
        assert post in posts

    def test_get_posts_by_author(self, post, user):
        posts = BlogPostService.get_posts_by_author(user.id)
        
        assert post in posts

    def test_publish_post(self, user, category):
        post = Post.objects.create(
            title='Draft Post',
            content='Content',
            author=user,
            category=category,
            status='draft'
        )
        
        published_post = BlogPostService.publish_post(post)
        
        assert published_post.status == 'published'
        assert published_post.published_at is not None


@pytest.mark.django_db
class TestBlogAnalyticsService:
    def test_get_popular_posts(self, user, category):
        from django.utils import timezone
        post1 = Post.objects.create(
            title='Popular Post',
            content='Content',
            author=user,
            category=category,
            status='published',
            views_count=100,
            published_at=timezone.now()
        )
        post2 = Post.objects.create(
            title='Less Popular Post',
            content='Content',
            author=user,
            category=category,
            status='published',
            views_count=50,
            published_at=timezone.now()
        )
        
        popular_posts = BlogAnalyticsService.get_popular_posts()
        
        assert list(popular_posts) == [post1, post2]

    def test_get_recent_posts(self, post):
        recent_posts = BlogAnalyticsService.get_recent_posts()
        
        assert post in recent_posts

    def test_get_blog_stats(self, post, category):
        stats = BlogAnalyticsService.get_blog_stats()
        
        assert stats['total_posts'] == 1
        assert stats['total_categories'] == 1
        assert stats['total_views'] == 0


@pytest.mark.django_db
class TestBlogCommentService:
    def test_create_comment(self, post, user):
        comment = BlogCommentService.create_comment(
            post=post,
            author=user,
            content='Test comment'
        )
        
        assert comment.post == post
        assert comment.author == user
        assert comment.content == 'Test comment'

    def test_approve_comment(self, post, user):
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Test comment',
            is_approved=False
        )
        
        approved_comment = BlogCommentService.approve_comment(comment)
        
        assert approved_comment.is_approved is True

    def test_get_recent_comments(self, post, user):
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Test comment'
        )
        
        recent_comments = BlogCommentService.get_recent_comments()
        
        assert comment in recent_comments


@pytest.mark.django_db
class TestBlogRecommendationService:
    def test_get_related_posts_same_category(self, user, category):
        from django.utils import timezone
        post1 = Post.objects.create(
            title='Post 1',
            content='Content 1',
            author=user,
            category=category,
            status='published',
            published_at=timezone.now()
        )
        post2 = Post.objects.create(
            title='Post 2',
            content='Content 2',
            author=user,
            category=category,
            status='published',
            published_at=timezone.now()
        )
        
        related_posts = BlogRecommendationService.get_related_posts(post1)
        
        assert post2 in related_posts

    def test_get_related_posts_same_tags(self, user, category, tag):
        from django.utils import timezone
        post1 = Post.objects.create(
            title='Post 1',
            content='Content 1',
            author=user,
            status='published',
            published_at=timezone.now()
        )
        post2 = Post.objects.create(
            title='Post 2',
            content='Content 2',
            author=user,
            status='published',
            published_at=timezone.now()
        )
        
        post1.tags.add(tag)
        post2.tags.add(tag)
        
        related_posts = BlogRecommendationService.get_related_posts(post1)
        
        assert post2 in related_posts