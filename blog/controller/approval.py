from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path

from blog import models
from blog.excel import nuser_excel


@login_required(login_url='/')
def approval_page(request):
    page = request.GET.get('page')
    search_real_name = request.GET.get('search_real_name')
    search_phone_number = request.GET.get('search_phone_number')
    search_status = request.GET.get('search_status')
    if page is None:
        page = 0
    search_dict = dict()
    if search_real_name:
        search_dict['real_name__contains'] = search_real_name
    if search_phone_number:
        search_dict['phone_number__contains'] = search_phone_number
    if search_status:
        search_dict['approval_status'] = search_status
    nusers = models.NUser.objects.filter(**search_dict).values('phone_number',
                                                               'real_name', 'identity_number', 'id',
                                                               'password', 'identity_photo__file_net_path',
                                                               'status', 'approval_status', 'approval_time',
                                                               'create_time', 'invitation_code',
                                                               'invitation_user__invited_user__real_name',
                                                               'invited_user__invitation_user__real_name',
                                                               )
    if int(page) <= 0:
        page = 1
    paginator = Paginator(nusers, 15)
    try:
        pnusers = paginator.page(page)
    except PageNotAnInteger:
        pnusers = paginator.page(1)
    except EmptyPage:
        pnusers = paginator.page(paginator.num_pages)
    new_arr = []
    for u in pnusers:
        u['count'] = get_count(u['id'], 0)
        u['invitation_user'] = get_invitation_user(u['id'])
    return render(request, 'management/approval/approval.html', context={'users': pnusers})


def get_invitation_user(id):
    sql = '''select bn.real_name from blog_nuser bn left join blog_nuserrelation b on bn.id = b.invitation_user_id

where b.invited_user_id = (select b.invited_user_id from blog_nuser bn left join blog_nuserrelation b on bn.id = b.invitation_user_id where b.invited_user_id = {0})'''.format(
        int(id))

    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    if len(fetchall) == 0:
        return ''
    elif fetchall[0][0] == '':
        return ''
    else:
        return fetchall[0][0]


def get_count(id, count):
    sql = '''select count(*),b.invited_user_id as count from blog_nuser bn left join blog_nuserrelation b on bn.id = b.invitation_user_id where b.invitation_user_id = {0}'''.format(
        id)
    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    if fetchall[0][0] == 0:
        return count
    else:
        count += fetchall[0][0]
        return get_count(fetchall[0][1], count)


def get_child(id, users: list):
    sql = '''select b.invited_user_id from blog_nuser bn left join blog_nuserrelation b on bn.id = b.invitation_user_id where invitation_user_id = {0}'''.format(
        id)
    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    id_1 = fetchall[0]
    if len(fetchall) > 0:
        _sql = '''select bn.* from blog_nuser bn left join blog_nuserrelation b on bn.id = b.invitation_user_id where b.invitation_user_id  = {0}'''.format(
            id_1)
        nuser = models.NUser.objects.raw(_sql)
        if len(fetchall) > 0:
            users.append(nuser)
            get_child(id_1, users)


@login_required(login_url='/')
def update(request, pk):
    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')
    real_name = request.POST.get('real_name')
    identity_number = request.POST.get('identity_number')
    invitation_code = request.POST.get('invitation_code')
    max_invitation_number = request.POST.get('max_invitation_number')
    photo_id = request.POST.get('photo_id')
    nuser_obj = models.NUser.objects.get(id=int(pk))

    if photo_id is not None and photo_id != '':
        file = models.FileRecord.objects.get(id=int(photo_id))
        nuser_obj.identity_photo = file
    nuser_obj.phone_number = phone_number
    nuser_obj.real_name = real_name
    nuser_obj.password = password

    nuser_obj.identity_number = identity_number
    nuser_obj.invitation_code = invitation_code
    nuser_obj.max_invitation_number = max_invitation_number
    nuser_obj.save()
    return HttpResponseRedirect('/management/approval')


@login_required(login_url='/')
def approval(request):
    id = request.POST.get('id')
    approval_status = request.POST.get('approval_status')
    reject_reason = request.POST.get('reject_reason')
    nuser_obj = models.NUser.objects.get(id=int(id))
    nuser_obj.approval_status = approval_status
    nuser_obj.reject_reason = reject_reason
    nuser_obj.save()
    request.session['nuser'] = nuser_obj
    return HttpResponseRedirect('/management/')


@login_required(login_url='/')
def view_child(request):
    id = request.POST.get('id')
    approval_status = request.POST.get('approval_status')
    reject_reason = request.POST.get('reject_reason')
    nuser_obj = models.NUser.objects.get(id=int(id))
    nuser_obj.approval_status = approval_status
    nuser_obj.reject_reason = reject_reason
    return render(request, 'management/approval/child.html', context={'users': get_child(int(id), [])})


def read_file(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


@login_required(login_url='/')
def export_nuser(request):
    nusers = models.NUser.objects.all().values('phone_number',
                                               'real_name', 'identity_number', 'id',
                                               'password', 'identity_photo__file_net_path',
                                               'status', 'approval_status', 'approval_time',
                                               'create_time', 'invitation_code',
                                               'invitation_user__invited_user__real_name',
                                               'invited_user__invitation_user__real_name','reject_reason'
                                               )
    for u in nusers:
        u['count'] = get_count(u['id'], 0)
        u['invitation_user'] = get_invitation_user(u['id'])
    file_path = nuser_excel(nusers)
    response = StreamingHttpResponse(read_file(file_path))
    response["Content-Type"] = "application/octet-stream"  # 这里就写这个就可以，如果错了你去看中文乱码就会格式不对
    response['Content-Disposition'] = 'attachment;filename*=utf-8="用户列表.xlsx"'
    response["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response
