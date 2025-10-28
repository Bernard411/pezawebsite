from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Articles / Blog / Tutorials
    path('tutorials/', views.tutorials_view, name='tutorials'),
    path('blog/', views.blog_view, name='blog'),
    path('article/<slug:slug>/', views.article_detail_view, name='article_detail'),

    # Tools
    path('tools/', views.tools_view, name='tools'),
    path('tool/<slug:slug>/', views.tool_detail_view, name='tool_detail'),

    # Resources
    path('resources/', views.resources_view, name='resources'),
    path('resource/<slug:slug>/', views.resource_detail_view, name='resource_detail'),
    
    path('category/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
    path('tag/<slug:tag>/', views.articles_by_tag, name='articles_by_tag'),
    path('search/', views.search_view, name='search'),
]
