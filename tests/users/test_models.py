import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.check_password('testpass123')
        assert not user.is_verified
        assert user.is_active

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
        
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

    def test_email_unique(self):
        User.objects.create_user(
            email='test@example.com',
            username='user1',
            password='testpass123'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                username='user2',
                password='testpass123'
            )

    def test_full_name_property(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        
        assert user.full_name == 'John Doe'

    def test_get_short_name(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        
        assert user.get_short_name() == 'John'

    def test_str_representation(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        assert str(user) == 'test@example.com'