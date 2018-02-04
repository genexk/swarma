# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    print('index')
    return render(request, 'ui/init.html', {})
    #return HttpResponse("home page")

def get_cluster_info(request):
    print('get_cluster_info')
    return render(request, 'ui/get_cluster_info.html', {})
