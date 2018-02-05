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
from api.models import Cluster, Node
from api.utils.dynamic_inventory import inv
from api.utils.runplaybook import runplaybook
import yaml
import json
import os
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

class get_cluster_info(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    def post(self, request, format=None):
        data=request.data
        print(data["data"])
        clustername = json.loads(data["data"])["clustername"]
        c = Cluster.objects.get(clustername = clustername)
        n = Node.objects.filter(cluster = c)
        print(c)
        print(n)
        output = {'clustername': c.clustername,
                  'datetime_added': c.datetime_added,
                  'join_token_manager': c.join_token_manager,
                  'join_token_worker': c.join_token_worker, 
                  'number_of_nodes': len(n),
                  'nodes': {},
                  }
        for node in n:
            output['nodes'][node.hostname] = {
                                              'ip': node.ip,
                                              'role': node.role,
                                              'locked': node.locked,
                                              }
        return Response(output)

    def get(self, request, format=None):
        return Response([c.clustername for c in Cluster.objects.all()])



class init_cluster(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    def run_init(self, cluster, nodes):
        print(inv().to_file(''))
        print(os.getcwd())
        pass
 
    def post(self, request, format=None):
        data=request.data
        output = {'success': False, 'error':""}
        self.run_init("", "")
        try:
            clustername = yaml.load(json.loads(data["data"])["clustername"])
            nodes = yaml.load(json.loads(data["data"])["nodes"])
        except Exception as e:
            print(e)
            output['error']+="%s"%(e)
            return Response(output)
    
        if clustername == None or Cluster.objects.filter(clustername=clustername).exists():     
            output['error']+="Clustername must not be empty or cluster with the same name already exists"
            return Response(output)
        else:
            for hostname in nodes.keys():
                if Node == "" or Nodes.objects.filter(hostname=hostname).exists():
                     output['error'] += "Node hostname must not be empty or node with the same hostname already exists"
                     return Response(output)
        
        return self.run_init(clustername, nodes)
         
        
        
        
        
    

