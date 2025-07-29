from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("stats/", views.user_stats_view, name="stats"),
    path("list/", views.UserListView.as_view(), name="list"),
]
