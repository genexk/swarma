#! /usr/bin/env python


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}
DOCUMENTATION = '''
---
module: docker_swarm

short_description: manages docker swarm 

version_added: "2.4"

description:
    - "to-do"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''


EXAMPLES = '''   '''

RETURN = '''
image:
    description: to-do.
    returned: success
    type: complex
    sample: {}
'''

from ansible.module_utils.basic import *
import docker
import netifaces as ni

class swarm_helper:
    error = ""

    info = False
    role = None
    locked = None
    token = None
    ip = None
    port = None
    init = False
    client = docker.from_env()
    def __init__(self, info=False, role = None, locked = None, token = None, ip = None, port = None, init = False):
        self.info = False
        self.role = None
        self.locked = None
        self.token = None
        self.ip = None
        self.port = None
        self.init = False
    
    def get_info(self):
        return client.info()

    def init_cluster(self):
        out = False
        port = ""
        if self.port != None:
            port = ":"+self.port
        if self.ip == None:
            # going to add try-except around client.swarm.init()
            first_iface = None
            for iface in ni.interfaces(): 
                if iface[0] == 'e':
                    first_iface = iface
            if first_iface == None:
                self.error += 'Cannot find a physical interface, please specify the interface name. Available ifaces: %s\n'%ni.interfaces()
            else:
                full_adv_addr = first_iface+port
                out = client.swarm.init(advertise_addr = full_adv_addr) 
        else:
            full_adv_addr = self.ip+port
            out = client.swarm.init(advertise_addr = full_adv_addr)
        if out:
            proc = subprocess.Popen(['docker', 'swarm', 'join-token','manager'],stdout=subprocess.PIPE)  
            raw_out = proc.communicate()[0]
            r = re.search(r'docker swarm.*token (.*)', raw_out)
            manager_token = r.group(1)

            proc = subprocess.Popen(['docker', 'swarm', 'join-token','manager'],stdout=subprocess.PIPE)
            raw_out = proc.communicate()[0]
            r = re.search(r'docker swarm.*token (.*)', raw_out)
            worker_token = r.group(1)
        return out
        
def main():
    module_args = dict(
        role = dict(type='str', required=False),
        locked = dict(type='bool', required=False),
        token = dict(type='str', required=False),
        ip = dict(type='str', required=False),
        port = dict(type='str', required=False),
        init = dict(type='bool', required=False),
        info = dict(type='bool', default=False),
    )
    
    module = AnsibleModule(module_args)
    
    info = module.params['info']
    role = module.params['role']
    
    info_out = {}
    if info:
        client = docker.from_env()
        info_out = client.info()
    
    module.exit_json(changed=False, result=info_out)


if __name__=='__main__':
   main()
