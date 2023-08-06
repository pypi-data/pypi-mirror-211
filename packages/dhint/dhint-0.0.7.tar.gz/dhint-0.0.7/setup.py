# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dhint', 'dhint.base']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.6,<2.0.0', 'typing-extensions>=4.6.2,<5.0.0']

setup_kwargs = {
    'name': 'dhint',
    'version': '0.0.7',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
