# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvola_api']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'mvola-api',
    'version': '1.0.0',
    'description': 'Python package for MVola API',
    'long_description': None,
    'author': 'tsiresymila',
    'author_email': 'tsiresymila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
