import random
import re
from datetime import datetime

from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import blog
from blog import models
from blog.controller import article
from blog.controller.files import save_file

phone_pattern = re.compile(r'^d{11}$')


def vip_index(request):
    return render(request, 'vip.html')


def validate_id_number(id_number):
    area_codes = {
        '11', '12', '13', '14', '15', '21', '22', '23', '31', '32',
        '33', '34', '35', '36', '37', '41', '42', '43', '44', '45',
        '46', '50', '51', '52', '53', '54', '61', '62', '63', '64',
        '65', '71', '81', '82', '91'
    }
    """
    验证身份证号码是否合法

    Args:
        id_number (str): 待验证的身份证号码

    Returns:
        bool: 是否合法
    """
    # 验证身份证号码格式是否正确
    pattern = r'^\d{17}[\dXx]$'
    if not re.match(pattern, id_number):
        return False

    # 验证身份证号码中的地区码是否正确
    province_code = id_number[:2]
    if province_code not in area_codes:
        return False

    # 验证身份证号码中的出生日期是否正确
    birthday = id_number[6:14]
    try:
        datetime.strptime(birthday, '%Y%m%d')
    except ValueError:
        return False

    # 验证身份证号码中的校验码是否正确
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_map = {
        0: '1', 1: '0', 2: 'X', 3: '9', 4: '8',
        5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'
    }
    check_sum = sum(int(id_number[i]) * factors[i] for i in range(17))
    check_code = check_code_map[check_sum % 11]
    if check_code != id_number[-1].upper():
        return False

    # 身份证号码验证通过
    return True


def get_invited_code():
    code_list = []
    for i in range(6):  # 控制验证码的位数
        state = random.randint(1, 3)  # 生成状态码
        if state == 1:
            first_kind = random.randint(65, 90)  # 大写字母
            random_uppercase = chr(first_kind)
            code_list.append(random_uppercase)
        elif state == 2:
            second_kinds = random.randint(97, 122)  # 小写字母
            random_lowercase = chr(second_kinds)
            code_list.append(random_lowercase)
        elif state == 3:
            third_kinds = random.randint(0, 9)
            code_list.append(str(third_kinds))
    verification_code = "".join(code_list)
    return verification_code

def about(request):
    return render(request,'about.html')
def fuli(request):
    return render(request,'fuli.html')
def articledetails(request,pk):
    article = models.Article.objects.filter(id=int(pk)).values('id', 'title', 'intro', 'category',
                                                               'user', 'created_time', 'type',
                                                               'cover__file_net_path',
                                                               'music__file_net_path', 'status',
                                                               'category__name',
                                                               'user__first_name', 'user_id',
                                                               'user__last_name', 'markdown_text', 'is_top',
                                                               'html_text').first()
    result = get_record_and_tags()

    return render(request, 'details.html', context={'article': article, 'records': result['records'],
                                                    'tags': result['tags'],'other':  blog.controller.article.get_article(2)})

def nlogin(request):
    if request.method == 'GET':
        if request.session.has_key('nlogin') and request.session['nlogin']:
            return HttpResponseRedirect('/')  # 跳转到主界面
        else:
            return render(request, 'index_login.html')
    else:
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        nuser = models.NUser.objects.filter(phone_number=phone_number, password=password).first()
        if nuser is not None:
            request.session['nuser'] = nuser
            request.session['nlogin'] = True
            return HttpResponseRedirect('/index/vip')  # 跳转到主界面
        else:
            return render(request, 'index_login.html', context={'success': False, 'msg': '用户名密码错误'})

def nlogout(request):
    request.session['nuser'] = None
    request.session['nlogin'] = False
    return HttpResponseRedirect('/')  # 跳转到主界面


def check_phone(num):
    if len(num) != 11:
        print(num, "位数不正确")
    elif num[0] != '1':
        print(num, '首位数字不正确')
    elif num[1] < '3':
        print(num, '第二位数字不正确')
    else:
        return True


@xframe_options_sameorigin
def upload_id_img(request):
    if request.session.has_key('nlogin') and request.session['nlogin']:
        file_obj = request.FILES.get('file')
        try:
            file_record = save_file(file_obj=file_obj)
            nuser = request.session['nuser']
            nuser.identity_photo = file_record
            nuser.save()
            request.session['nuser'] = nuser

        except Exception as e:
            return JsonResponse({"errno": 1, "message": str(e)})
        return JsonResponse({"errno": 0, "data": {
            'src': file_record.file_net_path,
            'status': 200,
        }})
    else:
        return HttpResponseRedirect('/index/login')  # 跳转到主界面


def submit_approval(request):
    if request.method == 'POST':
        if request.session.has_key('nlogin') and request.session['nlogin']:
            nuser = request.session['nuser']
            nuser.approval_status = 3
            nuser.save()
            request.session['nuser'] = nuser
            return HttpResponseRedirect('/index/identity_check')  # 跳转到主界面
    else:
        return HttpResponseRedirect('/index/login')  # 跳转到主界面


def check_view(request):
    if request.method == 'POST':
        uid = request.GET.get('uid')
        nuser = models.NUser.objects.get(id=int(uid))
        return JsonResponse({"status": 200, "realname": str(nuser.real_name), "username": nuser.phone_number,
                             'pic': nuser.identity_photo_id,
                             'pic_url': nuser.identity_photo.file_net_path, 'shiming': nuser.approval_status})


def identity_check(request):
    if request.method == 'GET':
        if request.session.has_key('nlogin') and request.session['nlogin']:
            nuser = request.session['nuser']
            if nuser.real_name == None or nuser.identity_number == None:
                return HttpResponseRedirect('/index/check')  # 跳转到主界面
            else:
                return render(request, 'identity_check.html')
        else:
            return HttpResponseRedirect('/index/login')  # 跳转到主界面


