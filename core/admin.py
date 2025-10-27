from django.contrib import admin
from .models import Category, Article, Tool, Resource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'is_tutorial',
        'is_featured', 'views', 'read_time', 'published_at'
    )
    list_filter = ('category', 'is_tutorial', 'is_featured', 'published_at')
    search_fields = ('title', 'content', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    autocomplete_fields = ('category',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    # ❌ Removed filter_horizontal for tags (not supported by taggit)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'external_link', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    ordering = ('name',)
    autocomplete_fields = ('category',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'external_link', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    ordering = ('name',)
    autocomplete_fields = ('category',)
