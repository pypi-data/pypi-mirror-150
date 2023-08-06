# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wiktrola']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wiktrola',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
