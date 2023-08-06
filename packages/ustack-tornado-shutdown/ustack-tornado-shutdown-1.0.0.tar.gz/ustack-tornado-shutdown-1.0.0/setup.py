# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ustack_tornado_shutdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ustack-tornado-shutdown',
    'version': '1.0.0',
    'description': 'Library for gracefully terminating a Tornado server on SIGTERM',
    'long_description': None,
    'author': 'uStudio Developers',
    'author_email': 'dev@ustudio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
