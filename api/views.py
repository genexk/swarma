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


    def save_to_model(self, cluster, nodes):
        c = Cluster.objects.create(clustername = cluster)
        print(c)
        for k in nodes.keys():
            n = Node.objects.create(hostname=k, role=nodes[k]['role'], cluster=c, locked=False)
            print(n)
        return True
    def run_init(self, cluster, nodes):
        # save to model
        print(self.save_to_model(cluster,nodes))
        # generate inventory with all nodes
        inv_file = inv().to_file(inv().gen_cluster_inv(cluster))
        # run ping playbook to check initial connectivity
        playbook_file = 'api/playbooks/ping.yml'
        r = runplaybook()
        print(r.run_any(playbook_file=playbook_file, inventory_file=inv_file))
        # run docker install playbook to setup the environment
        playbook_file= 'api/playbooks/docker_install.yml'
        ##print(r.run_any(playbook_file=playbook_file, inventory_file=inv_file))
        # generate inventory for the master node to init swarm cluster
        for k, v in nodes.items():
            if v['role'] == 'manager':
                break
        inv_file = inv().to_file(inv().gen_node_inv(k))
        # run docker_init playbook to init swarm cluster
        playbook_file = 'api/playbooks/docker_init.yml'
        r = runplaybook()
        result = r.run_any(playbook_file=playbook_file, inventory_file=inv_file)
        print(result['output'].keys())
        print(len(result['output']['plays']))
        print(result['output']['plays'])
        # save token to cluster
        for task in result['output']['plays'][0]['tasks']:
            if task['task']['name']=="init swarm on target node":
                manager_token = task['hosts'][k]['result']['init_cluster_output']['manager_token'] 
                worker_token = task['hosts'][k]['result']['init_cluster_output']['worker_token']
                c = Cluster.objects.get(clustername=cluster)
                c.join_token_manager = manager_token
                c.join_token_worker = worker_token 
                c.save()
        # generate inventory file excluding init node
        temp_inv1 = inv().gen_cluster_inv(clustername=cluster, exclude=[k])
        # attach tokens
        temp_inv2 = inv().attach_vars(temp_inv1, cluster, {'token_m': manager_token, 'token_w': worker_token})
        inv_file = inv().to_file(temp_inv2)       
        playbook_file = 'api/playbooks/docker_nodes.yml'
        r = runplaybook()
        result = r.run_any(playbook_file=playbook_file, inventory_file=inv_file)
        print(result)

       
    def post(self, request, format=None):
        data=request.data
        output = {'success': False, 'error':""}
        try:
            clustername = yaml.load(json.loads(data["data"])["clustername"])
            print(clustername)
            nodes = yaml.load(json.loads(data["data"])["nodes"])
            print(nodes)
        except Exception as e:
            print(e)
            output['error']+="%s"%(e)
            return Response(output)
    
        if clustername == None or Cluster.objects.filter(clustername=clustername).exists():     
            output['error']+="Clustername must not be empty or cluster with the same name already exists"
            return Response(output)
        else:
            for hostname in nodes.keys():
                if Node == "" or Node.objects.filter(hostname=hostname).exists():
                     output['error'] += "Node hostname must not be empty or node with the same hostname already exists"
                     return Response(output)
        print(clustername)
        print(type(nodes))
        print(nodes) 
        output['success']=self.run_init(clustername, nodes)

        return Response( output) 
         
        
        
        
class destroy_cluster(APIView):
    def run_destroy(self,clustername):
        try: 
            c = Cluster.objects.get(clustername=clustername) 
        except Exception as e:
            print(type(e))
            print(e)
            return False
        inv_file = inv().to_file(inv().gen_cluster_inv(clustername))
        playbook_file = 'api/playbooks/ping.yml'
        r = runplaybook()
        print(r.run_any(playbook_file=playbook_file, inventory_file=inv_file))
        playbook_file= 'api/playbooks/docker_leave.yml'
        result = r.run_any(playbook_file=playbook_file, inventory_file=inv_file)
        print(result['output'].keys())
        for instance in result['output']['stats'].keys():
            print(instance)
            if result['output']['stats'][instance]['failures'] !=0:
                print('failures in running leave playbook')
                return False
        print(Node.objects.filter(cluster=c).delete())
        print(c.delete())
        return True 
        
    def post(self, request, format=None):
        data=request.data
        output = {'success': False, 'error': ""}
        try:
            clustername = yaml.load(json.loads(data["data"])["clustername"])
            print(clustername)
        except Exception as e:
            print(e)
            output['error']+="%s"%(e)
            return Response(output)         
        output['success'] = self.run_destroy(clustername)
        return Response(output)
    

