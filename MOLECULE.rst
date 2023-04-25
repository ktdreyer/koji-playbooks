molecule cheat sheet
--------------------

Simple one-shot create/run example::

    molecule test -s centos8

To debug molecule, set the ``MOLECULE_NO_LOG=false`` environment variable and
add the ``--debug`` command-line option. For example::

    MOLECULE_NO_LOG=false molecule --debug test -s centos8

Instead of the all-in-one "test" sub-command, you can break down the steps
into individual commands.

    - Create and start a container::

          molecule create -s centos8

    - Run the "converge" step, to apply the roles specified in
      ``converge.yml``::

          molecule converge -s centos8

    - Destroy the running container::

          molecule destroy -s centos8

Verify that the container is running::

    podman ps -a

(and look for a container named "instance".)

Shell into the container instance::

    molecule login -s centos8

(If that does not work, try ``podman exec -it instance /bin/sh``)

Review the container's systemd log output::

    podman logs instance

Clean up the local container image that molecule created::

    podman rmi localhost/molecule_local/centos:stream8

Hints for parameterizing this and running it in CI:

https://www.jeffgeerling.com/blog/2018/testing-your-ansible-roles-molecule

https://www.jeffgeerling.com/blog/2020/travis-cis-new-pricing-plan-threw-wrench-my-open-source-works

Replicating GitHub Actions locally
-----------------------------

GitHub Actions runs the tests in an Ubuntu Jammy VM. It can be tedious to push
changes to GitHub, wait, and review the output. You may want to set up your
own local Ubuntu Jammy VM when making large changes that impact the tests.

Follow these instructions to set up Podman on your own Ubuntu Jammy VM in a
similar way to GitHub Actions::

  sudo apt-get update
  # follow the steps in .github/workflows/...

  sudo apt-get -y install python3-pip
  pip3 install molecule[ansible,podman] --user


Versioning
----------

There are many bugs in podman, Ansible, and Molecule. Please run the latest
versions of each.

Version combinations that are known to work:
- python3-molecule-3.0.5-2.fc32
- ansible-2.9.14-1.fc32
- podman-2.1.1-7.fc32

Note that since we run systemd in the container, that means that the systemd
version in CentOS 8 and the kernel version on the host (eg Fedora) sometimes
interact poorly. See https://bugzilla.redhat.com/1853736 for an example.
