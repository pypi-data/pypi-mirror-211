# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsxstyler']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.1.2,<4.0.0', 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'xlsxstyler',
    'version': '0.1.4',
    'description': 'Some rudimentary styling of excel tables and placing pictures using openpyxl',
    'long_description': None,
    'author': 'Gwang-Jin Kim',
    'author_email': 'gwang.jin.kim.phd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
