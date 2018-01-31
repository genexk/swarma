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
import re
import subprocess


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
        self.info = info
        self.role = role
        self.locked = locked
        self.token = token
        self.ip = ip
        self.port = port
        self.init = init
    
    def get_info(self):
        return self.client.info()

    def get_node_ls(self):
        proc = subprocess.Popen(['docker','node','ls','--format','"{{json .}}"'], stdout = subprocess.PIPE)
        raw_out = proc.communicate()[0]
        result = [json.loads(node) for node in raw_out.replace('"{', '{').replace('}"\n', '}\n').strip('\n').split()]
        return result

    def get_self_node_status(self):
        for node in get_node_ls():
            if node['Self']:
                return node
        return None

    def get_node_status(self, hostname):
        for node in get_node_ls():
            if node['Hostname']==hostname:
                return node
        return None

    def is_ready(self, current_node=True, hostname = None):
        if current_node:
            return get_self_node_status()['Status'] == 'Ready'
        else:
            return get_node_status(hostname)['Status'] == 'Ready'
    
    def is_leader(self, current_node=True, hostname = None):
        if current_node:
            return get_self_node_status()['ManagerStatus'] == 'Leader'
        else:
            return get_node_status(hostname)['ManagerStatus'] == 'Leader'

    def is_manager(self, current_node=True, hostname = None):
        if current_node:
            return get_self_node_status()['ManagerStatus'] == 'Leader' or get_self_node_status()['ManagerStatus'] == 'Reachable'
        else:
            return get_node_status(hostname)['ManagerStatus'] == 'Leader' or get_node_status()['ManagerStatus'] == 'Reachable'

    def _is_active(self, current_node=True, hostname = None):
        if current_node:
            return get_self_node_status()['ManagerStatus'] == 'Leader'
        else:
            return get_node_status(hostname)['ManagerStatus'] == 'Leader'

    def is_active(self):
        data = self.get_info()
        if data['Swarm']['LocalNodeState']=='active':
            return True
        return False

    def set_node_manager():
        pass

    def set_node_worker():
        pass
    
    def 

    
    def role_mod(self):
        if self.role == 'manager':
            if not self.is_manager():
                self.set_node_manager()
        if self.role == 'worker':
            if self.is_manager():
                self.set_node_worker()

    def 
            

    def init_cluster(self):
        print('init_cluster')
        out = False
        port = ""
        manager_token = ""
        worker_token = ""
        result = {}
        if self.port != None:
            port = ":"+self.port
        if self.ip == None:
            # going to add try-except around client.swarm.init()
            first_iface = None
            for iface in ni.interfaces(): 
                if iface[0] == 'e':
                    first_iface = iface
            if first_iface == None:
                self.error += 'Cannot find a physical interface, please specifythe ip or the interface name. Available ifaces: %s\n'%ni.interfaces()
            else:
                full_adv_addr = first_iface+port
        else:
            full_adv_addr = self.ip+port
        try:    
            out = self.client.swarm.init(advertise_addr = full_adv_addr, force_new_cluster=False)
        except docker.errors.APIError as e:
            self.error += 'Failed init new Swarm cluster: %s\n'%e
        proc = subprocess.Popen(['docker', 'info','--format','"{{json .}}"'], stdout=subprocess.PIPE)
        raw_out = proc.communicate()[0]
        #rc, raw_out, err = module.run_command('docker info --format "{{json .}}"', executable=executable, use_unsafe_shell=shell, encoding=None)
        raw_out = raw_out.strip()
        info_json = json.loads(raw_out[1:-1])
        
        if info_json['Swarm']['LocalNodeState']=='active':
            out = True
            proc = subprocess.Popen(['docker', 'swarm', 'join-token','manager'],stdout=subprocess.PIPE)  
            raw_out = proc.communicate()[0]
            r = re.search(r'docker swarm.*token (.*)', raw_out)
            manager_token = r.group(1)

            proc = subprocess.Popen(['docker', 'swarm', 'join-token','manager'],stdout=subprocess.PIPE)
            raw_out = proc.communicate()[0]
            r = re.search(r'docker swarm.*token (.*)', raw_out)
            worker_token = r.group(1)
        result ={'success': out, 'manager_token': manager_token, 'worker_token': worker_token, 'error': self.error}
        return result

    def join(self, token, remote_addr):
        return self.client.join(remote_addrs = remote_addr, token = token)
    def get_current_role(self
    def role_mod(self):
        

    def lock_state(self):
        pass 

    def run(self):
        swarm_helper_output = {}
        if self.info:
            swarm_helper_output['get_info_output'] = self.get_info()
        if self.init:
            swarm_helper_output['init_cluster_output'] = self.init_cluster()
        if self.role:
            swarm_helper_out['role_mod_output'] = self.role_mod()
        if not self.init:
            swarm_helper_out['lock_state_output'] = self.lock_state()        
            
        
def main():
    module_args = dict(
        name = dict(type='str', required=False),
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
    init = module.params['init']
    ip = module.params['ip']

    helper = swarm_helper(info = info, role = role, init = init, ip  = ip )
    helper_result = helper.run()
    module.exit_json(changed=False, result = helper_result)


if __name__=='__main__':
   main()
