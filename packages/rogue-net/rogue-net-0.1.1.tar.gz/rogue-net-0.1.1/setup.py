# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rogue_net', 'rogue_net.tests']

package_data = \
{'': ['*']}

install_requires = \
['entity-gym>=0.1.2,<0.2.0', 'ragged-buffer>=0.3.9,<0.4.0']

setup_kwargs = {
    'name': 'rogue-net',
    'version': '0.1.1',
    'description': 'Ragged batch transformer implementation that is compatible with entity-gym',
    'long_description': None,
    'author': 'Clemens Winter',
    'author_email': 'clemenswinter1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
