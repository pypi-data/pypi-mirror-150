# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaccard_precalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jaccard-precalc',
    'version': '0.1.2',
    'description': 'The Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.',
    'long_description': None,
    'author': 'mandrewstuart',
    'author_email': 'andrew_matte_@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
