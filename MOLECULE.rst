molecule cheat sheet
--------------------

Simple one-shot create/run example::

    molecule test -s centos8

I encountered problems with centos7 that took a while to track down
(https://github.com/containers/libpod/issues/6183).

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

  podman rmi localhost/molecule_local/centos:8

Hints for parameterizing this and running it in CI:

https://www.jeffgeerling.com/blog/2018/testing-your-ansible-roles-molecule

https://www.jeffgeerling.com/blog/2020/travis-cis-new-pricing-plan-threw-wrench-my-open-source-works

Replicating GitHub Actions locally
-----------------------------

GitHub Actions runs the tests in an Ubuntu Focal VM. It can be tedious to push
changes to GitHub, wait, and review the output. You may want to set up your
own local Ubuntu Focal VM when making large changes that impact the tests.

Follow these instructions to set up Docker on your own Ubuntu Focal VM in a
similar way to GitHub Actions::

  sudo apt-get update
  sudo apt-get -y install docker.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker ubuntu
  # log out and log back in as "ubuntu" to get the new "docker" posix group.

  sudo apt-get -y install python3-pip
  pip3 install docker molecule[ansible,docker] --user
