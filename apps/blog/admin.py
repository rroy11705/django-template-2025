from django.contrib import admin

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "is_featured", "views_count", "created_at", "published_at")
    list_filter = ("status", "is_featured", "category", "created_at", "published_at")
    search_fields = ("title", "content", "author__username", "author__email")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "author", "category")}),
        ("Content", {"fields": ("content", "excerpt", "featured_image")}),
        ("Settings", {"fields": ("status", "is_featured", "tags")}),
        ("Metadata", {"fields": ("views_count", "published_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ("views_count",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "author__username", "post__title")
    actions = ["approve_comments", "unapprove_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

    unapprove_comments.short_description = "Unapprove selected comments"
