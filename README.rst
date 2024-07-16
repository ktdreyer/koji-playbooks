.. image:: https://github.com/ktdreyer/koji-playbooks/workflows/tests/badge.svg
             :target: https://github.com/ktdreyer/koji-playbooks/actions

Ansible playbook(s) for automating the `Koji server install process
<https://docs.pagure.org/koji/server_howto/>`_.

This sets up the Kerberos (GSSAPI) method of authentication. I use this to
quickly set up Koji in VMs in OpenStack.

Playbooks
---------

* ``setup-koji.yml`` - Installs and configures a Kerberos KDC, koji-hub, and
  koji-builder.

Run this playbook on a RHEL or CentOS 7 or 8 host with EPEL enabled. /mnt/koji
should be a disk with plenty of space.

SSL configuration
-----------------

* This playbook generates an SSL CA and keypair using the `koji-ssl-admin tool
  <https://pagure.io/koji-tools/blob/master/f/src/bin/koji-ssl-admin>`_ .

  The Certificate Authority keypair:
    * ``/etc/pki/koji/koji-ca.crt``
    * ``/etc/pki/koji/koji-ca.key``

  The Apache web server HTTPS keypair (signed by koji-ca above):
    * ``/etc/pki/koji/kojidev.<domain>.chain.crt``
    * ``/etc/pki/koji/kojidev.<domain>.key``

  For GSSAPI (Kerberos) authentication, these are the only SSL certs you will
  need.

  The koji-hub role publishes the Koji CA at the following URL:
  https://kojidev.<domain>/kojifiles/koji-ca.crt . External Koji clients
  can download this file to verify the HTTPS connections.

Configure deploy
----------------

Prepare

- Disable selinux
- Disable firewalld
- Install python3 package on the destination system.
- Copy SSH public key

KOJI Domain

Domain can be configured in `setup-koji.yml` with variable `KOJI_DOMAIN`.domain
For example,

.. code-block:: yaml
  vars:
    KOJI_DOMAIN: stackwebservices.com

The main username

The main username is specified in `setup-koji.yml` file:

For example,

.. code-block:: yaml
  vars:
    KOJI_USER: ktdreyer
    KRB_PASSWORD: test


Inventory

```
cp inventory.ini.tpl inventory.ini
```

Roles
-----

* ``roles/kdc`` - installs and configures a Kerberos KDC, and bootstraps all
  the keytabs we need.

  This will create a "kdreyer" Kerberos account. The ``koji-hub`` role will
  bootstrap this account into Koji's database. If you need more Kerberos
  users, add them here.

* ``roles/koji-ssl-admin`` - Creates the SSL CA and HTTPS keypair for the Koji
  server.

* ``roles/koji-client`` - Configures a ``kojidev`` script and `profile
  <https://docs.pagure.org/koji/profiles/>`_.

* ``roles/postgresql`` - installs and configures PostgreSQL for Koji Hub

* ``roles/koji-hub`` - installs and configures Koji Hub

  This role requires the `koji_host
  <https://github.com/ktdreyer/koji-ansible/blob/master/library/koji_host.py>`_
  module from the `koji-ansible project
  <https://github.com/ktdreyer/koji-ansible>`_.

  This role will bootstrap "kdreyer" as the first Koji administrator in the
  database.

  If you need more users, add them with the `koji_user
  <https://github.com/ktdreyer/koji-ansible/blob/master/library/koji_user.py>`_
  module.

* ``roles/koji-web`` - installs and configures the web interface for Koji.

* ``roles/koji-builder`` - installs and configures a Koji builder.

* ``roles/koji-ra`` - installs and configures the Koji "ra" (repository admin)
  service.

* ``roles/koji-gc`` - installs and configures the Koji garbage collector
  service.

* ``roles/activemq`` - installs and configures an ActiveMQ 5 broker for testing
  the Koji Hub protonmsg plugin.

* ``roles/rabbitmq`` - installs and configures a RabbitMQ broker for testing
  the Koji Hub protonmsg plugin.

See Also
--------

For managing resources within your Koji hub, please see the
https://github.com/ktdreyer/koji-ansible project.
