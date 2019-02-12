Ansible playbook(s) for automating the `Koji server install process
<https://docs.pagure.org/koji/server_howto/>`_.

This sets up the Kerberos (GSSAPI) method of authentication. I use this to
quickly set up Koji in VMs in OpenStack.

Playbooks
---------

* ``setup-koji.yml`` - Installs and configures a Kerberos KDC, koji-hub, and
  koji-builder.

Run this playbook on a RHEL 7 or CentOS 7 host with EPEL enabled. /mnt/koji
should be a disk with plenty of space.

Hard-coded things
-----------------

This is a santized code drop from a set of internal playbooks, so several
things are currently hard-coded:

* The hostname is hardcoded in several places as "kojidev.example.com".

* The main username is hardcoded in several places as "kdreyer".

* This playbook does not generate any new SSL certificates. It assumes you
  already have an SSL CA and key pair. The `koji-ssl-admin tool
  <https://pagure.io/koji-tools/blob/master/f/src/bin/koji-ssl-admin>` can
  help with this.

  * roles/koji-hub/files/kojidev.example.com.chain.crt
  * roles/koji-hub/files/kojidev.example.com.crt
  * roles/koji-hub/files/kojidev.example.com.csr
  * roles/koji-hub/files/kojidev.example.com.key


Roles
-----

* ``roles/kdc`` - installs and configures a Kerberos KDC, and bootstraps all
  the keytabs we need.

  This will create a "kdreyer/admin" Kerberos admin
  account (not really used), and then a "kdreyer" normal Kerberos account. The
  "kdreyer" one will be bootstrapped into Koji later. If you need more
  Kerberos users, add them here.

* ``roles/koji-hub`` - installs and configures Koji Hub

  This will bootstrap "kdreyer" as the first Koji administrator in the
  database.

  If you need more users, add them with the `koji_user <>` module

* ``roles/koji-builder`` - installs and configures a Koji builder.

See Also
--------

For managing resources within your Koji hub, please see the
https://github.com/ktdreyer/koji-ansible project.
