# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calculadora_do_fillipe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'calculadora-do-fillipe',
    'version': '0.1.0',
    'description': 'Nova biblioteca bonita em time!',
    'long_description': None,
    'author': 'Mariana Pinheiro',
    'author_email': 'mariana.pinheiro@loggi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
