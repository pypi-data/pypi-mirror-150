# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src_'}

packages = \
['nautobot_utsc',
 'nautobot_utsc.diffsync',
 'nautobot_utsc.diffsync.bluecat',
 'nautobot_utsc.diffsync.yaml']

package_data = \
{'': ['*']}

install_requires = \
['debugpy',
 'django-auth-ldap',
 'django-debug-toolbar',
 'django-environ',
 'html-table-parser-python3>=0.2.0',
 'nautobot>=1.3',
 'nautobot_ssot>=1.1.0',
 'utsc.core']

setup_kwargs = {
    'name': 'nautobot-utsc',
    'version': '2022.5.10.1',
    'description': 'A collection of UTSC-specific modifications and extensions to Nautobot.',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
