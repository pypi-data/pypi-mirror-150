# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ichika-utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ichika-utils',
    'version': '0.1.0',
    'description': 'Stats Utils for Ichika',
    'long_description': '# Ichika Utils\n\nA set of utils used by Ichika. This is not production ready, and not even ready for anything. this is highly experimental.',
    'author': 'No767',
    'author_email': '73260931+No767@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/No767/Ichika-Utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
