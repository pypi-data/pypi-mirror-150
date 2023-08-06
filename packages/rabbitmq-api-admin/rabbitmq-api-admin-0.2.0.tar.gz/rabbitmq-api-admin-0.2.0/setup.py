# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rabbitmq_admin']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'rabbitmq-api-admin',
    'version': '0.2.0',
    'description': 'A python interface for the RabbitMQ Admin HTTP API',
    'long_description': None,
    'author': 'UMA.TECH',
    'author_email': 'developers@uma.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Uma-Tech/rabbitmq-api-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
