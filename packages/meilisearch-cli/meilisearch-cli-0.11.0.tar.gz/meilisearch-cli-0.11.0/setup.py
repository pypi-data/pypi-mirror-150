# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meilisearch_cli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1',
 'meilisearch>=0.18.3,<0.19.0',
 'requests==2.27.1',
 'rich==12.4.1',
 'typer==0.4.1']

entry_points = \
{'console_scripts': ['meilisearch-cli = meilisearch_cli.main:app']}

setup_kwargs = {
    'name': 'meilisearch-cli',
    'version': '0.11.0',
    'description': 'CLI for MeiliSearch',
    'long_description': '# MeiliSearch CLI\n\n[![Tests Status](https://github.com/sanders41/meilisearch-cli/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/meilisearch-cli/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-cli/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-cli/main)\n[![Coverage](https://codecov.io/github/sanders41/meilisearch-cli/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-cli)\n[![PyPI version](https://badge.fury.io/py/meilisearch-cli.svg)](https://badge.fury.io/py/meilisearch-cli)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meilisearch-cli?color=5cc141)](https://github.com/sanders41/meilisearch-cli)\n\nA CLI for working with MeiliSearch\n\n## Installation\n\nInstallation with [pipx](https://github.com/pypa/pipx) is recommended.\n\n```sh\npipx install meilisearch-cli\n```\n\nAlternatively MeiliSearch CLI can be installed with pip.\n\n```sh\npip install meilisearch-cli\n```\n\n## Usage\n\nAll commands require both a url for MeiliSearch and a master key. These values can either be passed\nusing the flags `--url` and `--master-key`, or can be read from the environment variables\n`MEILI_HTTP_ADDR` and `MEILI_MASTER_KEY`. The one exception is the `health` comman only requires the\nurl, and does not take a master key.\n\nAs an example, if the `MEILI_HTTP_ADDR` and `MEILI_MASTER_KEY` vairables are not set you can\nretrieve the version with:\n\n```sh\nmeilisearch-cli get-version --url http://localhost:7700 --master-key masterKey\n```\n\nor if the environment variables are set you can omit `--url` and `--master-key`:\n\n```sh\nmeilisearch-cli get-version\n```\n\nTo see a list of available commands run:\n\n```sh\nmeilisearch-cli --help\n```\n\nTo get information on individual commands add the `--help` flag after the command name. For example\nto get information about the `add-documents` command run:\n\n```sh\nmeilisearch-cli add-documents --help\n```\n\n## Example\n\n### Get Version\n\n![Get Version](https://github.com/sanders41/meilisearch-cli/raw/main/imgs/get-version.png)\n\n### Get Document\n\n![Get Document](https://github.com/sanders41/meilisearch-cli/raw/main/imgs/get-document.png)\n\n### Documentation\n\nThe MeiliSearch documentation sections can be displayed with clickable links to each section. The\nlinks are built based on the current state of the documentation and will automatically stay\nup-to-date with the latest documentation. To follow the links command + click on a Mac or\ncontrol + click on Linux and Windows. Note that some terminals do not support clickable links.\nIn this case the documentation tree will be displayed but not be clickable.\n\n![MeiliSearch Documentation](https://github.com/sanders41/meilisearch-cli/raw/main/imgs/docs.png)\n\n## Compatibility with MeiliSearch\n\nThis package only guarantees compatibility with [version v0.27 of MeiliSearch](https://github.com/meilisearch/MeiliSearch/releases/tag/v0.27.0).\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sanders41/meilisearch-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
