# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipyfacets']

package_data = \
{'': ['*']}

install_requires = \
['facets-overview>=1.0,<2.0',
 'ipython>=8.3,<9.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.4,<2.0']

setup_kwargs = {
    'name': 'ipyfacets',
    'version': '0.3.0',
    'description': 'The facets project(https://github.com/PAIR-code/facets) wrapper for jupyter',
    'long_description': "jupyter-facets\n==============\n\nProviding `facets <https://github.com/PAIR-code/facets>`_ wrapper for jupyter\n\n\nInstallation\n============\n::\n\n   pip install ipyfacets\n\nUsage\n=====\nImport::\n\n    import ipyfacets as facets\n\nFacets Overview::\n\n    facets.overview({'train': df_train, 'test': df_test})\n\nFacets Dive::\n\n    facets.dive(df)\n\nExample\n=======\nSee `Jupyter nbviewer <https://nbviewer.jupyter.org/github/porkbeans/jupyter-facets/blob/master/examples/simple_example.ipynb>`_\n",
    'author': 'porkbeans',
    'author_email': 'mizuo.taka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/porkbeans/jupyter-facets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
