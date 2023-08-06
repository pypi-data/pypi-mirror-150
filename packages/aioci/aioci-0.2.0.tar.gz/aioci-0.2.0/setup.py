# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioci']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aioci',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas.svensson@intility.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
