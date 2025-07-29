from typing import Optional

from django.conf import settings
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import User


class UserAuthService:
    @staticmethod
    def register_user(email: str, username: str, first_name: str, last_name: str, password: str) -> User:
        user = User.objects.create_user(
            email=email, username=username, first_name=first_name, last_name=last_name, password=password
        )

        # Send welcome email (implement as needed)
        UserEmailService.send_welcome_email(user)

        return user

    @staticmethod
    def login_user(request, user: User) -> None:
        login(request, user)

    @staticmethod
    def logout_user(request) -> None:
        logout(request)


class UserProfileService:
    @staticmethod
    def update_profile(user: User, **kwargs) -> User:
        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def get_user_stats(user: User) -> dict:
        from apps.blog.models import Post

        return {
            "posts_count": Post.objects.filter(author=user).count(),
            "is_verified": user.is_verified,
            "member_since": user.created_at,
        }


class UserEmailService:
    @staticmethod
    def send_welcome_email(user: User) -> bool:
        try:
            send_mail(
                subject="Welcome to Our Platform!",
                message=f"Hello {user.first_name}, welcome to our platform!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            # Log the error in production
            print(f"Failed to send welcome email: {e}")
            return False

    @staticmethod
    def send_password_reset_email(user: User, reset_token: str) -> bool:
        try:
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
            send_mail(
                subject="Password Reset Request",
                message=f"Click here to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Failed to send password reset email: {e}")
            return False
