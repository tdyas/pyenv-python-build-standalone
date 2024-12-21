# Pyenv Plugin for Python Build Standalone

This is a rough draft of a plugin for [`pyenv`](https://github.com/pyenv/pyenv) to install Python versions built by the [Python Build Standalone project](https://github.com/indygreg/python-build-standalone/releases/tag/20241206) as pyenv-managed Pythons.

## Installation

1. Create the pyenv plugins directory: `mkdir "$(pyenv root)/plugins"`

2. Clone this repository into your pyenv plugins directory: `git clone https://github.com/tdyas/pyenv-python-build-standalone.git "$(pyenv root)/plugins/pyenv-python-build-standalone"`

## Usage

### Install a PBS Python

The plugin adds a new `pyenv install-pbs` subcommand which will download and install Python builds from the Python Build Standalone site. The metadata necessary to do that comes with the plugin.

For example, install the latest Python 3.12 patchlevel and PBS release tag from PBS: `pyenv install-pbs 3.12`

Or install a specific PBS release by running: `pyenv install-pbs 3.13.1+20241206`

The name of the particular PBS version will be `pbs-PYTHON_VERSION+PBS_RELEASE_TAG`. You can then use that name with `pyenv global` to make it visible on the system.

### Listng releases

Run `pyenv install-pbs --list` to see a list of all known PBS Python releases. The output will be in the form of `pbs-PYTHON_VERSION+PBS_RELEASE_TAG` for each release.
