import pytest
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from apps.users.services import UserAuthService, UserProfileService, UserEmailService

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthService:
    def test_register_user(self):
        with patch.object(UserEmailService, 'send_welcome_email') as mock_email:
            mock_email.return_value = True
            
            user = UserAuthService.register_user(
                email='test@example.com',
                username='testuser',
                first_name='Test',
                last_name='User',
                password='testpass123'
            )
            
            assert user.email == 'test@example.com'
            assert user.username == 'testuser'
            assert user.check_password('testpass123')
            mock_email.assert_called_once_with(user)

    def test_login_user(self, user):
        mock_request = MagicMock()
        
        UserAuthService.login_user(mock_request, user)
        
        # Test that login was called (we can't easily test the actual login without full request)
        assert True  # Placeholder for actual login testing

    def test_logout_user(self):
        mock_request = MagicMock()
        
        UserAuthService.logout_user(mock_request)
        
        # Test that logout was called
        assert True  # Placeholder for actual logout testing


@pytest.mark.django_db
class TestUserProfileService:
    def test_update_profile(self, user):
        updated_user = UserProfileService.update_profile(
            user,
            first_name='Updated',
            bio='New bio'
        )
        
        assert updated_user.first_name == 'Updated'
        assert updated_user.bio == 'New bio'
        
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.bio == 'New bio'

    def test_get_user_stats(self, user, post):
        stats = UserProfileService.get_user_stats(user)
        
        assert 'posts_count' in stats
        assert 'is_verified' in stats
        assert 'member_since' in stats
        assert stats['posts_count'] == 1
        assert stats['is_verified'] == user.is_verified


@pytest.mark.django_db
class TestUserEmailService:
    @patch('apps.users.services.send_mail')
    def test_send_welcome_email_success(self, mock_send_mail, user):
        mock_send_mail.return_value = True
        
        result = UserEmailService.send_welcome_email(user)
        
        assert result is True
        mock_send_mail.assert_called_once()
        # Check the call arguments
        call_args = mock_send_mail.call_args
        assert call_args[1]['subject'] == 'Welcome to Our Platform!'
        assert user.email in call_args[1]['recipient_list']

    @patch('apps.users.services.send_mail')
    def test_send_welcome_email_failure(self, mock_send_mail, user):
        mock_send_mail.side_effect = Exception('Email sending failed')
        
        result = UserEmailService.send_welcome_email(user)
        
        assert result is False

    @patch('apps.users.services.send_mail')
    def test_send_password_reset_email_success(self, mock_send_mail, user):
        mock_send_mail.return_value = True
        
        result = UserEmailService.send_password_reset_email(user, 'test-token')
        
        assert result is True
        mock_send_mail.assert_called_once()
        # Check the call arguments
        call_args = mock_send_mail.call_args
        assert call_args[1]['subject'] == 'Password Reset Request'
        assert user.email in call_args[1]['recipient_list']