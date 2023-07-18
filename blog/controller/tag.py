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
def tags_page(request):
    # page: int = -1, is_paginator: bool = False, search_name: str = None
    if request.method == 'GET':
        page = request.GET.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
        search_name = request.GET.get('search_name')
        if search_name is None:
            tags = models.Tags.objects.all().values('id','name')
        else:
            tags = models.Tags.objects.filter(name__contains=search_name).values('id','name')
        if page <= 0:
            page = 1
        paginator = Paginator(tags, 15)
        try:
            tags = paginator.page(page)
        except PageNotAnInteger:
            tags = paginator.page(1)
        except EmptyPage:
            tags = paginator.page(paginator.num_pages)
        return render(request, 'management/tags/tags.html', context={'tags': tags})


def current_tag(request, name):
    tag_obj = models.Tags.objects.get(name=name)
    page = request.GET.get('page')
    if page is None:
        page = 0
    result = get_record_and_tags()

    context = {'current_category': tag_obj.name,
               'articles': article.get_article(is_paginator=True, page=int(page), tag=tag_obj),
               'records': result['records'],
               'tags': result['tags']
               }

    return render(request, 'category.html', context=context)


@login_required(login_url='/')
def get_all_tag(request):
    tags = serializers.serialize("json", models.Tags.objects.all())

    return JsonResponse(json.loads(tags), safe=False)


@login_required(login_url='/')
def search(request):
    term = request.GET.get("term")
    if term is not None and term != '':
        arr = []
        tags = models.Tags.objects.filter(name__contains=term)
        for item in tags:
            arr.append(item.name)
        return JsonResponse(arr, safe=False)
    else:
        arr = []
        tags = models.Tags.objects.all()
        for item in tags:
            arr.append(item.name)
        return JsonResponse(arr, safe=False)


@login_required(login_url='/')
def add_tag(request):
    if request.method == 'POST':
        tag_name = request.POST.get("tag_name")
        if tag_name == '':
            return JsonResponse({'success': False}, safe=False)
        else:
            obj = models.Tags(name=tag_name)
            obj.save()
            return JsonResponse({'success': True}, safe=False)
    else:
        raise ServerException("错误的请求")


@login_required(login_url='/')
def delete_tags(request):
    if request.method == 'GET':
        ids_str = request.GET.get("id")
        # models.Tags.objects.raw('DELETE FROM blog_tags WHERE id IN (%s)', ids_str)
        models.Tags.objects.get(id=int(ids_str)).delete()
        return HttpResponseRedirect('/management/tags')  # 跳转到主界面
    else:
        raise ServerException("错误的请求")
