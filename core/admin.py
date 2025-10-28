from django.contrib import admin
from .models import Category, Article, ArticleImage, Tool, Resource

# Inline image management for Articles
class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    fields = ('image_url', 'is_banner')
    readonly_fields = ()
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time', 'is_tutorial', 'is_featured', 'views', 'published_at')
    list_filter = ('is_tutorial', 'is_featured', 'category', 'published_at')
    search_fields = ('title', 'content', 'category__name', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleImageInline]
    readonly_fields = ('views', 'created_at', 'updated_at')
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    autocomplete_fields = ('category',)
    filter_horizontal = ()  # Removed 'tags' since Taggit uses its own through model


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image_url', 'is_banner')
    list_filter = ('is_banner',)
    search_fields = ('article__title',)
    autocomplete_fields = ('article',)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'external_link', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    ordering = ('name',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'file_url', 'external_link', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    ordering = ('name',)
