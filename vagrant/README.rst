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

Or use a centos.org snapshot::

  vagrant box add --name centos/stream8 -f https://cloud.centos.org/centos/8-stream/x86_64/images/CentOS-Stream-Vagrant-8-20230925.0.x86_64.vagrant-libvirt.box

Note that you must destroy and rebuild your Vagrant VMs to make use of this newer image::

  vagrant destroy
  vagrant up

Helpful Documentation:

 * https://docs.ansible.com/ansible/latest/scenario_guides/guide_vagrant.html
 * https://www.vagrantup.com/docs/provisioning/ansible.html
 * https://www.vagrantup.com/docs/provisioning/ansible_common.html
