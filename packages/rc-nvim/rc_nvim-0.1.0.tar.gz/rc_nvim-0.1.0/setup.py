# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rc_nvim']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rc-nvim',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Remote Container NeoVim\n\nThis is an implementation for supporting Remote Container for NeoVim.\n\n\n',
    'author': 'Sanskar Jethi',
    'author_email': 'sansyrox@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
