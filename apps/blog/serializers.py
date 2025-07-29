from rest_framework import serializers

from .models import Category, Comment, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "posts_count", "created_at"]

    def get_posts_count(self, obj):
        return obj.posts.filter(status="published").count()


class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "posts_count", "created_at"]

    def get_posts_count(self, obj):
        return obj.posts.filter(status="published").count()


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "author_name", "author_username", "is_approved", "created_at", "updated_at"]
        read_only_fields = ["author_name", "author_username", "is_approved", "created_at", "updated_at"]


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    comments_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author_name",
            "author_username",
            "category_name",
            "excerpt",
            "featured_image",
            "is_featured",
            "views_count",
            "comments_count",
            "reading_time",
            "created_at",
            "published_at",
        ]

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def get_reading_time(self, obj):
        # Estimate reading time (average 200 words per minute)
        word_count = len(obj.content.split())
        return max(1, round(word_count / 200))


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_avatar = serializers.ImageField(source="author.avatar", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "author_name",
            "author_username",
            "author_avatar",
            "category",
            "content",
            "excerpt",
            "featured_image",
            "tags",
            "is_featured",
            "views_count",
            "comments",
            "comments_count",
            "reading_time",
            "created_at",
            "updated_at",
            "published_at",
        ]

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        return max(1, round(word_count / 200))


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["title", "category", "content", "excerpt", "featured_image", "status", "is_featured", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)

        # Handle tags
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            post.tags.add(tag)

        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle tags if provided
        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                instance.tags.add(tag)

        return instance
