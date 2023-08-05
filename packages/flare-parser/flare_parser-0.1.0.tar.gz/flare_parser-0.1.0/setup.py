# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flare_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flare-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'user',
    'author_email': 'user@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
