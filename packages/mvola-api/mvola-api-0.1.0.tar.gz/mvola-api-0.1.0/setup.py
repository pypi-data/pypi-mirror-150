# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvola_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mvola-api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tsiresy.mila',
    'author_email': 'tsiresy.mila@ezway-technology.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
