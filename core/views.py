from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Article, Tool, Resource, Category


# 🏠 Home Page
def home_view(request):
    articles = Article.objects.filter(is_tutorial=True).order_by('-published_at')[:4]
    featured_article = Article.objects.filter(is_featured=True).first()
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'featured_article': featured_article,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'index.html', context)


# 📘 Tutorials Page
def tutorials_view(request):
    tutorials = Article.objects.filter(is_tutorial=True).order_by('-published_at')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'tutorials': tutorials,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'tutorials.html', context)


# 📰 Blog Page
def blog_view(request):
    posts = Article.objects.filter(is_tutorial=False).order_by('-published_at')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'blogs.html', context)


# 🧰 Tools Page
def tools_view(request):
    tools = Tool.objects.all().order_by('name')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'tools': tools,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'tools.html', context)


# 📚 Resources Page
def resources_view(request):
    resources = Resource.objects.all().order_by('name')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'resources': resources,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'resources.html', context)


# 📝 Article Detail Page (UPDATED WITH IMAGE CONTEXT)
def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    # Increment views safely
    Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
    article.refresh_from_db()
    
    # Get image data for the article
    content_images = article.get_content_images()
    featured_image = article.featured_image
    has_images = article.has_images()
    image_count = article.count_content_images()
    
    # Get related articles (same category, exclude current)
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(pk=article.pk).order_by('-published_at')[:3]
    
    context = {
        'article': article,
        'popular_posts': popular_posts,
        'categories': categories,
        'content_images': content_images,  # All images from content
        'featured_image': featured_image,  # Banner or first content image
        'has_images': has_images,          # Boolean
        'image_count': image_count,        # Number of images in content
        'related_articles': related_articles,
    }
    return render(request, 'article_detail.html', context)


# 🔧 Tool Detail Page
def tool_detail_view(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    # Get related tools (same category, exclude current)
    related_tools = Tool.objects.filter(
        category=tool.category
    ).exclude(pk=tool.pk)[:3]
    
    context = {
        'tool': tool,
        'popular_posts': popular_posts,
        'categories': categories,
        'related_tools': related_tools,
    }
    return render(request, 'tool_detail.html', context)


# 📁 Resource Detail Page
def resource_detail_view(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    # Get related resources (same category, exclude current)
    related_resources = Resource.objects.filter(
        category=resource.category
    ).exclude(pk=resource.pk)[:3]
    
    context = {
        'resource': resource,
        'popular_posts': popular_posts,
        'categories': categories,
        'related_resources': related_resources,
    }
    return render(request, 'resource_detail.html', context)


# 🏷️ Articles by Category
def articles_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by('-published_at')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'articles': articles,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'category_articles.html', context)


# 🏷️ Articles by Tag
def articles_by_tag(request, tag):
    from taggit.models import Tag
    tag_obj = get_object_or_404(Tag, slug=tag)
    articles = Article.objects.filter(tags__slug=tag).order_by('-published_at')
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'tag': tag_obj,
        'articles': articles,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'tag_articles.html', context)


# 🔍 Search View
def search_view(request):
    query = request.GET.get('q', '')
    articles = []
    
    if query:
        articles = Article.objects.filter(
            title__icontains=query
        ) | Article.objects.filter(
            content__icontains=query
        )
        articles = articles.order_by('-published_at').distinct()
    
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()
    
    context = {
        'query': query,
        'articles': articles,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'search_results.html', context)