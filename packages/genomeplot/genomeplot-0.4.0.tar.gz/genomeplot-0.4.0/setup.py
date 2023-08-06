# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genomeplot', 'genomeplot.prerolled']

package_data = \
{'': ['*'], 'genomeplot.prerolled': ['data/*']}

install_requires = \
['bokeh>=2.4.0,<2.5.0', 'pandas>=1.4.0,<1.5.0', 'pyfaidx>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'genomeplot',
    'version': '0.4.0',
    'description': 'A package for simplifying genome-wide plots',
    'long_description': '# genomeplot\n\n## overview\n\nA simple wrapper to `bokeh`, streamlining genome-wide visualisations.\n\n## documentation\n\nhttps://hardingnj.github.io/genomeplot/\n\n## installation\n\nEither via pip:\n`python -m pip install genomeplot`\n\nor from source using `poetry`\n\n## requirements\n\nSee `pyproject.toml`\n',
    'author': 'Nick Harding',
    'author_email': 'nickharding@cegx.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hardingnj.github.io/genomeplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
