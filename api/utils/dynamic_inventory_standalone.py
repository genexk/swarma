#! /usr/bin/env python
import os, sys

proj_path = "/code/swarma"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swarma.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import json
import pprint
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

        #random8 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)]) 
        #with open(
        return self.inventory
if __name__=="__main__":
    i = inv()
    print(json.dumps(i.gen()))
    #pp=pprint.PrettyPrinter(indent=4)
    #pp.pprint(i.gen())
