#!/usr/bin/python
import errno
import re
import os
import subprocess
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import PY2


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: krb_principal

short_description: Create Kerberos principals and export keytabs
description:
   - This module uses /usr/sbin/kadmin.local to create users and export
     keytab files.

options:
   name:
     description:
       - The name of the kerberos principal, for example "kdreyer@EXAMPLE.COM"
     required: true
   state:
     description:
       - The only allowed value is "present".
     required: false
     choices: [present]
   keytab:
     description:
       - If specified, Ansible will extract a .keytab file to this path.
       - If any file already exists at this path, then Ansible will delete the
         file and create a new keytab if Ansible also created a new principal.
         If Ansible did not create a new principal, then it will not delete or
         edit this file if it exists.
       - Ansible does not validate that the pre-existing file is a keytab.
     required: false
requirements:
  - "python >= 2.7"
'''

EXAMPLES = '''
- name: Create a user and a keytab.
  hosts: localhost
  tasks:
    - name: Create a kdreyer keytab
      krb_principal:
        name: kdreyer@EXAMPLE.COM
        keytab: /var/local/kdreyer.keytab
'''


def kadmin(query):
    """ Call "kadmin.local -q" with this query. """
    cmd = tuple(['/usr/sbin/kadmin.local']) + tuple(query.split())
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    if PY2:
        return output
    return output.decode('utf-8')


def get_principal(name):
    """ Return the full principal name, or None if it does not exist. """
    output = kadmin('getprinc %s' % name)
    for line in output.splitlines():
        if line.startswith('Principal:'):
            _, principal = line.split(':')
            return principal


def create_principal(name):
    """ Create an account, and return the full principal name. """
    output = kadmin('addprinc -randkey %s' % name)
    for line in output.splitlines():
        m = re.match('Principal "[^"]+" created.', line)
        if m:
            return m.group(0)
    raise RuntimeError('could not scrape addprinc output: %s' % output)


def extract_keytab(principal, keytab):
    """ Extract a keytab file for a principal. """
    kadmin('ktadd -k %s -norandkey %s' % (keytab, principal))


def run_module():
    module_args = dict(
        name=dict(required=True),
        keytab=dict(type='path'),
        state=dict(choices=['present'], default='present'),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    check_mode = module.check_mode
    params = module.params
    name = params['name']
    keytab = params['keytab']

    changes = []
    principal = get_principal(name)
    if not principal:
        changes.append('create principal %s' % name)
        if not check_mode:
            principal = create_principal(name)

    if keytab:
        if changes and not check_mode:
            # Delete the keytab
            try:
                os.remove(keytab)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        if not os.path.exists(keytab):
            changes.append('extract keytab %s' % keytab)
            if not check_mode:
                extract_keytab(principal, keytab)

    if not changes:
        module.exit_json(changed=False)

    module.exit_json(changed=True, stdout_lines=changes)


def main():
    run_module()


if __name__ == '__main__':
    main()
