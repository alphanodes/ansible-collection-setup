# Ansible Role: Composer

## Requirements

- `php` (version 5.4+) should be installed and working
- `git` should be installed and working
- `unzip` (required when using `composer_global_packages`)

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    composer_path: /usr/local/bin/composer

The path where composer will be installed and available to your system. Should be in your user's `$PATH` so you can run commands simply with `composer` instead of the full path.

    composer_keep_updated: false

Set this to `true` to update Composer to the latest release every time the playbook is run.

    composer_home_path: '~/.composer'
    composer_home_owner: root
    composer_home_group: root

The `COMPOSER_HOME` path and directory ownership; this is the directory where global packages will be installed.

    composer_version: ''

You can install a specific release of Composer, e.g. `composer_version: '1.0.0-alpha11'`. If left empty the latest development version will be installed. Note that `composer_keep_updated` will override this variable, as it will always install the latest development version.

    composer_version_branch: '--2'

By default, the latest version `2.x` of Composer is installed. If you need to install the legacy version `1.x`, set `composer_version_branch: '--1'`. If you need the latest preview version, set `composer_version_branch: '--preview'`, or `composer_version_branch: ''` to always get the latest (could be a new major version, like 3.x).

    composer_global_packages: []

A list of packages to install globally (using `composer global require`). If you want to install any packages globally, add a list item with a dictionary with the `name` of the package and a `release`, e.g. `- { name: phpunit/phpunit, release: "4.7.x" }`. The 'release' is optional, and defaults to `@stable`.

    composer_add_to_path: true

If `true`, and if there are any configured `composer_global_packages`, the `vendor/bin` directory inside `composer_home_path` will be added to the system's default `$PATH` (for all users).

    composer_add_project_to_path: false
    composer_project_path: /path/to/project/vendor/bin

If `true`, and if you have a project that requires Composer's `vendor/bin` directory be added to the `$PATH`, set that path with `composer_project_path`.

    composer_github_oauth_token: ''

GitHub OAuth token, used to avoid GitHub API rate limiting errors when building and rebuilding applications using Composer. Follow GitHub's directions to [Create a personal access token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) if you run into these rate limit errors.

    php_executable: php

The executable name or full path to the PHP executable. This is defaulted to `php` if you don't override the variable.

## Dependencies

None (but make sure you've installed PHP; the `alphanodes.setup.php` role can be used for this purpose).

## Example Playbook

    - hosts: servers
      roles:
        - alphanodes.setup.php
        - alphanodes.setup.composer

After the playbook runs, `composer` will be placed in `/usr/local/bin/composer` (this location is configurable), and will be accessible via normal user accounts.

## License

MIT

## Author Information

Originally created by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).

Adapted for AlphaNodes GmbH.
