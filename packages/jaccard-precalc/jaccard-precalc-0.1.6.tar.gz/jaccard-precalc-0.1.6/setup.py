# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaccard_precalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jaccard-precalc',
    'version': '0.1.6',
    'description': 'The Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.',
    'long_description': "# Jaccard Precalculated String Matcher\n\nThe Jaccard index measures exhaustive substring comparison of two strings. This package is a slightly modified Jaccard with pre-calculation accelerate results.\n\n```python3\n    from jaccard_precalc.JaccardPrecalc import JaccardPrecalc\n    string_list = ['Andrew Matte, 123 Main St, Toronto, Canada']\n    jac = JaccardPrecalc(string_list)\n    # jac.search(query_string, number_of_results)\n    results = jac.search('Andy Matte, Toronto, CA', 1) # returns a list of dicts where each dict is {input: score}, sorted by top score\n\n```",
    'author': 'mandrewstuart',
    'author_email': 'andrew_matte_@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
