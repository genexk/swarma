# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from api.serializers import * 
from api.models import Node
from api.utils.dynamic_inventory import inv
from api.utils.runplaybook import runplaybook
import yaml
import json
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class GenAnsibleInv(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    def get(self, request, format=None):
        i = inv()
        return Response(i.gen())


class RunPlaybook(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    def get(self, request, format=None):
        r = runplaybook()
        return Response(r.run())

class Echo(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def post(self, request, format=None):
        data=request.data
        print(data["data"])
        print(type(data["data"]))
        nodes = yaml.load(json.loads(data["data"])["nodes"])
        print(nodes)
        return Response(data["data"])
