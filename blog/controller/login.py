import logging

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from system.enum import status
from system.error.ServerException import ServerException

LOG = logging.getLogger('blog.views')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        logging.info('{0} {1} 用户尝试登录'.format(username, password))
        context = {
            'msg': '',
        }
        if username is None or password is None:
            request.session['msg'] = status.USER_OR_PASSWORD_NOT_EMPTY
            return HttpResponseRedirect('/')  # 跳转到主界面
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session["login_user"] = user
                request.session["is_login"] = True
                request.session['msg'] = ''
                LOG.info("登录成功")
                return HttpResponseRedirect('/management')  # 跳转到主界面

            else:
                request.session['msg'] = status.USER_OR_PASSWORD_ERROR
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='/')
def logout(request):
    request.session["login_user"] = None
    request.session["is_login"] = False
    request.session['msg'] = ''
    auth.logout(request)
    return HttpResponseRedirect('/')  # 跳转到主界面
