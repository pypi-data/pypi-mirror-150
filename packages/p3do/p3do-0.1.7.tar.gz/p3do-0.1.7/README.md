<div align="center">

# p3do - let 'em minions do it

![PyPI - License](https://img.shields.io/pypi/l/p3do)
![PyPI](https://img.shields.io/pypi/v/p3do)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/p3do)

p3do (pronounced _pee-three-duh_) is a collection of command-line utilities for
p3d. It allows you to conjure some tedious operations right from your magic little
fingertips.

<img src="res/p3do-animation.gif?raw=true" alt="p3do in action" width="75%"/>

<p />

[Installation](#installation) •
[Getting started](#getting-started) •
[Commands](#commands) •
[Contribute](#contribute)

</div>

## Installation

`p3do` is built on Python 3.8 or later installed. You can get Python from your
package manager du jour or download and install it from
https://www.python.org/downloads/ (looking at you Windows. Mac.
Whyihavetobother. Veryannoyingyouare.)

`p3do` is published to the [CheeseShop](https://pypi.org/project/p3do/) and
hence can be installed with pip:

```bash
pip install p3do
```

`p3do` installs itself as a command. If your `$PATH` is set up correctly you
will be able to just invoke `p3do` like so

```bash
p3do --help
```

## Getting Started

Light a bonfire and whisper _p3do_ in the most conspirative voice available to
you. Then start a terminal.

`p3do` is hierarchical, self-documenting and discoverable. The best way to start
is to just type `p3do`. This will show you the available commands and some
description. From there you can drill down the hierarchy for useful sub-command.

Each sub-command/command group has special flags and configuration. How to use
them is explained in [Commands](#commands) for each of them separately. You can
also use `p3d <group> <command> --help` in your terminal for concise on-line
help.

## Commands

`p3do` is hierarchical. Commands are batched into groups which can be further
nested into parent groups. We follow the same principle in the documentation
here.

* [`kc`](#kc): Keycloak commands
    - [KC Configuration](#kc-configuration): Not a command but read this first!
    - [`add-mappers`](#add-mappers): Add mappers to IdPs from realm export


### kc

Commands in this group allow to perform operations for Keycloak. Most of them
need authentication and server information. Please read [KC
Configuration](#kc-configuration) first on how to add your configuration.

Commands:
* [KC Configuration](#kc-configuration): Not a command but read this first!
* [`add-mappers`](#add-mappers): Add mappers to IdPs from realm export

#### KC Configuration

kc commands usually need some information about the server, realm and
authentication. This information can be read from a configuration file, given
via CLI parameters or interactively if information is missing. CLI parameters
take precendence and override any configuration read from a configuration file.

***Note:*** you don't need a configuration file at all. All (partial) parameters
can be specified via CLI arguments. Just leave out the `--auth_config` and
`--auth` flags.

A full configuration file which specifies all available options looks like this:

```ini
[test]
server=https://keycloak.example.com/auth/
username=admin
user_realm_name=master
password=password
realm_name=my-app
```

`[test]` is the name of the configuration. You can have multiple configurations
for different servers in your config file. `server`, `username`, `password` are
rather self-explanatory. `user_realm_name` is the realm the _user_ is in. This
is not necessarily the same realm as the one you want to modify. `realm_name` is
the realm name you want to modify (it usually does not make sense to put this
into the config file).

To specify the config file and config name you want to use, invoke a `p3do` command like this:

```bash
# `config.ini` is the config file, `test` is the config section you want to use
p3do kc add-mappers --auth_config config.ini --auth test <...other arguments...>
```

Note that you can override any configuration via CLI arguments:

```bash
# Override `admin` from `config.ini` with `admin2`
p3do kc add-mappers --auth_config config.ini --auth test --username admin2 <...other arguments...>
```

The configuration can also be partial:
```ini
[partial-test]
server=https://keycloak.example.com/auth/
username=admin
user_realm_name=master
```

Note that we don't specify a `password` or `realm_name` here. You can now invoke `p3do` with

```bash
# Complete `partial-test` via arguments
p3do kc add-mappers --auth_config config.ini --auth partial-test --password password --realm_name my-other-app <...other arguments...>
```

You can also just invoke `p3do` as before and will be asked interactively to fill out the missing pieces:

```bash
# No `password` or `realm_name` from `config.ini` or cli arguments
p3do kc add-mappers --auth_config config.ini --auth partial-test <...other arguments...>
# `p3do` will ask you to complete them interactively
Password: password
Realm_name: my-other-app
```

#### add-mappers

Add IdP mappers from a realm export `.json` to a realm. The IdP must already
exist and correspond to the IdP name specified in the mapper config. Keycloak
does not import mapper configuration by itself (yet?).

```bash
# `realm-export.json` is the path the the export file
p3do kc add-mappers --auth_config config.ini --auth test realm-export.json
```

## Contribute

***`p3do` is licensed under MIT and published to PyPI (including source). Do not
add sensitive company data. Any sensitive data has to be read from external
configuration files.***

### Contributors

All contributions are welcome. This can be new commands, improvements to the
on-line help, documentation or spelling mistakes. Just open a PR with your
changes. If your changes are larger, you find a bug but don't know how to fix
it, or you are just unsure if your idea fits, open an issue on GitHub first.

### Maintainers

The `p3do` main branch is protected and PRs have to be approved by by
[maintainers](CODEOWNERS) (code owners in GitHub lingo). Tooling like this can
easily grow out of control. Maintainers ensure that this is not happening to
`p3do`. Here are some guidelines.

- Every command in `p3do` must have a well known and feasible (manual)
  alternative
- `p3do` must not smear over too complicated process. If a process is too
  complicated fix the process.
- `p3do` must not obfuscate processes. If knowledge about how things work isn't
  spread enough, spread it.
- `p3do` must not gatekeep processes. It is not a mechanism for access
  management.
- `p3do` believes in the competency of its users

### Release Maintainers

Releases are pushed to [PyPI](https://pypi.org/project/p3do/). This requires
a token with Maintainer or Owner status on PyPI.

Releases are automatically created and pushed by a [GitHub
Action](https://github.com/swc-friedla/p3do/actions/workflows/publish.yml) when
a tagged release is created in GitHub.

Repository and release maintainers is probably but not necessarily the same set
of people.
