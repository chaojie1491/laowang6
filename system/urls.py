"""
URL configuration for system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from blog import views
from blog.controller import login, files
from system import settings
from django.urls import re_path as url

urlpatterns = [
                  path('user_avatar/<pk>', views.avatar),  # login_view is the custom login view    ,
                  path('admin/login/', login.login, name='new_admin_login'),  # login_view is the custom login view    ,
                  path('admin/', admin.site.urls),
                  path('', views.index, name='index'),
                  path('index', views.index),
                  path('category/', include('blog.router.category_url.category_url')),
                  path('article/', include('blog.router.article_url.article_url')),
                  path('date/<date>', views.current_record),

                  path('login', login.login),
                  path('index/login', views.nlogin),
                  path('index/nlogout', views.nlogout),
                  path('index/check', views.real_check),
                  path('index/vip', views.vip_index),
                  path('index/identity_check', views.identity_check),
                  path('index/real_check', views.real_check),
                  path('index/upload', views.upload_id_img),
                  path('index/submit_approval', views.submit_approval),
                  path('index/about', views.about),
                  path('index/fuli', views.fuli),
                  path('index/articledetails/<pk>.html', views.articledetails),

                  path('index/register', views.register),
                  path('logout', login.logout),
                  path('tag/', include('blog.router.tag_url.tag_url')),
                  path('management/', include('blog.router.admin_url.admin_url')),
                  path('avatar/', include('avatar.urls')),
                  url(r'^upload/files/(?P<path>.*)$', serve, {'document_root': settings.UPLOAD_ROOT})
              ] + static('/avatars', document_root=settings.AVATAR_DIR)
