import os
import django
from django.conf import settings

# Configure Django settings before importing Django modules
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.blog.models import Category, Post, Tag

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def category():
    return Category.objects.create(
        name='Technology',
        description='Posts about technology'
    )


@pytest.fixture
def tag():
    return Tag.objects.create(name='Python')


@pytest.fixture
def post(user, category):
    from django.utils import timezone
    return Post.objects.create(
        title='Test Post',
        content='This is a test post content.',
        author=user,
        category=category,
        status='published',
        published_at=timezone.now()
    )