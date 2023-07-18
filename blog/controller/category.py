import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from blog.views import get_record_and_tags
from system.error.ServerException import ServerException
from blog import models
from blog.controller import article


@login_required(login_url='/')
def category(request):
    # page: int = -1, is_paginator: bool = False, search_name: str = None
    if request.method == 'GET':
        page = request.GET.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
        search_name = request.GET.get('search_name')
        if search_name is None:
            category = models.Category.objects.all().values('id', 'name','seq')
        else:
            category = models.Category.objects.filter(name__contains=search_name).values('id', 'name','seq')
        if page <= 0:
            page = 1
        paginator = Paginator(category, 15)
        try:
            category = paginator.page(page)
        except PageNotAnInteger:
            category = paginator.page(1)
        except EmptyPage:
            category = paginator.page(paginator.num_pages)
        return render(request, 'management/category/category.html', context={'category': category})


def current_category(request, name):
    category_obj = models.Category.objects.get(name=name)
    page = request.GET.get('page')
    if page is None:
        page = 0
    result = get_record_and_tags()
    context = {'current_category': category_obj.name,
               'articles': article.get_article(is_paginator=True, page=int(page), category=category_obj),
               'records': result['records'],
               'tags': result['tags']
               }

    return render(request, 'category.html', context=context)


@login_required(login_url='/')
def get_all_category(request):
    category = serializers.serialize("json", models.Category.objects.all())
    return JsonResponse(json.loads(category), safe=False)


@login_required(login_url='/')
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get("category_name")
        seq = request.POST.get("seq")
        if category_name == '':
            return HttpResponseRedirect('/management/category')
        else:
            obj = models.Category(name=category_name, seq=int(seq))
            obj.save()
            return HttpResponseRedirect('/management/category')
    else:
        raise ServerException("错误的请求")


@login_required(login_url='/')
def delete_category(request):
    if request.method == 'GET':
        ids_str = request.GET.get("id")
        models.Category.objects.get(id=int(ids_str)).delete()
        return HttpResponseRedirect('/management/category')  # 跳转到主界面
    else:
        raise ServerException("错误的请求")
