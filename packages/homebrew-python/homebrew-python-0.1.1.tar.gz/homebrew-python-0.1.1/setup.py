# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homebrew_python']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'homebrew-python',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
