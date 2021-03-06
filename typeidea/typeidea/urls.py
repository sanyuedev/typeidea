"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import CategoryView, PostDetailView, IndexView, TagView, SearchView, AuthorView
from comment.views import CommentView
from config.views import LinkListView
from typeidea.custom_site import custom_site
from blog.apis import PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/<category_id>', CategoryView.as_view(), name='category-list'),
    path('tags/<tag_id>', TagView.as_view(), name='tag-list'),
    path('post/<post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('links/', LinkListView.as_view(), name='links'),
    path('search/', SearchView.as_view(), name='search'),
    path('author/<owner_id>', AuthorView.as_view(), name='author'),
    path('comment/', CommentView.as_view(), name="comment"),
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('admin/', custom_site.urls),
    path('rss/', LatestPostFeed(), name='rss'),
    path('sitemap.xml', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap),
         {'sitemaps': {'posts': PostSitemap}}),
    path('api/', include(router.urls)),
]
