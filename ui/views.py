# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    print('index')
    return render(request, 'ui/index.html', {})
    #return HttpResponse("home page")

def clusters(request):
    print('clusters')
    return render(request, 'ui/clusters.html', {})

def nodes(request):
    print('nodes')
    return render(request, 'ui/nodes.html', {})

def cluster(request):
    print('cluster')
    if request.method != 'POST':
        return render_index(request)
    else:
        data = json.loads(request.POST["data"])
        clustername  = data["clustername"]
        
    return render(request, 'ui/cluster.html', {})

def node(request):
    print('node')
    return render(request, 'ui/node.html', {})

def create_cluster(request):
    print('create_cluster')
    return render(request, 'ui/init.html', {})

def destroy_cluster(request):
    print('destroy_cluster')
    return render(request, 'ui/destroy.html',{})

def dashboard(request):
    print('dashbard')
    return render(request, 'ui/dash.html', {})
