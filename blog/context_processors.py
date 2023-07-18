from blog import models
from system import settings


def global_content(request):
    context = {'is_login': request.session['is_login'] if request.session.has_key('is_login') else False,
               'is_nlogin': request.session['nlogin'] if request.session.has_key('nlogin') else False,
               'nuser': request.session['nuser'] if request.session.has_key('nuser') else False,
               'user': request.session['login_user'] if request.session.has_key('login_user') else None,
               'msg': request.session['msg'] if request.session.has_key('msg') else '','domain':settings.DOMAIN,
               'category': models.Category.objects.all().order_by('seq')}
    if context['is_login']:
        context['tags'] = models.Tags.objects.all()

    return context
