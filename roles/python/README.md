# Ansible Role: Python

An Ansible Role that installs Python with pip and virtualenv on Linux.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    python_packages:
      - python3-pip
      - python3-virtualenv

The name of the packges to install to use python with pip on the system.

    python_pip_executable: pip3

Use can set the pip executable name. If not set, ansible/system default is used.

    python_pip_packages: []

A list of packages to install with pip. Examples below:

    python_pip_packages:
      # Specify names and versions.
      - name: docker
        version: "1.2.3"
      - name: awscli
        version: "1.11.91"

      # Or specify bare packages to get the latest release.
      - docker
      - awscli

      # Or uninstall a package.
      - name: docker
        state: absent

      # Or update a package ot the latest version.
      - name: docker
        state: latest

      # Or force a reinstall.
      - name: docker
        state: forcereinstall

      # Or install a package in a particular virtualenv.
      - name: docker
        virtualenv: /my_app/venv

## Example Playbook

    - hosts: all

      vars:
        python_pip_packages:
          - name: docker
          - name: awscli

      roles:
        - alphanodes.setup.python
