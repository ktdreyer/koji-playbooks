Bring up a new server::

    vagrant up --no-destroy-on-error

Re-run the Ansible playbooks (if they failed, or if you changed something)::

    vagrant provision

Log in with SSH::

    vagrant ssh

Destroy the VM and disk::

    vagrant destroy

Pull down an updated CentOS image from Vagrant Cloud::

    vagrant box update

Helpful Documentation:

 * https://docs.ansible.com/ansible/latest/scenario_guides/guide_vagrant.html
 * https://www.vagrantup.com/docs/provisioning/ansible.html
 * https://www.vagrantup.com/docs/provisioning/ansible_common.html
