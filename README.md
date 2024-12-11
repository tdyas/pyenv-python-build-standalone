# Pyenv Plugin for Python Build Standalone

This is a rough draft of a plugin for [`pyenv`](https://github.com/pyenv/pyenv) to install Python versions built by the [Python Build Standalone project](https://github.com/indygreg/python-build-standalone/releases/tag/20241206) as pyenv-managed Pythons.

## Installation

1. Clone this repository into your pyenv plugins directory: `git clone https://github.com/tdyas/pyenv-python-build-standalone.git "$(pyenv root)/pyenv-python-build-standalone"

## Usage

The plugin adds a new `pyenv pbs-install` subcommand which will download and install Python builds from the Python Build Standalone site. The metadata necessary to do that comes with the plugin.

For example, install the latest Python 3.12 patchlevel and PBS release tag from PBS: `pyenv pbs-install 3.12`

The name of the particular PBS version will be `pbs-PYTHON_VERSION-PBS_RELEASE_TAG`. You can then use that name with `pyenv global` to make it visible.