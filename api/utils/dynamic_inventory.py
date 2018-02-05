#! /usr/bin/env python

import json
import os
from api.models import Cluster, Node 


class inv:
    inventory = {}
    inventory['_meta']={}
    inventory['_meta']['hostvars']={}
    def __init__(self):
        pass

    def gen(self):
        for c in Cluster.objects.all():
            self.inventory[c.clustername]=[]
            for n in Node.objects.filter(cluster=c):
                self.inventory[c.clustername].append(n.hostname)
                self.inventory['_meta']['hostvars'][n.hostname]={'role': n.role,
                                                                 'locked': n.locked,}
        return self.inventory


    def gen_cluster_inv(self, clustername):
        inventory = {}
        inventory['_meta']={}
        inventory['_meta']['hostvars']={}
        c = Cluster.objects.get(clustername=clustername)
        for n in Node.objects.filter(cluster=c):
             inventory[c.clustername].append(n.hostname)
             inventory['_meta']['hostvars'][n.hostname]={'role': n.role,
                                                         'locked': n.locked,}
        return inventory 

    def gen_node_inv(self, hostname):
        pass   
        
if __name__=="__main__":
    i = inv()
    print(json.dumps(i.gen()))
