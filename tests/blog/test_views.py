import pytest
from django.urls import reverse
from rest_framework import status
from apps.blog.models import Post, Category


@pytest.mark.django_db
class TestPostListView:
    def test_get_published_posts(self, api_client, post):
        url = reverse('blog:post-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == post.title

    def test_filter_by_category(self, api_client, post, category):
        url = reverse('blog:post-list')
        
        response = api_client.get(url, {'category': category.slug})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_search_posts(self, api_client, post):
        url = reverse('blog:post-list')
        
        response = api_client.get(url, {'search': 'Test'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_featured_posts_only(self, api_client, user, category):
        from django.utils import timezone
        # Create a featured post
        featured_post = Post.objects.create(
            title='Featured Post',
            content='This is featured',
            author=user,
            category=category,
            status='published',
            is_featured=True,
            published_at=timezone.now()
        )
        
        url = reverse('blog:post-list')
        response = api_client.get(url, {'featured': 'true'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == featured_post.title


@pytest.mark.django_db
class TestPostDetailView:
    def test_get_post_detail(self, api_client, post):
        url = reverse('blog:post-detail', kwargs={'slug': post.slug})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title
        assert response.data['content'] == post.content
        assert 'related_posts' in response.data

    def test_get_non_existent_post(self, api_client):
        url = reverse('blog:post-detail', kwargs={'slug': 'non-existent'})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_view_count_increment(self, api_client, post):
        initial_views = post.views_count
        url = reverse('blog:post-detail', kwargs={'slug': post.slug})
        
        api_client.get(url)
        
        post.refresh_from_db()
        assert post.views_count == initial_views + 1


@pytest.mark.django_db
class TestPostCreateView:
    def test_create_post_authenticated(self, authenticated_client, category):
        url = reverse('blog:post-create')
        data = {
            'title': 'New Post',
            'content': 'This is a new post content.',
            'category': category.id,
            'status': 'draft'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.filter(title='New Post').exists()

    def test_create_post_unauthenticated(self, api_client, category):
        url = reverse('blog:post-create')
        data = {
            'title': 'New Post',
            'content': 'This is a new post content.',
            'category': category.id
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_post_with_tags(self, authenticated_client, category):
        url = reverse('blog:post-create')
        data = {
            'title': 'Post with Tags',
            'content': 'Content with tags.',
            'category': category.id,
            'tags': ['python', 'django'],
            'status': 'published'
        }
        
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        post = Post.objects.get(title='Post with Tags')
        assert post.tags.count() == 2


@pytest.mark.django_db
class TestPostUpdateView:
    def test_update_own_post(self, authenticated_client, user, category):
        post = Post.objects.create(
            title='Original Title',
            content='Original content',
            author=user,
            category=category
        )
        
        url = reverse('blog:post-update', kwargs={'slug': post.slug})
        data = {
            'title': 'Updated Title',
            'content': 'Updated content'
        }
        
        response = authenticated_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.title == 'Updated Title'
        assert post.content == 'Updated content'

    def test_update_other_user_post(self, api_client, post, user):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Create a different user
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        
        # Authenticate as the other user
        api_client.force_authenticate(user=other_user)
        
        url = reverse('blog:post-update', kwargs={'slug': post.slug})
        data = {
            'title': 'Hacked Title'
        }
        
        response = api_client.patch(url, data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCategoryListView:
    def test_get_categories(self, api_client, category):
        url = reverse('blog:category-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Check if response is paginated or not
        if 'results' in response.data:
            assert len(response.data['results']) == 1
            assert response.data['results'][0]['name'] == category.name
        else:
            assert len(response.data) == 1
            assert response.data[0]['name'] == category.name


@pytest.mark.django_db
class TestBlogStatsView:
    def test_get_blog_stats(self, api_client, post):
        url = reverse('blog:blog-stats')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'total_posts' in response.data
        assert 'total_categories' in response.data
        assert 'total_tags' in response.data
        assert response.data['total_posts'] == 1