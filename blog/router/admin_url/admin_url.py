"""IBE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from blog.controller import login, category, article, tag, files, approval
from blog.controller.admin import views

urlpatterns = [
    path('article', article.article, name='admin_article'),
    path('article/', include('blog.router.article_url.article_url')),
    path('tags/', include('blog.router.tag_url.tag_url')),
    path('tags', tag.tags_page, name='admin_tags'),
    path('category', category.category, name='admin_category'),
    path('category/', include('blog.router.category_url.category_url')),
    path('files', files.files, name='admin_files'),
    path('files/', include('blog.router.files_url.files_url')),
    path('approval/', include('blog.router.approval_url.approval')),
    path('', approval.approval_page, name=''),

]
urlpatterns += staticfiles_urlpatterns()
