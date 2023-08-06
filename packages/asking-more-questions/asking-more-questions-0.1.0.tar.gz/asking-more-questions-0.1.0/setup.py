# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asking_more_questions']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sqcli = asking_more_questions.client:app']}

setup_kwargs = {
    'name': 'asking-more-questions',
    'version': '0.1.0',
    'description': 'A collection of tools that make ad-hoc queries faster',
    'long_description': None,
    'author': 'Kim TImothy Engh',
    'author_email': 'kimothy@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
