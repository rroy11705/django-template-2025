from django.contrib.auth import logout
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import User
from .serializers import UserListSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from .services import UserAuthService, UserProfileService


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Remove password_confirm before passing to service
            validated_data = serializer.validated_data.copy()
            validated_data.pop("password_confirm", None)
            user = UserAuthService.register_user(**validated_data)
            token, created = Token.objects.get_or_create(user=user)

            return Response({"user": UserProfileSerializer(user).data, "token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            UserAuthService.login_user(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({"user": UserProfileSerializer(user).data, "token": token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass

    UserAuthService.logout_user(request)
    return Response({"message": "Successfully logged out"})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            UserProfileService.update_profile(user, **serializer.validated_data)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_stats_view(request):
    stats = UserProfileService.get_user_stats(request.user)
    return Response(stats)


class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
