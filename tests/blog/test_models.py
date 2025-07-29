import pytest
from django.contrib.auth import get_user_model
from apps.blog.models import Category, Post, Tag, Comment

User = get_user_model()


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        category = Category.objects.create(
            name='Technology',
            description='Posts about technology'
        )
        
        assert category.name == 'Technology'
        assert category.slug == 'technology'
        assert category.description == 'Posts about technology'

    def test_category_str_representation(self):
        category = Category.objects.create(name='Technology')
        
        assert str(category) == 'Technology'

    def test_category_slug_auto_generation(self):
        category = Category.objects.create(name='Web Development')
        
        assert category.slug == 'web-development'


@pytest.mark.django_db
class TestTagModel:
    def test_create_tag(self):
        tag = Tag.objects.create(name='Python')
        
        assert tag.name == 'Python'
        assert tag.slug == 'python'

    def test_tag_str_representation(self):
        tag = Tag.objects.create(name='Django')
        
        assert str(tag) == 'Django'

    def test_tag_slug_auto_generation(self):
        tag = Tag.objects.create(name='Machine Learning')
        
        assert tag.slug == 'machine-learning'


@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self, user, category):
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=user,
            category=category
        )
        
        assert post.title == 'Test Post'
        assert post.slug == 'test-post'
        assert post.content == 'This is a test post content.'
        assert post.author == user
        assert post.category == category
        assert post.status == 'draft'
        assert post.views_count == 0

    def test_post_str_representation(self, user):
        post = Post.objects.create(
            title='My Test Post',
            content='Content',
            author=user
        )
        
        assert str(post) == 'My Test Post'

    def test_post_slug_auto_generation(self, user):
        post = Post.objects.create(
            title='My Amazing Blog Post',
            content='Content',
            author=user
        )
        
        assert post.slug == 'my-amazing-blog-post'

    def test_post_excerpt_auto_generation(self, user):
        long_content = 'a' * 600
        post = Post.objects.create(
            title='Long Post',
            content=long_content,
            author=user
        )
        
        assert len(post.excerpt) == 500
        assert post.excerpt.endswith('...')

    def test_increment_views(self, user):
        post = Post.objects.create(
            title='Test Post',
            content='Content',
            author=user
        )
        
        initial_views = post.views_count
        post.increment_views()
        
        assert post.views_count == initial_views + 1


@pytest.mark.django_db
class TestCommentModel:
    def test_create_comment(self, user, post):
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='This is a test comment.'
        )
        
        assert comment.post == post
        assert comment.author == user
        assert comment.content == 'This is a test comment.'
        assert comment.is_approved is True

    def test_comment_str_representation(self, user, post):
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Test comment'
        )
        
        expected = f'Comment by {user.username} on {post.title}'
        assert str(comment) == expected