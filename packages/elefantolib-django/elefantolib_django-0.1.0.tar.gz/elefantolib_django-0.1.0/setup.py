# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elefantolib_django', 'elefantolib_django.serializers']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.2.1,<5.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'elefantolib>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'elefantolib-django',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Aibar',
    'author_email': 'bekaybar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
