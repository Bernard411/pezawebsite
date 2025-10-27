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


# 📝 Article Detail Page
def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()

    # Increment views safely
    Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
    article.refresh_from_db()

    context = {
        'article': article,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'article_detail.html', context)


# 🔧 Tool Detail Page
def tool_detail_view(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()

    context = {
        'tool': tool,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'tool_detail.html', context)


# 📁 Resource Detail Page
def resource_detail_view(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    popular_posts = Article.objects.order_by('-views')[:4]
    categories = Category.objects.all()

    context = {
        'resource': resource,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    return render(request, 'resource_detail.html', context)
