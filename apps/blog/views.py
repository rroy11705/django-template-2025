from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Category, Comment, Post, Tag
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    TagSerializer,
)
from .services import BlogAnalyticsService, BlogCommentService, BlogPostService, BlogRecommendationService


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = BlogPostService.get_published_posts()

        # Filter by category
        category = self.request.query_params.get("category")
        if category:
            queryset = BlogPostService.get_posts_by_category(category)

        # Filter by tag
        tag = self.request.query_params.get("tag")
        if tag:
            queryset = BlogPostService.get_posts_by_tag(tag)

        # Filter by author
        author = self.request.query_params.get("author")
        if author:
            queryset = BlogPostService.get_posts_by_author(author)

        # Search functionality
        search = self.request.query_params.get("search")
        if search:
            queryset = BlogPostService.search_posts(search)

        # Featured posts only
        featured = self.request.query_params.get("featured")
        if featured == "true":
            queryset = queryset.filter(is_featured=True)

        return queryset


class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return BlogPostService.get_published_posts()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increment view count
        BlogPostService.increment_post_views(instance)

        serializer = self.get_serializer(instance)
        data = serializer.data

        # Add related posts
        related_posts = BlogRecommendationService.get_related_posts(instance)
        data["related_posts"] = PostListSerializer(related_posts, many=True).data

        return Response(data)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_slug = self.kwargs.get("post_slug")
        post = get_object_or_404(Post, slug=post_slug, status="published")

        BlogCommentService.create_comment(post=post, author=self.request.user, content=serializer.validated_data["content"])


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def featured_posts_view(request):
    posts = BlogPostService.get_featured_posts()
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def popular_posts_view(request):
    posts = BlogAnalyticsService.get_popular_posts()
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def recent_posts_view(request):
    posts = BlogAnalyticsService.get_recent_posts()
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def blog_stats_view(request):
    stats = BlogAnalyticsService.get_blog_stats()
    return Response(stats)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
