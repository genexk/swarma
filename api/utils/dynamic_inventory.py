#! /usr/bin/env python

import json
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
        filename = 'tmp/%s.hosts'%(self.rand())
        with open(filename, 'w+') as f:
            f.write(inv)
        return filename

    def gen(self):
        for c in Cluster.objects.all():
            self.inventory[c.clustername]=[]
            for n in Node.objects.filter(cluster=c):
                self.inventory[c.clustername].append(n.hostname)
                self.inventory['_meta']['hostvars'][n.hostname]={'role': n.role,
                                                                 'locked': n.locked,}
        return self.inventory


    def gen_cluster_inv(self, clustername,exclude=[]):
        inventory = {}
        inventory['_meta']={}
        inventory['_meta']['hostvars']={}
        c = Cluster.objects.get(clustername=clustername)
        for n in Node.objects.filter(cluster=c):
             if n.hostname not in exclude:
                 inventory[c.clustername].append(n.hostname)
                 inventory['_meta']['hostvars'][n.hostname]={'role': n.role,
                                                             'locked': n.locked,}
        return inventory 

    def gen_node_inv(self, hostname):
        inventory = {}
        inventory['_meta']={}
        inventory['_meta']['hostvars']={}
        c = Cluster.objects.get(clustername=clustername)
        n = Node.objects.get(hostname=hostname)
        inventory[c.clustername].append(n.hostname)
        inventory['_meta']['hostvars'][n.hostname]={'role': n.role,
                                                    'locked': n.locked,}
        return inventory

        

        
if __name__=="__main__":
    i = inv()
    print(json.dumps(i.gen()))
