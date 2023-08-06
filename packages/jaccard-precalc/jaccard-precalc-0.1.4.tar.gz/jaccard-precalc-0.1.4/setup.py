# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaccard_precalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jaccard-precalc',
    'version': '0.1.4',
    'description': 'The Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.',
    'long_description': "====================================\nJaccard Precalculated String Matcher\n====================================\n\nThe Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.\n\nexample usage:\n\n``from jaccard_precalc.JaccardPrecalc import JaccardPrecalc\nstring_list = ['Andrew Matte, 123 Main St, Toronto, Canada']\njac = JaccardPrecalc(string_list)\n# jac.search(query_string, number_of_results)\nresults = jac.search('Andy Matte, Toronto, CA', 1) # returns a list of dicts where each dict is {input: score}, sorted by top score``",
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
