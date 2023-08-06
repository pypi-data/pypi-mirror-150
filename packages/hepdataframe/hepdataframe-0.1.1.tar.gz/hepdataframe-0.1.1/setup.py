# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hepdataframe']

package_data = \
{'': ['*']}

install_requires = \
['awkward>=1.8.0,<2.0.0', 'numpy>=1.22.3,<2.0.0', 'uproot>=4.2.2,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7'],
 'dev': ['pytest>=6'],
 'docs': ['sphinx>=4.0,<5.0',
          'sphinx_book_theme>=0.1.0',
          'sphinx_copybutton>=0.3.0'],
 'test': ['pytest>=6']}

setup_kwargs = {
    'name': 'hepdataframe',
    'version': '0.1.1',
    'description': 'HEP Dataframe',
    'long_description': "# HEP Dataframe\n\n[![Actions Status][actions-badge]][actions-link]\n[![Documentation Status][rtd-badge]][rtd-link]\n\n<!-- [![Code style: black][black-badge]][black-link] -->\n\n[![PyPI version][pypi-version]][pypi-link]\n\n<!-- [![Conda-Forge][conda-badge]][conda-link] -->\n\n[![PyPI platforms][pypi-platforms]][pypi-link]\n\n[![GitHub Discussion][github-discussions-badge]][github-discussions-link]\n\n<!-- [![Gitter][gitter-badge]][gitter-link] -->\n\n<!-- prettier-ignore-start -->\n[actions-badge]:            https://github.com/hepdataframe/hepdataframe/workflows/CI/badge.svg\n[actions-link]:             https://github.com/hepdataframe/hepdataframe/actions\n[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg\n[black-link]:               https://github.com/psf/black\n[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/hepdataframe\n[conda-link]:               https://github.com/conda-forge/hepdataframe-feedstock\n[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github\n[github-discussions-link]:  https://github.com/hepdataframe/hepdataframe/discussions\n[gitter-badge]:             https://badges.gitter.im/https://github.com/hepdataframe/hepdataframe/community.svg\n[gitter-link]:              https://gitter.im/https://github.com/hepdataframe/hepdataframe/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge\n[pypi-link]:                https://pypi.org/project/hepdataframe/\n[pypi-platforms]:           https://img.shields.io/pypi/pyversions/hepdataframe\n[pypi-version]:             https://badge.fury.io/py/hepdataframe.svg\n[rtd-badge]:                https://readthedocs.org/projects/hepdataframe/badge/?version=latest\n[rtd-link]:                 https://hepdataframe.readthedocs.io/en/latest/?badge=latest\n[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg\n<!-- prettier-ignore-end -->\n\nA Dataframe class for HEP data analysis.\n\n_Author's note: This is NOT a work of fiction. Any similarity to\n[ROOT::RDataframe](https://root.cern/manual/data_frame/) or\n[Pandas](https://pandas.pydata.org/) is purely intentional._\n",
    'author': 'Felipe Silva',
    'author_email': 'felipe.silva@cern.ch',
    'maintainer': 'Felipe Silva',
    'maintainer_email': 'felipe.silva@cern.ch',
    'url': 'https://github.com/hepdataframe/hepdataframe',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
