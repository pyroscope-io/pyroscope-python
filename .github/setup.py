# -*- coding: utf-8 -*-
# This file here is only here for this page to render properly:
#   https://github.com/pyroscope-io/pyroscope-python/network/dependents

from setuptools import setup

packages = \
['pyroscope', 'pyroscope_io']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyroscope-io',
    'version': '0.5.0',
    'description': 'Pyroscope integration for Python',
    'long_description': '',
    'author': 'Pyroscope Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
