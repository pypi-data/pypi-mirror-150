# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strpay']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'strpay',
    'version': '0.1.0.dev0',
    'description': '',
    'long_description': None,
    'author': 'Jun Luo',
    'author_email': '4catcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
