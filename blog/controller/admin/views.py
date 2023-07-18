from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

import blog
from blog import models


@xframe_options_sameorigin
@login_required(login_url='/login')
def index(request):
    return render(request, 'management/index.html')

