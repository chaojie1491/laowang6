import hashlib
import os
import uuid
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from blog import models
from system import settings
from system.error.ServerException import ServerException


@xframe_options_sameorigin
@login_required(login_url='/')
def upload_markdown_img(request):
    file_obj = request.FILES.get('file')
    try:
        file_record = save_file(file_obj=file_obj)
    except Exception as e:
        return JsonResponse({"errno": 1, "message": str(e)})
    from PIL import Image

    img = Image.open(file_record.file_path + file_record.file_name)
    width, height = img.size
    print('Image size: {}x{}'.format(width, height))

    return JsonResponse({"errno": 0, "data": {
        'url': file_record.file_net_path,
        'alt': '',
        "href": file_record.file_net_path,
        "width": width,
        "height": height
    }})




def save_file(file_obj):
    def get_unique_str():
        uuid_str = str(uuid.uuid4())
        md5 = hashlib.md5()
        md5.update(uuid_str.encode('utf-8'))
        return md5.hexdigest()

    if file_obj is None:
        raise ServerException('文件不存在')
    else:
        file_type = file_obj.name.split('.')[-1]

        filename = get_unique_str() + '.' + file_obj.name.split('.')[-1]
        filepath = os.path.join(settings.UPLOAD_ROOT + '/' + file_type + '/')
        if not os.path.exists(filepath):
            os.mkdir(filepath)

        file_net_path = settings.DOMAIN + settings.UPLOAD_URL + '/' + file_type + '/' + filename

        f = open(filepath + filename, 'wb')
        for i in file_obj.chunks():
            f.write(i)
        f.close()

    file_record = models.FileRecord.objects.create(origin_name=file_obj.name, file_name=filename, file_path=filepath,
                                                   create_date=datetime.now(),
                                                   suffix=file_obj.name.split('.')[-1], file_net_path=file_net_path)
    return file_record


@login_required(login_url='/')
def files(request):
    # page: int = -1, is_paginator: bool = False, search_name: str = None
    if request.method == 'GET':
        page = request.GET.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
        search_name = request.GET.get('search_name')
        if search_name is None:
            files = models.FileRecord.objects.all()
        else:
            files = models.FileRecord.objects.filter(origin_name__contains=search_name)
        if page <= 0:
            page = 1
        paginator = Paginator(files, 15)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)
        return render(request, 'management/files/files.html', context={'files': files})


@login_required(login_url='/')
def delete(request):
    # page: int = -1, is_paginator: bool = False, search_name: str = None

    if request.method == 'GET':
        ids_str = request.GET.get("id")
        # models.files.objects.raw('DELETE FROM blog_files WHERE id IN (%s)', ids_str)
        models.FileRecord.objects.get(id=int(ids_str)).delete()
        return HttpResponseRedirect('/management/files')  # 跳转到主界面
    else:
        raise ServerException("错误的请求")
