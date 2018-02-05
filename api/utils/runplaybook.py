import subprocess
import os
import re
import json

class runplaybook:
    cluster = 'all'
    playbook = 'facts.yml'
    inventory_script = 'dynamic_inventory_standalone.py'
    script_path = '/code/swarma/api/utils/'
    def __init__(self, cluster='all', playbook='facts.yml'):
        self.cluster = cluster
        self.playbook=playbook
        pass


    def run(self):
        my_env = os.environ.copy()
        my_env["ANSIBLE_STDOUT_CALLBACK"] = "json" 
        proc = subprocess.Popen(['/usr/bin/ansible-playbook', '-i', os.path.join(self.script_path,self.inventory_script), os.path.join(self.script_path, self.playbook)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
        print(' '.join(['ansible-playbook', '-i', os.path.join(self.script_path,self.inventory_script), os.path.join(self.script_path, self.playbook)]))
        stdout_value,stderr_value = proc.communicate()
        #print(stdout_value)
        stdout_clean = json.loads(re.search(r'(\{.*\})', stdout_value, re.S).group(0) )
        print(stdout_clean)
        return {'output': stdout_clean, 'error': stderr_value}
        

    def run_any(self, playbook_file, inventory_file):
        my_env = os.environ.copy()
        my_env["ANSIBLE_STDOUT_CALLBACK"] = "json"
        print(' '.join(['/usr/bin/ansible-playbook', '-i', inventory_file, playbook_file]))
        proc = subprocess.Popen(['/usr/bin/ansible-playbook', '-i', inventory_file, playbook_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
        stdout_value,stderr_value = proc.communicate()
        print(stdout_value)
        stdout_clean = json.loads(re.search(r'(\{.*\})', stdout_value, re.S).group(0) )
        print(stdout_clean)
        return {'output': stdout_clean, 'error': stderr_value}