def real_check(request):
    if request.method == 'GET':
        if request.session.has_key('nlogin') and request.session['nlogin']:
            return render(request, 'check.html')
        else:
            return HttpResponseRedirect('/index/login')  # 跳转到主界面
    else:
        real_name = request.POST.get('real_name')
        identity_number = request.POST.get('identity_number')
        uid = request.POST.get('uid')
        nuser = models.NUser.objects.get(id=int(uid))
        if real_name == None or identity_number == None:
            return render(request, 'check.html', {'success': False, 'msg': '名字和身份证不能为空'})
        elif not validate_id_number(identity_number):
            return render(request, 'check.html', {'success': False, 'msg': '身份证格式错误'})
        else:
            nuser.real_name = real_name
            nuser.identity_number = identity_number
            nuser.save()
            request.session['nuser'] = nuser
            return HttpResponseRedirect('/index/identity_check')  # 跳转到主界面


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        password = request.POST['password']
        phone_number = request.POST['phone']
        invited_code = request.POST['invited_code']
        if password == '' or password is None:
            return render(request, 'register.html', context={'success': False, 'msg': '密码必填'})
        if phone_number == '' or phone_number is None:
            return render(request, 'register.html', context={'success': False, 'msg': '手机必填'})
        if not check_phone(phone_number):
            return render(request, 'register.html', context={'success': False, 'msg': '手机号码格式错误'})

        user_obj = models.NUser.objects.filter(phone_number=phone_number).first()
        if user_obj is not None:
            return render(request, 'register.html', context={'success': False, 'msg': '手机已被注册'})

        if invited_code is not None and invited_code != '' and len(str(invited_code)) > 1:
            nuser = models.NUser.objects.filter(invitation_code=invited_code).first()
            if nuser is None:
                return render(request, 'register.html', context={'success': False, 'msg': '邀请码无效'})
            else:
                user_obj = models.NUser.objects.create(password=password,
                                                       invitation_code=get_invited_code(),
                                                       phone_number=phone_number,
                                                       create_time=datetime.now(),
                                                       approval_status=0, max_invitation_number=10)
                models.NUserRelation.objects.create(invitation_user=nuser, invited_user=user_obj)
                request.session['nuser'] = user_obj
                request.session['nlogin'] = True
                return HttpResponseRedirect('/index/check')  # 跳转到主界面

        else:
            user_obj = models.NUser.objects.create(password=password,
                                                   invitation_code=get_invited_code(),
                                                   phone_number=phone_number,
                                                   create_time=datetime.now(),
                                                   approval_status=0, max_invitation_number=10)
            request.session['nuser'] = user_obj
            request.session['nlogin'] = True
            return HttpResponseRedirect('/index/check')  # 跳转到主界面


def current_record(request, date):
    page = request.GET.get('page')
    if page is None:
        page = 0
    result = get_record_and_tags()
    context = {'current_record': date,
               'articles': article.get_article(is_paginator=True, page=int(page), date_record=date),
               'records': result['records'],
               'tags': result['tags']
               }

    return render(request, 'category.html', context=context)


def avatar(request, pk):
    sql = '''select avatar from auth_user au left join avatar_avatar aa on au.id = aa.user_id where au.id = {0}'''.format(
        pk)
    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    return HttpResponseRedirect('/' + fetchall[0][0])  # 跳转到主界面


# Create your views here.

@xframe_options_sameorigin
def index(request):
    article_sql = '''SELECT count(*) as count,strftime('%Y-%m',created_time) as datetime FROM blog_article group by strftime('%Y,%m',created_time)'''
    tag_sql = '''SELECT bt.id,bt.name,count() as count FROM blog_tags bt  left join blog_article_tags bat on bt.id = bat.tags_id group by bt.name
order by count desc limit 10'''
    cursor = connection.cursor()
    cursor.execute(article_sql)
    fetchall = cursor.fetchall()

    records = []
    for obj in fetchall:
        dic = {}
        dic['count'] = obj[0]
        dic['datetime'] = obj[1]
        records.append(dic)
    cursor.execute(tag_sql)
    fetchall = cursor.fetchall()
    tags = []
    for obj in fetchall:
        dic = {}
        dic['id'] = obj[0]
        dic['name'] = obj[1]
        dic['count'] = obj[2]
        tags.append(dic)
    context = {
        'articles_new': article.get_article(20),
        'records': records,
        'tags': tags
    }
    return render(request, 'index.html', context=context)


def get_record_and_tags():
    article_sql = '''SELECT count(*) as count,strftime('%Y-%m',created_time) as datetime FROM blog_article group by strftime('%Y,%m',created_time)'''
    tag_sql = '''SELECT bt.id,bt.name,count() as count FROM blog_tags bt  left join blog_article_tags bat on bt.id = bat.tags_id group by bt.name
    order by count desc limit 10'''
    cursor = connection.cursor()
    cursor.execute(article_sql)
    fetchall = cursor.fetchall()

    records = []
    for obj in fetchall:
        dic = {}
        dic['count'] = obj[0]
        dic['datetime'] = obj[1]
        records.append(dic)
    cursor.execute(tag_sql)
    fetchall = cursor.fetchall()
    tags = []
    for obj in fetchall:
        dic = {}
        dic['id'] = obj[0]
        dic['name'] = obj[1]
        dic['count'] = obj[2]
        tags.append(dic)
    context = {
        'records': records,
        'tags': tags
    }
    return context
