#! /usr/bin/env python

import json
import yaml
import os
import string
from random import *
from api.models import Cluster, Node 


class inv:
    inventory = {}
    inventory['_meta']={}
    inventory['_meta']['hostvars']={}
    def __init__(self):
        pass

    def rand(self, n = 8):
        all_char = string.ascii_letters+string.digits
        output = "".join([choice(all_char) for x in range(8)])
        return output

    def to_file(self, inv):
        filename = 'tmp/%s.yml'%(self.rand())
        print(inv)
        with open(filename, 'w+') as f:
            yaml.dump(inv, f, default_flow_style=False)
        return filename

    def gen(self):
        inventory = {}
        for c in Cluster.objects.all():
            inventory[c.clustername]={}
            for n in Node.objects.filter(cluster=c):
                inventory[c.clustername][n.hostname]={}
                inventory[c.clustername][n.hostname]={'role': n.role,
                                                      'locked': n.locked,}
        return inventory


    def gen_cluster_inv(self, clustername,exclude=[]):
        inventory = {}
        c = Cluster.objects.get(clustername=clustername)
        inventory[c.clustername]={'hosts':{}}
        for n in Node.objects.filter(cluster=c):
             if n.hostname not in exclude:
                 inventory[c.clustername]['hosts'][n.hostname]={}
                 inventory[c.clustername]['hosts'][n.hostname]={'role': n.role,
                                                                'locked': n.locked,}
        return inventory 
    
    def gen_node_inv(self, hostname):
        inventory = {}
        c = 'all'
        inventory[c]={'hosts':{}}
        n = Node.objects.get(hostname=hostname)
        inventory[c]['hosts'][n.hostname]={}
        inventory[c]['hosts'][n.hostname]={'role': n.role,
                                           'locked': n.locked,}
        return inventory

        
    def attach_vars(self, inv, clustername, var_dict):
        inv[clustername]['vars'] = var_dict
        return inv

    def attach_node_vars(self, inv, clustername, hostname, var_dict):
        for k,v in var_dict.items():
            inv[clustername]['hosts'][hostname][k]=v
        return inv
        
        
        
if __name__=="__main__":
    i = inv()
    print(json.dumps(i.gen()))
