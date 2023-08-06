# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkbottle_types',
 'vkbottle_types.codegen',
 'vkbottle_types.codegen.methods',
 'vkbottle_types.codegen.responses',
 'vkbottle_types.events',
 'vkbottle_types.events.enums',
 'vkbottle_types.events.objects',
 'vkbottle_types.methods',
 'vkbottle_types.responses']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.6,<2.0.0', 'vkbottle>=4.3.12,<5.0.0']

setup_kwargs = {
    'name': 'vkbottle-types',
    'version': '5.131.146.16',
    'description': 'Types for vkbottle',
    'long_description': 'None',
    'author': 'timoniq',
    'author_email': 'None',
    'maintainer': 'FeeeeK',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
