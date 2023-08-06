# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homebrew_python']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['hbp = homebrew_python.cli:app']}

setup_kwargs = {
    'name': 'homebrew-python',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/homebrew-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
