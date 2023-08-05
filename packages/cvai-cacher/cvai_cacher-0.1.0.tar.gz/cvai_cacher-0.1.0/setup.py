# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvai_cacher']

package_data = \
{'': ['*']}

install_requires = \
['cvai-logger>=0.1.0,<0.2.0', 'redis>=4.3.1,<5.0.0']

setup_kwargs = {
    'name': 'cvai-cacher',
    'version': '0.1.0',
    'description': 'ClearVision AI cacher',
    'long_description': None,
    'author': 'Gautham Reddy',
    'author_email': 'gauthamv93@yaho.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
