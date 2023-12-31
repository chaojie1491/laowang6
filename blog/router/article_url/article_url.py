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
from django.urls import path
from blog import views
from blog.controller import login, category, article

urlpatterns = [
    path('new', article.new, name='article_new'),
    path('add_article', article.add_article),
    path('get_all_article', article.get_all_article),
    path('to_edit/<pk>', article.to_edit),
    path(r'<pk>.html', article.show_article),
    path('edit_article', article.edit_article),
    path('delete_article', article.delete_article),
]
urlpatterns += staticfiles_urlpatterns()
