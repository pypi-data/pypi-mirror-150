# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elysium']

package_data = \
{'': ['*']}

install_requires = \
['deta>=1.1.0,<2.0.0', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'elysium',
    'version': '0.0.1',
    'description': 'Deta Base Typed ODM',
    'long_description': None,
    'author': 'Ian Kollipara',
    'author_email': 'ian.kollipara@cune.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
