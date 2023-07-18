import json
from datetime import datetime

from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

import blog
from blog import models
from system.error.ServerException import ServerException


@login_required(login_url='/login')
def article(request):
    page = request.GET.get('page')
    search_title = request.GET.get('search_title')
    search_content = request.GET.get('search_content')
    if page is None:
        page = 0
    articles = blog.controller.article.get_article(is_paginator=True, page=int(page), search_title=search_title,
                                                   search_content=search_content)
    return render(request, 'management/article/article.html', context={'articles': articles})


def new(request):
    return render(request, 'management/article/new_article.html')


def show_article(request, pk):
    article = models.Article.objects.filter(id=int(pk)).values('id', 'title', 'intro', 'category',
                                                               'user', 'created_time', 'type',
                                                               'cover__file_net_path',
                                                               'music__file_net_path', 'status',
                                                               'category__name',
                                                               'user__first_name', 'user_id',
                                                               'user__last_name', 'markdown_text', 'is_top',
                                                               'html_text').first()
    from blog.views import get_record_and_tags
    result = get_record_and_tags()

    return render(request, 'details.html', context={'article': article, 'records': result['records'],
               'tags': result['tags']})


@login_required(login_url='/')
def to_edit(request, pk):
    article = models.Article.objects.filter(id=int(pk)).values('id', 'title', 'intro', 'category',
                                                               'user', 'created_time', 'type',
                                                               'cover__file_net_path',
                                                               'music__file_net_path', 'status',
                                                               'category__name',
                                                               'user__first_name', 'user_id',
                                                               'user__last_name', 'markdown_text', 'html_text',
                                                               'is_top').first()
    tags = models.Tags.objects.raw(
        'select * from blog_tags left join blog_article_tags bat on blog_tags.id = bat.tags_id where  bat.article_id = {0}'.format(
            int(pk)))
    tags_str = []
    for tag in tags:
        tags_str.append(tag.name)
    return render(request, 'management/article/edit_article.html',
                  context={'article': article, 'tags': ','.join(tags_str)})


@login_required(login_url='/')
def edit_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        intro = request.POST['intro']
        category = request.POST['category']
        html_text = request.POST['html']
        markdown_text = request.POST['markdown']
        type_ = request.POST['type']
        status = request.POST['status']
        tags = request.POST['tags']
        pk = request.POST['pk']
        is_top = request.POST['is_top']
        category_obj = models.Category.objects.get(id=category)

        article_obj = models.Article.objects.get(id=int(pk))
        tags_id = []
        for tag in str(tags).split(','):
            tag_obj = models.Tags.objects.filter(name=tag).first()
            if tag_obj is None:
                obj = models.Tags(name=tag)
                obj.save()
                tags_id.append(obj.pk)
            else:
                tags_id.append(tag_obj.pk)
        if len(tags_id) > 0:
            article_obj.tags.set(tags_id)
        # models.Article.objects.filter(id=int(pk)).update(title=title, intro=intro, category=category_obj,
        #                                                  html_text=html_text,
        #                                                  markdown_text=markdown_text,
        #                                                  type=type_, status=status,
        #                                                  tags=str(tags).split(',')
        #                                                  )
        article_obj.title = title
        article_obj.intro = intro
        article_obj.category = category_obj
        article_obj.html_text = html_text
        article_obj.markdown_text = markdown_text
        article_obj.type = type_
        article_obj.status = status
        article_obj.is_top = is_top
        article_obj.save()
        return JsonResponse({"success": True, "message": "修改成功"})
    else:
        raise ServerException("错误的请求")


def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        intro = request.POST['intro']
        category = request.POST['category']
        html_text = request.POST['html']
        markdown_text = request.POST['markdown']
        type_ = request.POST['type']
        status = request.POST['status']
        tags = request.POST['tags']
        is_top = request.POST['is_top']

        category_obj = models.Category.objects.get(id=category)

        article_obj = models.Article.objects.create(title=title, intro=intro, category=category_obj,
                                                    html_text=html_text,
                                                    markdown_text=markdown_text,
                                                    type=type_, status=status, user=UserModel.objects.get(pk=1),
                                                    created_time=datetime.now(),
                                                    is_top=is_top
                                                    )
        tags_id = []
        for tag in str(tags).split(','):
            tag_obj = models.Tags.objects.filter(name=tag).first()
            if tag_obj is None:
                obj = models.Tags(name=tag)
                obj.save()
                tags_id.append(obj.pk)
            else:
                tags_id.append(tag_obj.pk)
        if len(tags_id) > 0:
            article_obj.tags.set(tags_id)
        return JsonResponse({"success": True, "message": "添加成功"})
    else:
        raise ServerException("错误的请求")


