# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sharktopoda_client',
 'sharktopoda_client.decorators',
 'sharktopoda_client.localization',
 'sharktopoda_client.model',
 'sharktopoda_client.udp']

package_data = \
{'': ['*']}

install_requires = \
['Rx>=3.2.0,<4.0.0', 'dataclasses-json>=0.5.4,<0.6.0', 'zmq>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'sharktopoda-client',
    'version': '0.1.4',
    'description': 'Sharktopoda client API, translated to Python',
    'long_description': None,
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
