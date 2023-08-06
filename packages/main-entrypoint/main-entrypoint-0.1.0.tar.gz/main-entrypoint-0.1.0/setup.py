# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['main_entrypoint']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'main-entrypoint',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jonathan Striebel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