@login_required(login_url='/')
def add_media(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        type_ = request.POST['type']
        status = request.POST['status']
        tags = request.POST['tags']
        cover = request.POST['cover_id']
        music_id = request.POST['music_id']
        cover_obj = models.FileRecord.objects.get(id=cover)
        music_obj = models.FileRecord.objects.get(id=music_id)

        category_obj = models.Category.objects.get(id=category)
        article_obj = models.Article.objects.create(title=title, category=category_obj,
                                                    type=type_, status=status, user=request.user,
                                                    created_time=datetime.now(),
                                                    cover=cover_obj, music=music_obj
                                                    )
        if tags != 'null':
            article_obj.tags.set(str(tags).split(','))
        return JsonResponse({"success": True, "message": "添加成功"})
    else:
        raise ServerException("错误的请求")


@login_required(login_url='/')
def add_music(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        type_ = request.POST['type']
        status = request.POST['status']
        tags = request.POST['tags']
        cover = request.POST['cover_id']
        music_id = request.POST['music_id']
        cover_obj = models.FileRecord.objects.get(id=cover)
        music_obj = models.FileRecord.objects.get(id=music_id)

        category_obj = models.Category.objects.get(id=category)
        article_obj = models.Article.objects.create(title=title, category=category_obj,
                                                    type=type_, status=status, user=request.user,
                                                    created_time=datetime.now(),
                                                    cover=cover_obj, music=music_obj
                                                    )
        if tags != 'null':
            article_obj.tags.set(str(tags).split(','))
        return JsonResponse({"success": True, "message": "添加成功"})
    else:
        raise ServerException("错误的请求")


def set_tag(articles):
    for i in range(len(articles)):
        tags = models.Tags.objects.raw(
            'select * from blog_tags left join blog_article_tags bat on blog_tags.id = bat.tags_id where  bat.article_id = {0}'.format(
                articles[i]['id']))
        tags_field = []
        for item in tags:
            tags_field.append(item.name)
        articles[i]['tags'] = tags_field


def get_article(top: int = -1, page: int = -1, is_paginator: bool = False, category: models.Category = None,
                tag: models.Tags = None, search_title: str = None, search_content: str = None, date_record: str = None):
    if category is None and tag is None:
        search_dict = dict()
        if search_title:
            search_dict['title__contains'] = search_title
        if search_content:
            search_dict['markdown_text__contains'] = search_content
        articles = models.Article.objects.filter(**search_dict).order_by('-created_time').values(
            'id', 'title', 'intro', 'category',
            'user', 'created_time', 'type',
            'cover__file_net_path',
            'music__file_net_path', 'status',
            'category__name','net_cover',
            'user__first_name', 'user_id',
            'user__last_name',
            'is_top', 'html_text')
    elif date_record is not None:
        date_format = "%Y-%m"
        date = datetime.strptime(date_record, date_format)
        articles = models.Article.objects.filter(created_time__year=date.year,created_time__month=date.month).order_by('-created_time').values('id', 'title',
                                                                                                       'intro',
                                                                                                       'category',
                                                                                                       'user',
                                                                                                       'created_time',
                                                                                                       'type',
                                                                                                                                               'net_cover',

                                                                                                                                               'cover__file_net_path',
                                                                                                       'music__file_net_path',
                                                                                                       'status',
                                                                                                       'category__name',
                                                                                                       'user__first_name',
                                                                                                       'user_id',
                                                                                                       'user__last_name',
                                                                                                       'tags__name',
                                                                                                       'is_top',
                                                                                                       'html_text')
    elif tag is not None:
        articles = models.Article.objects.filter(tags__name=tag.name).order_by('-created_time').values('id', 'title',
                                                                                                       'intro',
                                                                                                       'category',
                                                                                                       'user',
                                                                                                       'created_time',
                                                                                                       'type',
                                                                                                       'net_cover',

                                                                                                       'cover__file_net_path',
                                                                                                       'music__file_net_path',
                                                                                                       'status',
                                                                                                       'category__name',
                                                                                                       'user__first_name',
                                                                                                       'user_id',
                                                                                                       'user__last_name',
                                                                                                       'tags__name',
                                                                                                       'is_top',
                                                                                                       'html_text')
    else:
        articles = models.Article.objects.filter(category_id=category.id).order_by('-created_time').values('id', 'title',
                                                                                                     'intro',
                                                                                                     'category',
                                                                                                     'user',
                                                                                                     'created_time',
                                                                                                     'type',
                                                                                                           'net_cover',
                                                                                                     'cover__file_net_path',
                                                                                                     'music__file_net_path',
                                                                                                     'status',
                                                                                                     'category__name',
                                                                                                     'user__first_name',
                                                                                                     'user_id',
                                                                                                     'user__last_name',
                                                                                                     'is_top',
                                                                                                     'html_text')

    if is_paginator:
        if page <= 0:
            page = 1
        paginator = Paginator(articles, 15)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        set_tag(articles=articles)

        return articles
    else:
        articles = list(articles)
    if top > -1:
        articles = articles[:top]
    set_tag(articles=articles)
    return articles
    # return JsonResponse({'all_article': json.loads(json.dumps(articles, default=str))})


@login_required(login_url='/')
def get_all_article(request):
    articles = models.Article.objects.order_by('-created_time').values('id', 'title',
                                                                       'intro',
                                                                       'category',
                                                                       'user',
                                                                       'created_time',
                                                                       'type',
                                                                       'cover__file_net_path',
                                                                       'music__file_net_path',
                                                                       'status',
                                                                       'category__name',
                                                                       'user__first_name', 'user_id',
                                                                       'user__last_name')
    return JsonResponse(json.loads(json.dumps(list(articles), default=str)), safe=False)


@login_required(login_url='/')
def delete_article(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        article = models.Article.objects.get(id=int(id))
        article.tags.clear()
        article.delete()

        return HttpResponseRedirect('/management/article')  # 跳转到主界面
    else:
        raise ServerException("错误的请求")
